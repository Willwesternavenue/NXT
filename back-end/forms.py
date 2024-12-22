from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class UserCreateForm(FlaskForm):
    company = StringField('Company Name', validators=[DataRequired(), Length(min=2, max=100)])  # company
    name = StringField('Login ID', validators=[DataRequired(), Length(min=2, max=100)])  # name（login_idとして使用）
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField('Create User')

class LoginForm(FlaskForm):
    name = StringField('Login ID', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=100)])
    submit = SubmitField('Login')

class AdminCreateForm(FlaskForm):
    name = StringField('Admin Name', validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=255)])
    submit = SubmitField('Create Admin')

class AdminLoginForm(FlaskForm):
    name = StringField('Username', validators=[DataRequired()])  # name フィールド
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')