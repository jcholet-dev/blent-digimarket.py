# models/product_model.py
from datetime import datetime, timezone
from database import db

class Product(db.Model):
    __tablename__ = 'produit'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    categorie = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    quantite_stock = db.Column(db.Integer, nullable=False, default=0)
    date_creation = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "description": self.description,
            "categorie": self.categorie,
            "prix": self.prix,
            "quantite_stock": self.quantite_stock,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None
        }