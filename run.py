from flaskblog import app

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
