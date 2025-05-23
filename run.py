from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__,template_folder="templatess",static_folder="static")

app.secret_key="ganesh123"

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:brahmaganesh%4099K@localhost/flask_dd'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


db=SQLAlchemy(app)