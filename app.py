from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@db:5432/messages_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)

# Flag to ensure seeding only happens once
db_initialized = False

@app.before_request
def initialize_db_once():
    global db_initialized
    if not db_initialized:
        db.create_all()
        if not Message.query.first():
            messages = [
                "Today is your lucky day!",
                "Hard work pays off!",
                "Be kind to yourself and others.",
                "Success is around the corner.",
                "You are capable of amazing things!"
            ]
            for msg in messages:
                db.session.add(Message(text=msg))
            db.session.commit()
        db_initialized = True

# Route to get a random message
@app.route("/")
def get_random_message():
    messages = Message.query.all()
    if messages:
        random_message = random.choice(messages)
        return jsonify({"message": random_message.text})
    else:
        return jsonify({"error": "No messages found in the database."}), 404

# Health check endpoint
@app.route("/health")
def health_check():
    return jsonify({"status": "OK"}), 200

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")

