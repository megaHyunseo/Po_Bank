from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class IDCard(db.Model):
    registration_number = db.Column(db.String(50), primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
