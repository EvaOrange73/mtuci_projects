from flask import render_template, request

from app import app

# user = {'username': "Eva"}
posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    },
    {
        'author': {'username': 'Василий'},
        'body': 'Привет!!'
    }
]


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', posts=posts, name="")


@app.route('/dict')
def dict():
    name = request.args.get("name")
    message = request.args.get("message")
    posts.append(
        {
            'author': {'username': name},
            'body': message
        }
    )
    return render_template('index.html', title='Home', posts=posts, name=name)
