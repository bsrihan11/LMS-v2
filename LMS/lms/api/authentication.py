from flask import jsonify, request
from datetime import timedelta
from flask.views import MethodView
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity,set_access_cookies, set_refresh_cookies,unset_jwt_cookies
from lms.models import User,Role
from lms import db
from lms.forms import LoginForm, format_errors

class LoginView(MethodView):

    def post(self):

        data = request.get_json()
        form = LoginForm(data=data)

        if form.validate():
            user = User.query.filter_by(email = form.email.data).first()
            if not user.is_active():
                return jsonify(errors={'general':'User is blocked.'}),401
            
            response = jsonify(message="logged in successfully.")

            if user.role.role_name in ["ADMIN", "MANAGER"]:
                access_token = create_access_token(identity=user.user_id,expires_delta=timedelta(minutes=35))
                refresh_token = create_refresh_token(identity=user.user_id,expires_delta=timedelta(minutes=65))  

                set_access_cookies(response,access_token,max_age=timedelta(minutes=30))
                set_refresh_cookies(response,refresh_token,max_age=timedelta(minutes=60))
            else:
                access_token = create_access_token(identity=user.user_id,expires_delta=timedelta(minutes=30))
                refresh_token = create_refresh_token(identity=user.user_id,expires_delta=timedelta(days=13))

                set_access_cookies(response,access_token,max_age=timedelta(minutes=25))
                set_refresh_cookies(response,refresh_token,max_age=timedelta(days=12))

            return response,200
            
        else:
            return jsonify(errors=format_errors(form.errors)), 401
        


class LogoutView(MethodView):

    @jwt_required(verify_type=False)
    def delete(self):
        response = jsonify(message="logout successful.")
        unset_jwt_cookies(response)
        return response,200

  

class RefreshView(MethodView):
    
    @jwt_required(refresh=True)
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user:
            response = jsonify(message="refreshed access token")

            if user.role.role_name in ["ADMIN", "MANAGER"]:
                access_token = create_access_token(identity=user.user_id,expires_delta=timedelta(minutes=35))
                set_access_cookies(response,access_token,max_age=timedelta(minutes=30))
            
            else:
                access_token = create_access_token(identity=user.user_id,expires_delta=timedelta(minutes=30))
                set_access_cookies(response,access_token,max_age=timedelta(minutes=25))

            
            return response,200

        else:
            return jsonify(errors={'general':'invalid user.'}),401



