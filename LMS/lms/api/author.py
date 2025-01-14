from flask import jsonify, request
from flask.views import MethodView
from lms.forms import AuthorForm, format_errors
from lms.api.utils import manager_required
from lms.models import Author,BookAuthor
from lms import db,cache


class AuthorResource(MethodView):


    def get(self,author_id):
        author = Author.query.get(author_id)

        if author:
            return jsonify(author=author.to_json()),200
        else:
            return jsonify(errors= {"general":"invalid author."}),404

    
    @manager_required
    def post(self):
        data = request.get_json()

        form = AuthorForm(data=data)

        if form.validate():
            new_author = Author(**data)

            db.session.add(new_author)

            db.session.commit()

            return jsonify(message=f"author created.",author_id=new_author.author_id),200
        else:
            return jsonify(errors=format_errors(form.errors)), 401



    @manager_required
    def put(self,author_id):

        author = Author.query.get(author_id)
        if author:

            data = request.get_json()

            form = AuthorForm(data=data)

            if form.validate():
                author.author_name = form.author_name.data

                db.session.commit()

                return jsonify(message=f'author updated successfully. ID:{author.author_id}'),200

            else:
                return jsonify(errors=format_errors(form.errors)), 401
        else:
            return jsonify(errors= {"general":"invalid author."}), 404

        
    @manager_required
    def delete(self,author_id):
        author = Author.query.get(author_id)

        if author:
            book_links = BookAuthor.query.filter_by(author_id=author.author_id).all()

            for book_link in book_links:
                db.session.delete(book_link)

            db.session.commit()
            
            db.session.delete(author)
            db.session.commit()

            return jsonify(message="author deleted successfully."),200
        else:

            return jsonify(errors= {"general":"invalid author."}),404
