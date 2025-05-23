from run import db



class User(db.Model):
  id= db.Column(db.Integer,primary_key=True)
  name= db.Column(db.String(100),unique=True,nullable=False)
  email=db.Column(db.String(120),unique=True,nullable=False)
  password= db.Column(db.String(200),nullable=False)
  is_admin= db.Column(db.Boolean,default=False)