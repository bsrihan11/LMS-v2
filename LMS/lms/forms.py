from flask import Flask
from lms.api.utils import is_valid_days, is_valid_password,is_valid_username,\
      is_valid_year,is_valid_section,is_valid_author

from lms.models import User
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError,\
                    IntegerField,PasswordField,TextAreaField,BooleanField
from wtforms.validators import DataRequired, Email,NumberRange,Length,number_range,AnyOf

def format_errors(errors):
    formatted_errors = {}
    for field in errors:
        formatted_errors[field] = str(errors[field][0])
        
    return formatted_errors
    
class BaseForm(FlaskForm):
    class Meta:
        csrf = False
     

    
class EmailForm(BaseForm):
    email = StringField('email', validators=[DataRequired(),
                                             Length(min=1,max=120,
                                                    message="email should not exceed 120 characters."),
                                             Email()])

    def validate(self):
        if super(EmailForm, self).validate():
            
        
            if not User.query.filter_by(email=self.email.data).first():
                self.email.errors.append('email not found.')
            
            return True
    
    


class PasswordForm(BaseForm):
    password = PasswordField('password', validators=[DataRequired(),is_valid_password])


class LoginForm(BaseForm):

    email = StringField('email', validators=[DataRequired(),
                                             Length(min=1,max=120,
                                                    message="email should not exceed 120 characters."),Email()])
    password = PasswordField('password', validators=[DataRequired(),is_valid_password])

    def validate(self):
        if super(LoginForm, self).validate():
        
            user = User.query.filter_by(email=self.email.data).first()
            if user is None:
                self.email.errors.append('email does not exist.please register.')
                return False

            if not user.check_password(self.password.data):
                self.password.errors.append('incorrect password.')
                return False
            return True
        

class RegisterationForm(BaseForm):
    email = StringField('email', validators=[DataRequired(),
                                             Length(min=1,max=120,
                                                    message="email should not exceed 120 characters."), Email()])
    first_name = StringField('first_name',validators=[DataRequired(),
                                                      Length(min=1,max=50,
                                                             message="first name should not exceed 50 characters.")
                                                      ,is_valid_username])
    last_name = StringField('last_name',validators=[DataRequired(),
                                                    Length(min=1,max=50,
                                                           message="last name should not exceed 50 characters."),
                                                    is_valid_username])
    password = PasswordField('password', validators=[DataRequired(),is_valid_password])

    def validate(self):
        if super(RegisterationForm, self).validate():
            
            user = User.query.filter_by(email=self.email.data).first()
            if user is not None:
                self.email.errors.append('email already in use.please Login!')
                return False

            return True
        

class UpdateUserForm(BaseForm):
    email = StringField('email', validators=[DataRequired(),
                                             Length(min=1,max=120,
                                                    message="email should not exceed 120 characters."),
                                                    Email()])
    first_name = StringField('first_name',validators=[DataRequired(),
                                                      Length(min=1,max=50,
                                                             message="first name should not exceed 50 characters.")
                                                             ,is_valid_username])
    last_name = StringField('last_name',validators=[DataRequired(),
                                                    Length(min=1,max=50,
                                                           message="last name should not exceed 50 characters."),
                                                    is_valid_username])


class BookForm(BaseForm):
    book_name = StringField('book_name', validators=[DataRequired(),
                                                     Length(min=1,max=264,
                                                            message="book name should not exceed 264 characters.")])
    book_cover = StringField('book_cover', validators=[DataRequired(),
                                                       Length(min=1,max=100,
                                                              message="book cover should not exceed 264 characters.")])
    book_price = IntegerField('book_price', validators=[DataRequired(),
                                                        NumberRange(min=0,
                                                                    message="book price can't be below 0.")])
    section_id = IntegerField('section_id',validators=[DataRequired(),is_valid_section])
    path = StringField('path',validators=[DataRequired(),
                                          Length(min=1,max=200,
                                                 message="path should not exceed 200 characters.")])
    book_summary = TextAreaField('book_summary', validators=[DataRequired(),
                                                             Length(min=30,max=300,
                                                                    message="book summary should be between 30 and 300 characters.")])
    year = IntegerField('year', validators=[DataRequired(),is_valid_year])
    days = IntegerField('days',validators=[is_valid_days])
    is_available = BooleanField('is_available', validators=[AnyOf([True, False],
                                                                  message="availability should be either true or false.")])
    
    author_list = StringField('author_list',validators=[DataRequired(),is_valid_author])

class AuthorForm(BaseForm):
    author_name = StringField('author_name', validators=[DataRequired(),
                                                         Length(min=1,max=264,
                                                                message="author name should not exceed 264 characters.")])

class SectionForm(BaseForm):
    section_name = StringField('section_name', validators=[DataRequired(),
                                                           Length(min=1,max=264,
                                                                message="section name should not exceed 264 characters.")])
    section_cover = StringField('section_cover', validators=[DataRequired(),
                                                             Length(min=1,max=100,
                                                                  message="section cover should not exceed 100 characters.")])


class RatingForm(BaseForm):
    rating = IntegerField('rating',validators=[DataRequired(),number_range(min=1,max=5,
                                                                           message="Rating should be between 1 and 5.")])
    

class AdUpUserForm(BaseForm):
    user_id = IntegerField("user_id",validators=[DataRequired()])
    active = AnyOf(values=[1,0],message="Invalid value for user active.")
    role_id = AnyOf(values=[1,2,3],message="Invalid value for role.")