from flask import Flask, request, jsonify
from models import db, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/users", methods=["POST"])
def add_user():
    data = request.json
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name'"}), 400
    user = User(name=data["name"], status=data.get("status", "inactive"))
    db.session.add(user)
    db.session.commit()
    return jsonify({"id": user.id, "name": user.name, "status": user.status}), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_status(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    if "status" not in data:
        return jsonify({"error": "Missing 'status'"}), 400

    user.status = data["status"]
    db.session.commit()

    return jsonify({"id": user.id, "name": user.name, "status": user.status})

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "name": u.name, "status": u.status}
        for u in users
    ])

if __name__ == "__main__":
    app.run(debug=True)
