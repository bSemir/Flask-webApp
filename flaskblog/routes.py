import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

posts = [
    {
        "author": "Semir Blekic",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "December 30, 2022",
    },
    {
        "author": "John Doe",
        "title": "Blog Post 2",
        "content": "Second post content",
        "date_posted": "December 29, 2022",
    },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # log in the user
            login_user(user, remember=form.remember.data)
            # if user tries to access some routes without being logged in
            # we have query parameter called next in the URL, that we can use to redirect users when they log in
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password!", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    # print(current_user)
    logout_user()
    return redirect(url_for("home"))


def save_picture(form_picture):
    # random_hex will be the base of our filename
    # we don't want to keep the name of the picture bc it might collide with other images in our folder,
    # so we randomize the name of image
    random_hex = secrets.token_hex(8)
    # we need to save pic with the same extension that is uploaded
    _, f_ext = os.path.splitext(form_picture.filename)
    # picture filename
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)
    # save in our directory
    form_picture.save(picture_path)
    # print(picture_fn)
    return picture_fn


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            # save it just like we did it with the username and email
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )
