 # -*- coding: utf-8-*-

from flask import Flask, render_template
from flask import url_for
from faker import Faker
from flask_sqlalchemy import SQLAlchemy
import os, sys, click

dbType = 'sqlite'
WIN = sys.platform.startswith('win')
if WIN:
    prefix = dbType+':///'
else:
    prefix = dbType+':////'

app = Flask(__name__)

app.config['SQLALCHEMY_URI'] = prefix+os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # 初始化扩展，传入程序实例app

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

class User(db.Model):
    #创建表，名称为user，自动生成，小写处理
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))


fake = Faker()
name = fake.name()
movies = [
    {'title': 'My Neihbor Totoro', 'year': '1988'},
    {'title': 'Dead  Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]
for i in range(2):
    movies.append({'title': fake.name(), 'year': fake.year()})



@app.route('/')
def index_page():
    return render_template('index.html', name=name, movies=movies)


@app.route('/hello')
def hello_page():
    return u"<h1>欢迎Welcome</h1><img src=\"http://helloflask.com/totoro.gif\"> \
        <p><a href='/user/Alice'>URL中存放变量</a>: "\
        +url_for('user_page', name='Alice') \
        +"<p><a href="+url_for('user_page', name="White")+">White</a>"
        

@app.route('/user/<name>')
def user_page(name):
    return "User Page: "+name
