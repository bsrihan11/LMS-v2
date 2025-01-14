from io import BytesIO
from flask import current_app, jsonify, request, send_file
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from lms.models import Transaction,User,Book
from lms import db,cache
from lms.forms import RatingForm, format_errors
import os

class PDFResource(MethodView):
    @jwt_required()
    def get(self, book_id):
        book = Book.query.get(book_id)
        if not book or not book.is_available:
            return jsonify(errors={"general": "invalid book."}), 404

        user = User.query.get(get_jwt_identity())
        if not user or not user.is_active():
            return jsonify(errors={"general": "user is blocked."}), 401

        trans = Transaction.query.filter_by(user_id=user.user_id, book_id=book_id).first()
        if not trans or trans.status != 'AVAILABLE':
            return jsonify(errors={"general": "invalid transaction."}), 401

        input_path = os.path.join(current_app.config['ROOT_PATH'], "lms", "static", book.path)
        with open(input_path, 'rb') as file:
            pdf_bytes = file.read()

        pdf_io = BytesIO(pdf_bytes)
        pdf_io.seek(0)

        return send_file(pdf_io, mimetype='application/pdf', as_attachment=True,download_name=book.path)
    



class TransactionResource(MethodView):

    @jwt_required()
    def get(self):
        book_id = request.args.get("book_id")
        if not book_id:
            return jsonify(errors={'general': 'invalid request.'}), 404

        user = User.query.get(get_jwt_identity())
        if not user or not user.is_active():
            return jsonify(errors={"general": "user is blocked. action not allowed."}), 401

        trans = Transaction.query.filter_by(book_id=book_id, user_id=user.user_id, status='AVAILABLE').first()
        if not trans:
            return jsonify(errors={"general": "invalid transaction."}), 401

        if trans.downloaded:
            return jsonify(errors={"general": "book already downloaded."}), 401

        book = Book.query.get(book_id)

        input_path = os.path.join(current_app.config['ROOT_PATH'], "lms", "static", book.path)
        with open(input_path, 'rb') as file:
            pdf_bytes = file.read()

        pdf_io = BytesIO(pdf_bytes)
        pdf_io.seek(0)
        trans.downloaded = True
        db.session.commit()
        
        return send_file(pdf_io, download_name=book.path)

    @jwt_required()
    def post(self):
        book_id = request.args.get("book_id")
        if not book_id:
            return jsonify(errors={'general': 'invalid request.'}), 404

        user = User.query.get(get_jwt_identity())
        if not user or not user.is_active():
            return jsonify(errors={"general": "user is blocked. action not allowed."}), 401

        try:
            new_collection = user.add_to_collection(book_id)
            return jsonify(message="book added to collection",new_collection=new_collection), 200
        except Exception as error:
            return jsonify(errors={'general': str(error)}), 401


    @jwt_required()
    def delete(self):
        book_id = request.args.get("book_id")
        if book_id:
            user = User.query.get(get_jwt_identity())
            try:
                user.return_book(book_id)
                return  jsonify(message='book returned.'),200
            except Exception as error:
                return jsonify(errors={'general':str(error)}), 401
        else:
            return jsonify(errors={'general':'invalid request.'}),404

        
class RatingResource(MethodView):

    @jwt_required()
    def put(self):
        book_id = request.args.get("book_id")
        rating = request.args.get("rating")
        if not (book_id and rating):
            return jsonify(errors={'general': 'invalid request.'}), 404

        form = RatingForm(rating=rating)
        if not form.validate():
            return jsonify(errors=format_errors(form.errors)), 401

        user = User.query.get(get_jwt_identity())
        if not user:
            return jsonify(errors={"general": "user not found."}), 401

        try:
            user.rate_book(book_id, form.rating.data)
            return jsonify(message=f'gave {rating} to book successfully'), 200
        except Exception as error:
            return jsonify(errors={'general': str(error)}), 401