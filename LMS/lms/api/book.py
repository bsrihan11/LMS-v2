from flask import jsonify, request
from flask.views import MethodView
from numpy import delete
from lms.forms import BookForm, format_errors
from lms.api.utils import manager_required
from lms.models import Book
from lms import db,cache

def update_book_cache(book_id,type):

    book = Book.query.get(book_id)
    if book:
        if type == 'FULL' and book.is_available == False:
            return None
        book = book.to_json(type=type)

        cache.set(f"book-{book_id}-{type}", book , timeout = 6 * 60 * 60 )

        return book

    return None

def get_book_cache(book_id,type='FULL'):

    result = cache.get(f"book-{book_id}-{type}")
    if result:
        return result
    else:
        result = update_book_cache(book_id,type)
        return result





class BookResource(MethodView):
        
    def get(self,book_id):
        type = request.args.get('type')
        if type and type == 'BRIEF':
            result = get_book_cache(book_id,type='BRIEF')
            if result:
                return jsonify(book=result),200
            else:
                return jsonify(errors={'general':"invalid book."}),404
            
        if type and type == 'ADMIN':
            book = Book.query.get(book_id)
            if book:
                book_data = book.to_json(type = 'ADMIN')
                return jsonify(book=book_data),200
            
            else:
                return jsonify(errors={'general':"invalid book."}),404

        result = get_book_cache(book_id)
        if result:
            return jsonify(book=result),200
        else:
            return jsonify(errors={'general':"invalid book."}),404

            


    
    @manager_required
    def post(self):
        data = request.get_json()

        form = BookForm(data=data)

        if form.validate():
            new_book = Book(**data)
            db.session.add(new_book)

            db.session.commit()

            new_book.assign_authors(data.get("author_list"))

            if new_book.is_available == True:

                cache.set(f"book-{new_book.book_id}-FULL",new_book.to_json(type='FULL'),timeout = 6 * 60 * 60)
                cache.set(f"book-{new_book.book_id}-BRIEF",new_book.to_json(type='BRIEF'),timeout = 6 * 60 * 60)

            return jsonify(message=f"book created.",book_id=new_book.book_id),200
        else:
            
            return jsonify(errors=format_errors(form.errors)), 401

    @manager_required
    def put(self,book_id):

        book = Book.query.get(book_id)
        if book:
            data = request.get_json()

            form = BookForm(data=data)

            if form.validate():
                if form.is_available.data == False:
                    book.is_available = form.is_available.data
                    db.session.commit()
                    cache.delete(f'book-{book_id}-FULL')
                    cache.delete(f'section-{book.section_id}')
                     
                    from lms.helpers import top_sellers
                    top_sell = top_sellers() 

                    if book.book_id in top_sell:
                        cache.delete('top_sellers')

                    return jsonify(message=f"book successfully removed. ID:{book.book_id}"),200
                  

                flag,old = False,-1
                book.book_name = form.book_name.data
                book.book_cover = form.book_cover.data
                book.book_price = form.book_price.data
                if book.section_id!=form.section_id.data:
                    flag = True
                    old = book.section_id
                book.section_id = form.section_id.data

                book.path = form.path.data
                book.book_summary = form.book_summary.data
                book.year = form.year.data
                book.days = form.days.data
                book.is_available = form.is_available.data

                db.session.commit()

                book.assign_authors(data.get("author_list"))


                if flag and book.section.section_name!='DEFAULT':

                    cache.delete(f"section-{book.section_id}")
                    cache.delete(f"section-{old}")

                cache.set(f"book-{book.book_id}-FULL",book.to_json(type='FULL'),timeout = 6 * 60 * 60)
                cache.set(f"book-{book.book_id}-BRIEF",book.to_json(type='BRIEF'),timeout = 6 * 60 * 60)
                
                return jsonify(message=f"book info updated. ID:{book.book_id}"),200
            
            else:
                return jsonify(errors=format_errors(form.errors)), 401
        else:
            return jsonify(errors={"general":"invalid book."}),404
            
    @manager_required
    def delete(self,book_id):
        book = Book.query.get(book_id)

        if book:
            book.is_available = False
            db.session.commit()
            
            cache.delete(f'book-{book_id}-FULL')

            return jsonify(message="book removed successfully"),200
        else:

            return jsonify(errors={"general":"invalid book."}),404



