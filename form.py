from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,FileField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
  name=StringField(" Username",validators=[DataRequired(),Length(min=3)])
  email=StringField("Email",validators=[DataRequired(),Length(min=4)])
  password=PasswordField("Password",validators=[DataRequired()])
  submit=SubmitField("Register")


class LoginForm(FlaskForm):
  email=StringField(" Email",validators=[DataRequired(),Length(min=3)])
  password=PasswordField("Password",validators=[DataRequired()])
  submit=SubmitField("Login")

class UpdateForm(FlaskForm):
  username=StringField("username",validators=[DataRequired(),Length(min=3)])
  email=StringField("email",validators=[DataRequired()])
  submit=SubmitField("Update")