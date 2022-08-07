from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from application import db
from application.models import User, EggPost
from application.users.forms import RegistationForm, LoginForm, UpdateUserForm
from application.users.picture_handler import add_profile_pic
from werkzeug.security import generate_password_hash,check_password_hash

users = Blueprint('users', __name__)


#Regiser
@users.route("/register", methods = ['GET','POST'])
def register():
    form = RegistationForm()

    if form.validate_on_submit():
        user = User(email = form.email.data,
                    username = form.username.data,
                    password=form.password.data,
                    first_name = form.first_name.data,
                    last_name = form.last_name.data,
                    phone = form.phone.data)
        db.session.add(user)
        db.session.commit()
        flash("Thanks for registration!")
        return redirect(url_for("users.login"))

    return render_template('register.html', form = form)

#Login
@users.route('/login', methods= ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Log in Success!')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('core.info')

            return redirect(next)

        return render_template('login.html', form = form)
    return render_template('login.html', form = form)

#Logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.info"))

#Account (update)
@users.route('/account', methods = ['GET','POST'])
@login_required
def account():

    form = UpdateUserForm()
    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.phone = form.phone.data

        db.session.commit()
        flash("user account updated")
        return redirect(url_for("users.account"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.phone.data = current_user.phone
        form.email.data = current_user.email

    profile_image = "application/static/profile_pics/"+current_user.profile_image
    return render_template("account.html", profile_image = profile_image, form = form)

#User list of collecting eggs
@users.route('/<username>')
def user_posts(username):
    page = request.args.get('page',1,type=int)
    user = User.query.filter_by(username = username).first_or_404()
    egg_posts = EggPost.query.filter_by(collector = user).order_by(EggPost.date.desc()).paginate(page=page, per_page = 10)
    return render_template('user_egg_posts.html', egg_posts = egg_posts, user= user)
