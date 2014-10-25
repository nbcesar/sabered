"""
forms.py

Web forms based on Flask-WTForms

See: http://flask.pocoo.org/docs/patterns/wtforms/
     http://wtforms.simplecodes.com/

"""

from flaskext import wtf
from flaskext.wtf import validators
from wtforms.ext.appengine.ndb import model_form

from .models import Test


class TestForm(wtf.Form):
    test_name = wtf.TextField('Test Name', validators=[validators.Required()])
    num_mc = wtf.IntegerField('Multiple Choice (MC)', validators=[validators.Required()])
    mc_answers = wtf.SelectField('MC Answer Choices', choices=[('4','1, 2, 3, 4'),('3','1, 2, 3'),('5','1, 2, 3, 4, 5'),('6','1, 2, 3, 4, 5, 6')],validators=[validators.Required()])
    num_or = wtf.IntegerField('Open Response (OR)', validators=[validators.Required()])
    #or_points = wtf.SelectField('Max OR Points', choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8')],validators=[validators.Required()])
    num_students = wtf.IntegerField('# of Students', validators=[validators.Required()])

"""
# App Engine ndb model form example
TestForm = model_form(Test, wtf.Form, field_args={
    'test_name': dict(validators=[validators.Required()]),
    'num_mc': dict(validators=[validators.Required()]),
    'num_or': dict(validators=[validators.Required()]),
    'num_students': dict(validators=[validators.Required()])
})
"""

class RegisterForm(wtf.Form):
	first_name = wtf.TextField('First Name', validators=[validators.Required()])
	last_name = wtf.TextField('Last Name', validators=[validators.Required()])
	email = wtf.TextField('Email', validators=[validators.Required()])
	password = wtf.PasswordField('Password',validators=[validators.Required()])
	confirm = wtf.PasswordField('Confirm Password',[validators.Required(), validators.EqualTo('password', message='Passwords must match')])

class LoginForm(wtf.Form):
	email = wtf.TextField('Email', validators=[validators.Required()])
	password = wtf.PasswordField('Password', validators=[validators.Required()])