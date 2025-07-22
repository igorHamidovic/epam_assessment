from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float)
    price = db.Column(db.Numeric, nullable=False)
