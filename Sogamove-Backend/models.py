from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class TravelHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_location = db.Column(db.String(100), nullable=False)
    end_location = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'start_location': self.start_location,
            'end_location': self.end_location,
            'timestamp': self.timestamp.isoformat()
        }

class User(db.Model):
    __bind_key__ = 'postgres'  # Esto vincula este modelo a PostgreSQL
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String(20), nullable=False)
    number_Id = db.Column(db.String(20), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    expedition_date = db.Column(db.Date, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    # Relación con la tabla Comment
    comments = db.relationship('Comment', backref='user', lazy=True)

class Comment(db.Model):
    __bind_key__ = 'postgres'  # Aseguramos que esté vinculada correctamente
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_Id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    username = db.Column(db.String(100), nullable=False)  # Guarda el nombre del usuario
    content = db.Column(db.Text, nullable=False)  # Contenido del comentario
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # Marca de tiempo

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
