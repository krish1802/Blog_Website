from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Setting up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/data.db'
db = SQLAlchemy(app)


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(30))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

# Setting up routes
@app.route('/')
def index():
    posts = Blogpost.query.all()
    return render_template('index.html', posts=posts)

@app.route('/index')
def home_page():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    date_posted = post.date_posted.strftime('%B %d, %Y')
    return render_template('post.html', post=post, date_posted=date_posted)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

# Actual Program to run
if __name__ == '__main__':
    app.run(debug=True)
