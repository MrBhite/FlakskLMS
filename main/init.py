import os, sys, random, string
from urllib.parse import unquote

from flask import Flask, render_template, request
from flask import jsonify
from ex import db
from modules.user import User
from modules.book import Book
from modules.BorrowList import BorrowList
from modules.message import Message
from service import userService
# from views.test import testBluePrint
from views.C2CBluePrint import *
from views.messageBluePrint import *
from views.libraryBluePrint import *
from views.userBluePrint import *


def createApp():
    app = Flask(__name__)
    app.secret_key = 'whatu149isilike'

    # 配置数据库设置
    DBconfig(app)

    # 配置路径及蓝图
    addRoute(app)
    return app


def addRoute(app):
    # 默认开始界面
    @app.route('/')
    def index():
        return render_template('test.html')
        pass

    @app.route('/Books/<int:times>', methods=['GET'])
    def allBooks(times):
        # 显示所有书籍信息，而不分是否是library系统还是C2C系统
        # 前端通过ajax传入简单字符串(times),后端返回json
        # times为计数器,将其转为int查看是第几次请求,(下将其int值计为n)
        # 从数据库中搜寻第n*10-n*10+9共十个book对象,作为List并打包为json传出
        books = bookService.getAllBooks(times, "sadmin")
        return jsonify(code=200, msg=books)

    @app.route('/Book/<string:searchKey>/<int:times>', methods=['GET'])
    def selectBook(searchKey, times):
        # 显示所有书籍信息，而不分是否是library系统还是C2C系统
        # 前端通过ajax传入json(含(searchKey)和(times)),后端返回json
        # 从数据库中搜索searchKey相关数据,将搜索到的book对象根据times作为List并打包为json传出
        books = bookService.searchBook(searchKey, times)
        return jsonify(code=200, msg=books)

    # 上传图片
    @app.route('/uploadImage', methods=['POST'])
    def upload():
        basedir = os.path.abspath(os.path.dirname(__file__))  # 当前文件所在路径
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
        img = request.files.get('image')
        img_name = ran_str + img.filename
        img.save(basedir + "/static/images/" + img_name)
        return jsonify(code=200, imagePath=f'/static/images/{img_name}')

    # 跳转到第一个参数对应的py文件查看蓝图(即路由)的详细信息;
    # url_prefix表示该蓝图内对应url的公共前缀
    app.register_blueprint(C2CBluePrint, url_prefix='/C2C')
    app.register_blueprint(messageBluePrint, url_prefix='/message')
    app.register_blueprint(libraryBluePrint, url_prefix='/library')
    app.register_blueprint(userBluePrint, url_prefix='/user')


def DBconfig(app):
    # 设置数据库连接地址
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Raymond:123456@127.0.0.1:3306/librarymanage'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.init_app(app)
    pass
