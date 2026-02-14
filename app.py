from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message
import os

# -------------------------
# APP CONFIG
# -------------------------
app = Flask(__name__)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# SQLite database inside instance folder (SAFE FOR HOSTINGER)
DB_PATH = os.path.join(BASE_DIR, 'instance', 'ecom_squire.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# -------------------------
# EMAIL CONFIG (HOSTINGER - FIXED)
# -------------------------
app.config.update(
    MAIL_SERVER='smtp.hostinger.com',  # Changed from gmail
    MAIL_PORT=465,                     # SSL Port
    MAIL_USE_SSL=True,                 # Hostinger prefers SSL for 465
    MAIL_USE_TLS=False,
    MAIL_USERNAME='Ypur Mail',
    MAIL_PASSWORD='You Mail Password' # Use your actual email password
)


mail = Mail(app)
db = SQLAlchemy(app)

# -------------------------
# DATABASE MODEL
# -------------------------
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

# Create DB if not exists
with app.app_context():
    db.create_all()

# -------------------------
# ROUTES
# -------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/forms/contact.php", methods=["POST"])
def contact_handler():
    name = request.form.get("name")
    email = request.form.get("email")
    subject = request.form.get("subject")
    message = request.form.get("message")

    try:
        # Save to DB
        new_entry = Contact(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(new_entry)
        db.session.commit()

        # Send Email
        msg = Message(
            subject=f"New Ecom Squire Lead: {subject}",
            sender=app.config['MAIL_USERNAME'],
            recipients=['growth@ecom-squire.com'],
            body=f"""
Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""
        )
        mail.send(msg)

        return "OK"

    except Exception as e:
        print("ERROR:", e)
        # This will show you the exact error in your browser
        return f"Error: {str(e)}", 500 


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    app.run()
