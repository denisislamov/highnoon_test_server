from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    telegram_id = db.Column(db.BigInteger, unique=True, nullable=False)
    status = db.Column(db.String(32), nullable=False, default="offline")

    invited_by_user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    invited_by = db.relationship("User", remote_side=[id], uselist=False, post_update=True)