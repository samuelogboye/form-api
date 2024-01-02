from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os
from flask_cors import CORS
from emails import send_email

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

    mandatory_keys = ['name', 'msg_title', 'email', 'msg']


    data = request.get_json()

    missing_fields = [key for key in mandatory_keys if key not in data]

    if missing_fields:
        return jsonify({'message': 'Missing fields: ' + ', '.join(missing_fields)}), 400

    name = data['name']
    sender_msg_title = data['msg_title']
    email = data['email']
    msg_all = data['msg']



    try:
        # Sending email to the user
        user_template_data = {
            'app_name': "Revpoint",
            'title': "Thanks for contacting us",
            'body': "We've received your message and will get back to you as soon as possible. You can also reply to this email if you have any other questions.",
            'name': name
        }

        send_email(name, email, "Thanks for contacting us", "email.html", user_template_data)

        # Sending notification email to the admin
        admin_template_data = {
            'app_name': "Revpoint",
            'title': "New Message Received",
            'body': f"New message received from {name} ({email}).",
            'name': name,
            'message': msg_all,
            'sender_title': sender_msg_title,
        }

        send_email(name, admin_email, "New Message Received", "admin_email.html", admin_template_data)

        return jsonify({'msg': 'Email sent', 'status': "success"}), 201
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Email not sent', 'error': str(e)}), 500




if __name__ == '__main__':
        app.run(debug=False, host='0.0.0.0')