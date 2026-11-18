from database import db
from datetime import datetime, timezone

class Command(db.Model):
    __tablename__ = 'commande'

    id = db.Column(db.Integer, primary_key=True)

    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'), nullable=False)
    date_commande = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    adresse_livraison = db.Column(db.String(255), nullable=False)
    statut = db.Column(db.String(50), nullable=False, default='en_attente')
    lignes = db.relationship('LigneCommande', backref='commande_associee', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            "id": self.id,
            "utilisateur_id": self.utilisateur_id,
            "date_commande": self.date_commande.isoformat() if self.date_commande else None,
            "adresse_livraison": self.adresse_livraison,
            "statut": self.statut,
            "lignes": [ligne.to_dict() for ligne in self.lignes]
        }


class LigneCommande(db.Model):
    __tablename__ = 'ligne_commande'

    id = db.Column(db.Integer, primary_key=True)
    commande_id = db.Column(db.Integer, db.ForeignKey('commande.id'), nullable=False)
    produit_id = db.Column(db.Integer, db.ForeignKey('produit.id'), nullable=False)
    quantite = db.Column(db.Integer, nullable=False, default=1)
    prix_unitaire = db.Column(db.Float, nullable=False)
    produit_associe = db.relationship('Product', backref='lignes_commande', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "commande_id": self.commande_id,
            "produit_id": self.produit_id,
            "quantite": self.quantite,
            "prix_unitaire": self.prix_unitaire,
            "produit": self.produit_associe.to_dict() if self.produit_associe else None
        }