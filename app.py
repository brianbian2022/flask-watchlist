 # -*- coding: utf-8-*-

from flask import Flask, render_template
from flask import url_for
from faker import Faker
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os, sys, click

dbType = 'sqlite'
WIN = sys.platform.startswith('win')
if WIN:
    prefix = dbType+':///'
else:
    prefix = dbType+':////'

app = Flask(__name__)

def fake_data():
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
    return name,movies

# app.config['SQLALCHEMY_URI'] = prefix+os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix+os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_BINDS'] = {
    'users': prefix+os.path.join(app.root_path, 'data.db')
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # 初始化扩展，传入程序实例app
migrate = Migrate(app, db)
# 数据迁移工具
# 执行;
# flask db init 将创建migrations目录
# flask db migrate
# More info check https://github.com/miguelgrinberg/Flask-Migrate

# 创建数据库模型
class User(db.Model):
    #创建表，名称为user，自动生成，小写处理
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

# class的名字将会是表的名字，表的名字将为小写
class Movie(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))

''' 完成后执行以下命令可以创建数据库
    # flask shell
    # from app import db
    # db.create_all()
    # db.drop_all() 
    # from app import User, Movie
    # user = User(name="Tom Hanks")
    # m1 = Movie(title='Leon', year='1994')
    # db.session.add(user)
    # db.session.add(m1)
    # db.session.commit()
    # movie = Movie.query.first() # 获取 Movie 模型的第一个记录(返回模型类实例)
    # movie.title
    # Movie.query.all()
    # Movie.query.count() 
    # Movie.query.filter_by(title='Mahjong').first() # 获取 title 字段值为 Mahjong 的记录
    # db.session.delete(movie) # 使用 db.session.delete() 方法删除记录,传入模型实例
'''

@app.cli.command()
@click.option('--drop', is_flag=True, help="Drop original database")
@click.option('--fake', is_flag=True, help="Fake test datas")
def initdb(drop, fake):
    ''' 
功能说明：自定义flask命令进行数据库初始化操作
使用方法：\r\n 
【1】flask initdb
【2】flask initdb --drop
'''
    if drop:
        db.drop_all()
        click.echo("删除数据库。")
    db.create_all()
    click.echo("初始化数据库。")
    if fake:
        click.echo("填充数据库")
        name,movies = fake_data()
        user = User(name=name)
        db.session.add(user)
        for m in movies:
            print(m)
            db.session.add(Movie(title=m['title'], year=m['year']))
        db.session.commit() 

@app.route('/')
def index_page():
    user = User.query.first()
    movies = Movie.query.all()
    #name = user.name
    #return render_template('index.html', name=name, movies=movies)
    return render_template('index.html', user=user, movies=movies)


@app.route('/hello')
def hello_page():
    return u"<h1>欢迎Welcome</h1><img src=\"http://helloflask.com/totoro.gif\"> \
        <p><a href='/user/Alice'>URL中存放变量</a>: "\
        +url_for('user_page', name='Alice') \
        +"<p><a href="+url_for('user_page', name="White")+">White</a>"
        

@app.route('/user/<name>')
def user_page(name):
    return "User Page: "+name


@app.errorhandler(404)
def page_404(error):
    user = User.query.first()
    return render_template('404.html', user=user), 404