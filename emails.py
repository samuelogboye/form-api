from flask import current_app, render_template
from flask_mail import Message
import threading

def send_async_email(app, msg):
    with app.app_context():
        try:
            from app import mail
            mail.send(msg)
        except Exception as e:
            print(e)  # Handle the exception accordingly

def send_email(name, email, subject, template, template_data):
    try:
        with current_app.app_context():
            msg_title = subject
            sender = "noreply@app.com"
            msg = Message(msg_title, sender=sender, recipients=[email])
            msg.html = render_template(template, data=template_data)

            thr = threading.Thread(target=send_async_email, args=(current_app._get_current_object(), msg))
            thr.start()

            return {'msg': 'Email sent', 'status': "success"}, 201
    except Exception as e:
        return {'msg': 'Email not sent', 'error': str(e)}, 500
