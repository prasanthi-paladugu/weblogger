from flask import request, session, g, redirect, url_for, abort, \
    render_template, flash, Flask
from flask_wtf import Form
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired
from flask.ext.sqlalchemy import SQLAlchemy

import os
# SQLAlchemy database configuration. Here we are using a local sqlite3
# database

# http://stackoverflow.com/questions/29397002/creating-database-with-sqlalchemy-in-flask

########################
# $ python
# from yourapplication import db 
# db.create_all()
########################



# Application Defintion
app = Flask(__name__)


# Database Configuration
db_path = os.path.join(os.path.dirname(__file__), 'app.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_ECHO'] = False

# Generate a random secret key
app.config['SECRET_KEY'] = os.urandom(24)


# Enable debugging
app.config['DEBUG'] = True

db = SQLAlchemy(app)


class Posts(db.Model):

    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))

    def __init__(self, title, description):
        self.title = title
        self.description = description

# Forms

class PostForm(Form):
    title = TextField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])


# Views / Controllers

@app.route('/')
def list_posts():
    """
    """
    posts = Posts.query.all()
    return render_template('index.html', posts=posts)


@app.route('/add', methods=['GET', 'POST'])
def create_post():
    """

    """
    post_form = PostForm(request.form)
    if request.method == 'POST':

        post = Posts(post_form.title.data, post_form.description.data)

        db.session.add(post)
        db.session.commit()
        return redirect(url_for('list_posts'))
    return render_template('post_form.html', post_form=post_form)


@app.route('/delete/<id>', methods=('GET', 'POST'))
def delete_post(id):
    """
    """
    post = Posts.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('list_posts'))


@app.route('/update/<id>', methods=('GET', 'POST'))
def update_post(id):
    """
    """
    post = Posts.query.get(id)
    post_form = PostForm(obj=post)

    if request.method == 'POST':
        post = Posts.query.get(id)
        post.title = post_form.title.data
        post.description = post_form.description.data
        db.session.commit()
        return redirect(url_for('list_posts'))

    return render_template('post_form.html', post_form=post_form)

# You can pass around port inside run

if __name__ == '__main__':
    app.run()
