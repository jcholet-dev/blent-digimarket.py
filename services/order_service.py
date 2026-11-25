from models.order_model import Command, LigneCommande
from models.product_model import Product
from database import db
from services.cart_service import CartService
from flask_jwt_extended import get_jwt_identity


class OrderService:
    @classmethod
    def create_order(cls, data, adresse_livraison_texte):
        # 1. Récupérer l'ID utilisateur depuis le JWT
        current_identity = get_jwt_identity()
        if not current_identity:
            raise ValueError("Utilisateur non authentifié.")
        utilisateur_id = int(current_identity)

        # 2. Récupérer les articles : soit envoyés dans le JSON (data), soit depuis le CartService
        articles_data = data.get("articles")

        if not articles_data:
            # Si aucun article n'est dans la requête, on essaie de les récupérer depuis le panier de la session/service
            cart_data = CartService.get_cart_details() if hasattr(CartService, 'get_cart_details') else None
            articles_data = cart_data.get("articles", []) if cart_data else []

        if not articles_data:
            raise ValueError("Le panier est vide.")

        try:
            # 3. Création de la commande principale
            new_command = Command(
                utilisateur_id=utilisateur_id,
                adresse_livraison=adresse_livraison_texte,
                statut="en_attente"
            )
            db.session.add(new_command)
            db.session.flush()

            # 4. Ajout des lignes de commande
            for item in articles_data:
                # Gestion flexible de la structure des articles (dict ou ID direct)
                if isinstance(item, int):
                    produit_id = item
                    quantite = 1
                    produit_obj = db.session.get(Product, produit_id)
                    prix_unitaire = produit_obj.prix if produit_obj else 0.0
                elif isinstance(item, dict):
                    produit_info = item.get("produit")
                    if isinstance(produit_info, dict):
                        produit_id = produit_info.get("id")
                        prix_unitaire = produit_info.get("prix", 0.0)
                    else:
                        produit_id = item.get("produit_id") or item.get("produit")
                        prix_unitaire = item.get("prix_unitaire", 0.0)

                        # Si le prix est manquant, on le récupère en BDD
                        if not prix_unitaire and produit_id:
                            p_obj = db.session.get(Product, produit_id)
                            prix_unitaire = p_obj.prix if p_obj else 0.0

                    quantite = item.get("quantite", 1)
                else:
                    continue

                if not produit_id:
                    raise ValueError("Identifiant de produit invalide dans le panier.")

                ligne = LigneCommande(
                    commande_id=new_command.id,
                    produit_id=produit_id,
                    quantite=quantite,
                    prix_unitaire=prix_unitaire
                )
                db.session.add(ligne)

            db.session.commit()

            # 5. Vider le panier après validation réussie
            if hasattr(CartService, 'clear_cart'):
                CartService.clear_cart()

            return new_command.id

        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def get_user_orders(cls, user_id):
        return Command.query.filter_by(utilisateur_id=user_id).order_by(Command.date_commande.desc()).all()