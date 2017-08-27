from flask_mail import Message
from hello import mail
msg=Message('test subject',sender='2269937513@qq.com',recipients=['2269937513@qq.com'])
msg.body='text body'  
msg.html='<b>HTML</b> body'   
app_ctx=app.app_context()
app_ctx.push()
with app_ctx():
with app.app_context():

