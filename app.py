from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # Replace this with logic to fetch all messages from the database
        messages = Message.query.all()
        return jsonify(messages), 200

    elif request.method == 'POST':
        data = request.get_json()
        body = data.get('body')
        username = data.get('username')

        # Create a new message and add it to the database
        new_message = Message(body=body, username=username)
        db.session.add(new_message)
        db.session.commit()

        return jsonify(new_message), 201

@app.route('/messages/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def messages_by_id(id):
    message = Message.query.get(id)

    if not message:
        return jsonify({'message': 'Message not found'}), 404

    if request.method == 'GET':
        return jsonify(message), 200

    elif request.method == 'PUT':
        data = request.get_json()
        body = data.get('body')
        username = data.get('username')

        # Update the message attributes and commit to the database
        message.body = body
        message.username = username
        db.session.commit()

        return jsonify(message), 200

    elif request.method == 'DELETE':
        # Delete the message from the database
        db.session.delete(message)
        db.session.commit()

        return jsonify({'message': 'Message deleted'}), 200

if __name__ == '__main__':
    app.run(port=5555)
