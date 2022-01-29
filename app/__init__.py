# file name: __init__.py
# pwd: /project_name/app/__init__.py
from flask import Flask
from app.module.mail import mail_info
from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = mail_info['MAIL_SERVER']
app.config['MAIL_PORT'] = mail_info['MAIL_PORT']
app.config['MAIL_USERNAME'] = mail_info['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = mail_info['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# 파일 이름이 index.py 이므로
from app.main.index import main as main

# 위에서 추가한 파일을 연동해주는 역할
app.register_blueprint(main) # as main으로 설정해주었으므로

@app.route("/email", methods=['post', 'get'])
def email_test():
    if request.method == 'POST':
        senders = "noreply"
        receiver = request.form['email_receiver']
        content = request.form['email_content']
        receiver = receiver.split(',')
       
        for i in range(len(receiver)):
            receiver[i] = receiver[i].strip()
        print(receiver)
        result = send_email(senders, receiver, content)
        if not result:
            return render_template('/main/email.html', content="Email is sent")
        else:
            return render_template('/main/email.html', content="Email is not sent")
    else:
        return render_template('/main/email.html')
   
def send_email(senders, receiver, content):
    try:
        mail = Mail(app)
        msg = Message('SWDR시스템 자동메일', sender = senders, recipients = receiver)
        msg.body = content
        mail.send(msg)
    except Exception:
        pass
    finally:
        pass