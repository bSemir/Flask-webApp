from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = ""
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)

# I'll separate this later
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship(
        "Post", backref="author", lazy=True
    )  # backref isn't the actual column in Post, but lets us access who is the user that created that post

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


if __name__ == "__main__":
    app.run(debug=True)


# some db stuff for later
# >>> app_ctx = app.app_context()
# >>> app_ctx.push()
# >>> db.create_all()
# >>> user_1 = User(username='Semir', email='email@email.com', password='password')
# >>> db.session.add(user_1)
# >>> db.session.commit()
# >>> u = User.query.all()
# >>> u
# [User('Semir', 'email@email.com', 'default.jpg')]
# >>> usr = User.query.filter_by(username='Semir').first()
# >>> usr
# User('Semir', 'email@email.com', 'default.jpg')
# >>> usr.id
# 1
# >>> usr.posts
# []


# testing the relationship
# >>> post_1 = Post(title='Blog 1', content='First Post yaay', user_id=usr.id)
# >>> post_2 = Post(title='Blog 2', content='Second Post yaay', user_id=usr.id)
# >>> db.session.add(post_1)
# >>> db.session.add(post_2)
# >>> db.session.commit()
# >>> usr.posts
# [Post('Blog 1', '2022-12-31 20:30:34.062233'), Post('Blog 2', '2022-12-31 20:30:34.062562')]

# >>> for post in usr.posts:
# ...     print(post.title)
# ...
# Blog 1
# Blog 2
# >>> post = Post.query.first()
# >>> post
# Post('Blog 1', '2022-12-31 20:30:34.062233')
# >>> post.user_id
# 1

# >>> post.author
# User('Semir', 'email@email.com', 'default.jpg')
