import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_cors import CORS
from flask_caching import Cache
from lms.celery import make_celery
from lms.config import Config




db = SQLAlchemy()
jwt = JWTManager()
mail = Mail()
cache = Cache()


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    jwt.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    cache.init_app(app)
    database_exists = os.path.isfile('lms.db')

    import lms.models
    if not database_exists:
        with app.app_context():
            db.create_all()

            db.session.commit()


    from lms.api import api
    app.register_blueprint(api,url_prefix="/api")

    import redis
    redis_conn = redis.StrictRedis(host='localhost', port=6379, db=3)
    keys_to_delete = redis_conn.keys()
    if keys_to_delete:
        redis_conn.delete(*keys_to_delete)
        
    return app


app = create_app()
CORS(app, origins=["http://localhost:8080"],supports_credentials=True)



app.extensions['mail'].debug = 0
celery = make_celery(app)
app.app_context().push()



@app.teardown_appcontext
def shutdown_session(exception=None):
   db.session.remove()
