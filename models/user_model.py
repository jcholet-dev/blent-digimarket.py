from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'utilisateur'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='client')
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        self.mot_de_passe = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.mot_de_passe, password)

    @classmethod
    def create_user(cls, data):
        new_user = cls(
            email=data.get('email'),
            nom=data.get('nom'),
            role='client',
            date_creation=datetime.now(timezone.utc)
        )
        new_user.set_password(data.get('mot_de_passe'))
        db.session.add(new_user)
        db.session.commit()
        return new_user



    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "nom": self.nom,
            "role": self.role,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None
        }