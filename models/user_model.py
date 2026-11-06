from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Instance de SQLAlchemy (si tu l'initialises dans un autre fichier comme db.py, importe-la simplement ici)
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'utilisateur'  # Nom de la table dans digitmarket.db

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='client')  # 'client' ou 'admin'
    date_creation = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def set_password(self, password):
        """Hache le mot de passe et l'enregistre"""
        self.mot_de_passe = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie un mot de passe par rapport au hash stocké"""
        return check_password_hash(self.mot_de_passe, password)

    def to_dict(self):
        """Convertit l'objet en dictionnaire (pratique pour renvoyer du JSON dans l'API)"""
        return {
            "id": self.id,
            "email": self.email,
            "nom": self.nom,
            "role": self.role,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None
        }