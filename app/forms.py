from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField, FileField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileAllowed
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # Custom validator to ensure unique email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered.')

class SubmitContentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=5, max=150)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    submit = SubmitField('Submit Content')

class SymptomCheckerForm(FlaskForm):
    symptom1 = SelectField('Do you experience frequent urination?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
    symptom2 = SelectField('Do you experience pain during urination?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
    symptom3 = SelectField('Do you experience blood in your urine?', choices=[('yes', 'Yes'), ('no', 'No')], validators=[DataRequired()])
    submit = SubmitField('Check Symptoms')

class AddSpecialistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    specialty = StringField('Specialty', validators=[DataRequired(), Length(min=2, max=100)])
    location = StringField('Location', validators=[DataRequired(), Length(min=2, max=150)])
    contact = StringField('Contact Info', validators=[DataRequired(), Length(min=10, max=15)])
    submit = SubmitField('Add Specialist')

class ReportForm(FlaskForm):
    message = TextAreaField('Describe your issue or concern', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit Report')
