from flask import jsonify, request
from flask.views import MethodView
from lms.models import Book
from lms import cache
from lms.helpers import fuzzy_search
from lms.api.book import get_book_cache


class SearchResource(MethodView):

    def get(self):
        q = request.args.get('q')
        if not q:
            return jsonify(errors=['invalid request.']), 404
        
        from lms.helpers import fuzzy_search
        result = fuzzy_search(q)
        if len(result) == 0:
            return jsonify(error=['No result found.']), 404
        
        response = jsonify(books=result)
        return response, 200