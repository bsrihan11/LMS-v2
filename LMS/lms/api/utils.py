from datetime import timedelta
import re
from wtforms import ValidationError
from flask_mail import Message
from flask import request,jsonify,current_app
from functools import wraps
import string
import os
from lms import mail
from lms.models import Section,Author,Permission,User
from flask_jwt_extended import verify_jwt_in_request,get_jwt_identity



def send_email(subject,recipients,body=None,html=None,path=None):

    msg = Message(subject=subject,recipients=recipients,body=body,html=html)

    if path == None:
        mail.send(msg)
    else:
        with current_app.open_resource(path) as pdf:
            msg.attach(filename=os.path.basename(path), content_type='application/pdf', data=pdf.read())

        mail.send(msg)
    




def format_vol_sold(number):
    suffixes = ['', 'thousand', 'million']
    if number == 0:
        return '0'
    magnitude = 0
    while number >= 1000:
        magnitude += 1
        number /= 1000.0
    if magnitude == 0:
        return f"{int(number)}"
    else:
        return f"{int(number)} {suffixes[magnitude]}"
    

    
def detect_html_css_js(form,field):
    input_string = field.data
   
    html_pattern = re.compile(r'<[^>]*>')
    css_pattern = re.compile(r'\bstyle\s*=\s*["\'][^"\']*[\'"]')
    js_pattern = re.compile(r'<script[^>]*>.*?<\/script>', re.DOTALL)

    
    has_html = bool(html_pattern.search(input_string))
    has_css = bool(css_pattern.search(input_string))
    has_js = bool(js_pattern.search(input_string))

    if has_html or has_css or has_js:
        raise ValidationError("no html or script allowed!")
    
    return True


def is_valid_password(form,field):
    password = field.data
    punctuation = re.escape(string.punctuation.replace('"', '').replace("'", ''))
    allowed_characters = string.ascii_letters + string.digits + punctuation
    allowed_pattern = re.compile(f'^[{allowed_characters}]+$')

    if not bool(allowed_pattern.match(password)):
        raise ValidationError(f"only alphabets,digits and punctuations(no quotation marks) allowed.")
    
    if len(password)>22 or len(password)<4:
        raise ValidationError("password should be between 8 and 22 characters.")
    

def is_valid_username(form,field):
    name = field.data
    
    allowed_characters = string.ascii_letters
    allowed_pattern = re.compile(f'^[{allowed_characters}]+$')
    
    if not bool(allowed_pattern.match(name)):
        raise ValidationError(f"only alphabets allowed.")
    
    return True

def is_valid_year(form,field):

    if 1000<=field.data<=9999:
        return True
    else:
        raise ValidationError("invalid year.")
    
def is_valid_days(form,field):
    if 7<=field.data<=90:
        return True
    else:
        raise ValidationError("invalid days.")


def is_valid_section(form,field):
    section = Section.query.get(field.data)
    if not section or section.section_name == "DEFAULT":
        raise ValidationError(f"invalid section id: {field.data}")
        
    return True

def is_valid_author(form,field):
    elements = field.data.split(',')
    for element in elements:
        if not element.strip().isdigit():
            raise ValidationError(f"invalid author id: {element}")
        
    elements = [int(element) for element in elements]

    for id in elements:
        author = Author.query.get(id)
        if not author:
            raise ValidationError(f"invalid author id: {id}")
        
    
    return True


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user = User.query.get(get_jwt_identity())
                
                if not current_user.is_eligible(permission):
                        raise Exception("Insufficient Permissions.")
                else:
                    return f(*args, **kwargs)
            except Exception as e:
                return jsonify(msg=str(e)),401         

        decorated_function.__name__ = f.__name__    
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)

def manager_required(f):
    return permission_required(Permission.MANAGER)(f)



