import os
from threading import Thread
from flask import Flask, render_template, session, redirect, url_for
#redirect:重定向;reder_template:渲染模板;
from flask_script import Manager,Shell
#Flask-Script支持命令行选项,是一个Flask 扩展，为Flask 程序添加了一个命令行解析器
from flask_bootstrap import Bootstrap
#使用Flask-Bootstrap集成Twitter Bootstrap,Bootstrap是Twitter 开发的一个开源框架，它提供的用户界面组件可用于创建整洁且具有吸引力的网页，而且这些网页还能兼容所有现代Web 浏览器。
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_mail import Mail,Message

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)#程序实例
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER']='smtp.qq.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USERNAME']=os.environ.get('2269937513@qq.com')
app.config['MAIL_PASSWORD']=os.environ.get('ayarohilcrmnebeg')

app.config['FLASKY_MAIL_SUBJECT_PREFIX']=['Flasky']
app.config['FLASKY_MAIL_SENDER']='Flasky Admin <2269937513@qq.com>'
app.config['FLASKY_ADMIN']=os.environ.get('FLASKY_ADMIN')

manager = Manager(app)#Flask-Script 输出了一个名为Manager的类
bootstrap = Bootstrap(app)#Flask-Bootstrap 的初始化方法
moment = Moment(app)
db = SQLAlchemy(app)
migrate=Migrate(app,db)
mail=Mail (app)

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	users = db.relationship('User', backref='role', lazy='dynamic')

	def __repr__(self):
		return '<Role %r>' % self.name


class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' % self.username

def send_async_email(app,msg):
    with app.app_context():#在程序实例上调用app.app_context() 可获得一个程序上下文。
	        mail.send(msg)

def send_email(to,subject,template,**kwargs):
	msg=Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+ ' ' +subject,
				sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
	msg.body=render_template(template+'.txt',**kwargs)
	msg.html=render_template(template+'.html',**kwargs)#render_template 函数的第一个参数是模板的文件名。随后的参数都是键值对，表示模板中变量对应的真实值.
	thr = Thread(target=send_async_email,args=[app,msg])
	thr.start()
	return thr

class NameForm(FlaskForm):
	name = StringField('What is your name?', validators=[Required()])
	submit = SubmitField('Submit')

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command("shell",Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

@app.errorhandler(404)#客户端请求未知页面或路由时显示400
def page_not_found(e):
	return render_template('404.html'), 404


@app.errorhandler(500)#有未处理的异常时显示500
def internal_server_error(e):
	return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])#路由
def index():#视图函数
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		if user is None:
			user=User(username=form.name.data)
			db.session.add(user)
			session['known']=False
			if app.config['FLASKY_ADMIN']:
				send_email(app.config['FLASKY_ADMIN'],'New User',
							'mail/new_user',user=user)
		else:
			session['known']=True
		session['name']=form.name.data
		return redirect(url_for('index'))#由于使用频繁，Flask 提供了redirect() 辅助函数，用于生成这种重定向响应:这种响应没有页面文档，只告诉浏览器一个新地址用以加载新页面。重定向经常在Web表单中使用.
	return render_template('index.html',
		form=form,name=session.get('name'),
		known=session.get('known',False))


if __name__ == '__main__': #启动服务器
	manager.run()#服务器由manager.run()启动,启动后就能解析命令行了。
