from flask import Blueprint
from lms.api.authentication import LoginView,RefreshView,LogoutView
from lms.api.user import UserResource,MainResource
from lms.api.book import BookResource
from lms.api.author import AuthorResource
from lms.api.section import SectionResource
from lms.api.transaction import TransactionResource,RatingResource,PDFResource
from lms.api.search import SearchResource

api = Blueprint('api', __name__)

#----------------------Authentication view-----------------------------------------

login_view = LoginView.as_view('login')
logout_view = LogoutView.as_view('logout')
refresh_view = RefreshView.as_view('refresh')

api.add_url_rule('/login', view_func=login_view, methods=['POST'])
api.add_url_rule('/logout', view_func=logout_view, methods=['DELETE'])
api.add_url_rule('/refresh',view_func=refresh_view,methods = ['POST'])


#----------------------User view--------------------------------------------------------

user_view = UserResource.as_view('user_api')
main = MainResource.as_view('main_api')
api.add_url_rule('/user', view_func=user_view, methods=['GET','POST','PUT','DELETE'])
api.add_url_rule('/main',view_func=main,methods=['GET'])

#----------------------Section view------------------------------------------------------

section_view = SectionResource.as_view('section_api')
api.add_url_rule('/section/<int:section_id>', view_func=section_view, methods=['GET','PUT','DELETE'])
api.add_url_rule('/section', view_func=section_view, methods=['POST'])


#----------------------Author view-------------------------------------------------------

author_view = AuthorResource.as_view('author_api')
api.add_url_rule('/author/<int:author_id>', view_func=author_view, methods=['GET','PUT','DELETE'])
api.add_url_rule('/author', view_func=author_view, methods=['POST'])


#----------------------Book view----------------------------------------------------------

book_view = BookResource.as_view('book_api')
api.add_url_rule('/book/<int:book_id>', view_func=book_view, methods=['GET','PUT','DELETE'])
api.add_url_rule('/book', view_func=book_view, methods=['POST'])

#----------------------Transaction view---------------------------------------------------

transaction_view = TransactionResource.as_view('transaction_api')
api.add_url_rule('/transaction', view_func=transaction_view, methods=['GET','POST','DELETE'])


#----------------------Rating view---------------------------------------------------------

rating_view = RatingResource.as_view('rating_api')
api.add_url_rule('/rating', view_func=rating_view, methods=['PUT'])



#----------------------Rating view---------------------------------------------------------

search_view = SearchResource.as_view('search_api')
api.add_url_rule('/search', view_func=search_view, methods=['GET'])



#----------------------PDF view---------------------------------------------------------

pdf_view = PDFResource.as_view('pdf_api')
api.add_url_rule('/pdf/<int:book_id>', view_func=pdf_view, methods=['GET'])




#----------------------Admin---------------------------------------------------------

from lms.api import admin




