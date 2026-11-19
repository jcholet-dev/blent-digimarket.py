from models.order_model import Command, LigneCommande
from database import db
from services.cart_service import CartService
from flask import session

class OrderService:
    @classmethod
    def create_order(cls, cart_data, adresse_livraison_texte):
        if not cart_data or not cart_data.get("articles"):
            raise ValueError("Le panier est vide.")
        utilisateur_id = session.get('user_id', 1)

        try:
            new_command = Command(
                utilisateur_id=utilisateur_id,
                adresse_livraison=adresse_livraison_texte,
                statut="en_attente"
            )
            db.session.add(new_command)
            db.session.flush()
            for item in cart_data["articles"]:
                ligne = LigneCommande(
                    commande_id=new_command.id,
                    produit_id=item["produit"]["id"],
                    quantite=item["quantite"],
                    prix_unitaire=item["produit"]["prix"]
                )
                db.session.add(ligne)

            db.session.commit()
            CartService.clear_cart()

            return new_command.id
        except Exception as e:
            db.session.rollback()
            raise e