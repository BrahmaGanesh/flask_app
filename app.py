from flask import Flask, request, redirect,render_template,flash,session,url_for
from form import LoginForm,RegisterForm,UpdateForm
from werkzeug.security import generate_password_hash
from models import User
from run import db,app
from werkzeug.security import generate_password_hash, check_password_hash # ADDED check_password_hash



app=app
db=db

@app.route('/register', methods=["POST","GET"])
def register():
  form = RegisterForm()
  if form.validate_on_submit():
    hash_psw=generate_password_hash(form.password.data)
    user=User.query.filter_by(name=form.name.data).first()
    if user:
      flash("already exist","danger")
    else:
      user=User(name=form.name.data,email=form.email.data,password=hash_psw)
      db.session.add(user)
      db.session.commit()
      return redirect('/login')
  return render_template("register.html",form=form)


@app.route("/login",methods=["POST","GET"])
def login():
  form=LoginForm()
  if form.validate_on_submit():
    user=User.query.filter_by(email=form.email.data).first()
    if user and check_password_hash(user.password,form.password.data):
      session["user_id"]=user.id
      session["username"]=user.name
      flash("Login Successful","Success")
      if user.is_admin:
        return redirect("/admin")
      else:
        return redirect("/")
    else:
      flash("Invalid email or password","danger")
      redirect("/login")
  return render_template("login.html",form=form)



@app.route('/profile',methods=["POST",'GET'])
def profile():
  if 'user_id' not in session:
    flash('please Login first ',"warning")
    return redirect(url_for("login"))
  user = User.query.get(session["user_id"])
  form=UpdateForm(obj=user)

  if form.validate_on_submit():
    user.name=form.username.data
    user.email=form.email.data
    db.session.commit()
    flash("Profile updated successfully","success")
    session["username"]=user.name
    return redirect(url_for("home"))
  return render_template("update.html",form=form)

@app.route('/delete')
def delete():
  if 'user_id'not in session:
    flash("login required","warning")
    return redirect('/login')
  user=User.query.get(session["user_id"])
  db.session.delete(user)
  db.session.commit()
  session.clear()
  flash("your account was delete","info")
  return redirect('/register')


@app.route('/admin')
def admin():
  if 'user_id' not in session:
    flash("Login required","warning")
    return redirect("/login")
  user=User.query.get(session["user_id"])
  if not user.is_admin:
    flash("Access denied. Admins only","danger")
    return redirect('/')
  users=User.query.all()
  return render_template("admin.html",users=users)

@app.route('/admin/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    admin = User.query.get(session['user_id'])
    if not admin.is_admin:
        return redirect(url_for('home'))

    user = User.query.get_or_404(user_id)
    form = UpdateForm(obj=user)

    if form.validate_on_submit():
        user.name = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('User updated!', 'success')
        return redirect(url_for('admin'))

    return render_template('update.html', form=form)

@app.route('/admin/delete/<int:user_id>')
def delete_user(user_id):
    admin = User.query.get(session['user_id'])
    if not admin.is_admin:
        return redirect(url_for('home'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted!', 'info')
    return redirect(url_for('admin'))

@app.route("/")
def home():
  if 'user_id' not in session:
    flash("please Login first","warning")
    return redirect('/login')
  return render_template("home.html",username=session.get('username'))


@app.route('/logout')
def logout():
  session.clear()
  flash("Logout Successfully","info")
  return redirect("/login")
if __name__ == "__main__":
  app.run(debug=True)