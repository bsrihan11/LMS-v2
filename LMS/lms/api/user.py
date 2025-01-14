from asyncio import timeout
from flask import jsonify, request
from datetime import timedelta
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity,set_access_cookies, set_refresh_cookies,unset_jwt_cookies
from lms.models import User,Role
from lms import db,cache
from lms.forms import RegisterationForm,UpdateUserForm, format_errors

class MainResource(MethodView):
    
    def get(self):
        from lms.helpers import top_sellers,sections
        response = {}

        response['top_sellers'] = top_sellers()
        response['sections'] = sections()

        return jsonify(response),200



class UserResource(MethodView):

    def post(self):
        data = request.get_json()
        form = RegisterationForm(data=data)
        if form.validate():
            role_id = Role.query.filter_by(role_name="USER").first().role_id
            new_user = User(**data,role_id=role_id)
            
            db.session.add(new_user)
            db.session.commit()

            return jsonify(message="User created successfully"), 200
        else:
            return jsonify(errors=format_errors(form.errors)), 401
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user_data = cache.get(f'user-{user_id}')

        if not user_data:
            user = User.query.get(user_id)
            if user and user.is_active():
                user_data = user.to_json()
                cache.set(f"user-{user_id}", user_data, timeout=24 * 60 * 60)
            else:
                response = jsonify(errors={'general': 'invalid user.'})
                unset_jwt_cookies(response)
                return response, 401

        collection = cache.get(f'user-{user_id}-collection')

        if collection is None:
            user = User.query.get(user_id)
            collection = user.get_collection()
            cache.set(f"user-{user_id}-collection", collection, timeout=12 * 60 * 60)

        return jsonify(user=user_data, collection=collection), 200


    @jwt_required()
    def put(self):
        data = request.get_json()
        form = UpdateUserForm(data=data)

        if form.validate():
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user.role.role_name in ["ADMIN","MANAGER"]:
                response = jsonify(errors={"general":"Action not allowed."})
                return response,403
            
            user.email = form.email.data
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            db.session.commit()

            user_data = user.to_json()
            cache.set(f"user-{user_id}",user_data,timeout = 24 * 60 * 60)
            response = jsonify(message="successfully updated user details.",
                                user = user_data)
            

            access_token = create_access_token(identity=user.user_id,expires_delta=timedelta(minutes=20))
            refresh_token = create_refresh_token(identity=user.user_id,expires_delta=timedelta(days=13))

            set_access_cookies(response,access_token,max_age=timedelta(minutes=15))
            set_refresh_cookies(response,refresh_token,max_age=timedelta(days=12))


            return response, 200
        else:
            return  jsonify(errors=format_errors(form.errors)), 401
        

    
    @jwt_required()
    def delete(self):
        user = User.query.get(get_jwt_identity())
        if user.role.role_name in ["ADMIN","MANAGER"]:
            response = jsonify(errors="Action not allowed.")
            return response,403


        cache.delete(f"user-{user.user_id}-collection")
        cache.delete(f"user-{user.user_id}")
        db.session.delete(user)
        db.session.commit()

        response = jsonify(message="user deleted successfully.")
        unset_jwt_cookies(response)



        return response, 200
        

