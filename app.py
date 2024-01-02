from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from flask_cors import CORS

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Secret key
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587 # 465
app.config['MAIL_USE_TLS'] = True # False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Initialize Flask-Mail
mail = Mail(app)

# Routes
@app.route('/')
def index():
        return "This is a test"


@app.route('/test')
def test():
        return "Hello World!"

@app.route('/mail/', methods=['POST'])
def push_mail():
        admin_email = os.getenv('ADMIN_EMAIL')

        name = request.form['name']
        sender_msg_title = request.form['msg_title']
        email = request.form['email']
        msg_all = request.form['msg']
        if not name or not sender_msg_title or not msg_all or not email:
                return jsonify({'error': 'Missing data'}), 400

        msg_title = "Thanks for contacting us"
        sender = "noreply@app.com"
        msg = Message(msg_title,sender=sender,recipients=[email])
        msg_body = "We've received your message and will get back to you as soon as possible. You can also reply this email if you have any other question."
        msg.body = ""
        msg.reply_to = admin_email
        data = {
		'app_name': "Revpoint",
		'title': msg_title,
		'body': msg_body,
                'name': name
	}

        msg.html = render_template("email.html", data=data)

        try:
                mail.send(msg)

                 # Send a notification email to the admin
                admin_msg_title = "New Message Received"
                admin_msg = Message(admin_msg_title, sender=sender, recipients=[admin_email])
                admin_msg_body = f"New message received from {name} ({email})."
                admin_msg.body = admin_msg_body
                # Set the reply-to email address
                admin_msg.reply_to = email
                admin_data = {
                        'app_name': "Revpoint",
                        'title': admin_msg_title,
                        'body': admin_msg_body,
                        'name': name,
                        'message': msg_all,
                        'sender_title': sender_msg_title,
                }
                admin_msg.html = render_template("admin_email.html", data=admin_data)

                mail.send(admin_msg)  # Send the notification email to the admin

                return jsonify({'msg': 'Email sent', 'status': "success"}), 201
        except Exception as e:
                print(e)
                return jsonify({'msg': 'email not sent', 'error': str(e)}), 500



if __name__ == '__main__':
        app.run(debug=False, host='0.0.0.0')