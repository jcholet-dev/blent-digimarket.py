from models.product_model import Product
from flask import session

class CartService:
    @staticmethod
    def _get_raw_cart():
        if 'cart' not in session:
            session['cart'] = {}
        return session['cart']

    @classmethod
    def add_product(cls, produit_id, quantite=1):
        cart = cls._get_raw_cart()
        produit_id_str = str(produit_id)

        if produit_id_str in cart:
            cart[produit_id_str] += int(quantite)
        else:
            cart[produit_id_str] = int(quantite)

        session['cart'] = cart
        session.modified = True

    @classmethod
    def remove_product(cls, produit_id):
        cart = cls._get_raw_cart()
        produit_id_str = str(produit_id)

        if produit_id_str in cart:
            del cart[produit_id_str]
            session['cart'] = cart
            session.modified = True

    @classmethod
    def update_quantity(cls, produit_id, quantite):
        cart = cls._get_raw_cart()
        produit_id_str = str(produit_id)
        quantite = int(quantite)

        if produit_id_str in cart:
            if quantite > 0:
                cart[produit_id_str] = quantite
            else:
                del cart[produit_id_str]
            session['cart'] = cart
            session.modified = True

    @classmethod
    def get_cart_item_count(cls):
        cart = cls._get_raw_cart()
        return len(cart)

    @classmethod
    def get_cart_details(cls):
        cart = cls._get_raw_cart()
        detailed_items = []
        total_general = 0.0

        for produit_id, quantite in cart.items():
            produit = Product.query.get(int(produit_id))
            if produit:
                sous_total = produit.prix * quantite
                total_general += sous_total
                detailed_items.append({
                    "produit": produit.to_dict(),
                    "quantite": quantite,
                    "sous_total": sous_total
                })

        return {
            "articles": detailed_items,
            "total_general": total_general
        }

    @classmethod
    def clear_cart(cls):
        session['cart'] = {}
        session.modified = True