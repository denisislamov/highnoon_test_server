from flask import Flask, request, jsonify
from models import db, User
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    if not data or "name" not in data or "telegram_id" not in data:
        return jsonify({"error": "Missing 'name' or 'telegram_id'"}), 400

    user = User(
        name=data["name"],
        telegram_id=data["telegram_id"],
        status=data.get("status", "offline")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "id": user.id,
        "name": user.name,
        "telegram_id": user.telegram_id,
        "status": user.status,
        "invited_by_user_id": user.invited_by_user_id
    }), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    status = data.get("status")
    invited_by_id = data.get("invited_by_user_id")

    if not status:
        return jsonify({"error": "Missing 'status'"}), 400

    user.status = status

    if status == "invited":
        if not invited_by_id:
            return jsonify({"error": "Missing 'invited_by_user_id' for status 'invited'"}), 400
        user.invited_by_user_id = invited_by_id
    else:
        user.invited_by_user_id = None

    db.session.commit()

    return jsonify({
        "id": user.id,
        "name": user.name,
        "telegram_id": user.telegram_id,
        "status": user.status,
        "invited_by_user_id": user.invited_by_user_id
    })

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([
        {
            "id": u.id,
            "name": u.name,
            "telegram_id": u.telegram_id,
            "status": u.status,
            "invited_by_user_id": u.invited_by_user_id
        }
        for u in users
    ])

if __name__ == "__main__":
    app.run(debug=True)