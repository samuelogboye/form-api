from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

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

# # Model
# class Contact(db.Model):
#         id = db.Column(db.Integer, primary_key=True)
#         name = db.Column(db.String(100))
#         email = db.Column(db.String(100))
#         msg_title = db.Column(db.String(100))
#         msg = db.Column(db.String(100))

#         def __init__(self, msg_title, msg, name, email):
#                 self.name = name
#                 self.email = email
#                 self.msg_title = msg_title
#                 self.msg = msg

#         def __repr__(self):
#                 return '<Contact %r>' % self.name

#         def serialize(self):
#                 return {
#                         'id': self.id,
#                         'name': self.name,
#                         'email': self.email,
#                         'msg_title': self.msg_title,
#                         'msg': self.msg
#                 }

# # Use the app context to create the Contact table
# with app.app_context():
#     db.create_all()


# Routes
@app.route('/')
def index():
        return "This is a test"


@app.route('/test')
def test():
        return "Hello World!"

@app.route('/mail/', methods=['POST'])
def push_mail():
        name = request.form['name']
        msg_title = request.form['msg_title']
        email = request.form['email']
        msg_all = request.form['msg']
        if not name or not msg_title or not msg_all or not email:
                return jsonify({'error': 'Missing data'}), 400

        msg_title = "Thanks for contacting us"
        sender = "noreply@app.com"
        msg = Message(msg_title,sender=sender,recipients=[email])
        msg_body = "We've received your message and will get back to you as soon as possible"
        msg.body = ""
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
                admin_email = os.getenv('ADMIN_EMAIL')
                admin_msg_title = "New Message Received"
                admin_msg = Message(admin_msg_title, sender=sender, recipients=[admin_email])
                admin_msg_body = f"New message received from {name} ({email})."
                admin_msg.body = admin_msg_body
                admin_data = {
                        'app_name': "Revpoint",
                        'title': admin_msg_title,
                        'body': admin_msg_body,
                        'name': name,
                        'message': msg_all
                }
                admin_msg.html = render_template("admin_email.html", data=admin_data)

                mail.send(admin_msg)  # Send the notification email to the admin

                return jsonify({'msg': 'Email sent', 'status': "success"}), 201
        except Exception as e:
                print(e)
                return jsonify({'msg': 'email not sent', 'error': str(e)}), 500



if __name__ == '__main__':
        app.run(debug=False, host='0.0.0.0')