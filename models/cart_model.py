from models.product_model import Product

class Cart:
    def __init__(self, session_cart=None):
        self.items = session_cart if session_cart is not None else {}

    def add_product(self, produit_id, quantite=1):
        produit_id_str = str(produit_id)
        if produit_id_str in self.items:
            self.items[produit_id_str] += quantite
        else:
            self.items[produit_id_str] = quantite

    def remove_product(self, produit_id):
        produit_id_str = str(produit_id)
        if produit_id_str in self.items:
            del self.items[produit_id_str]

    def get_details(self):
        detailed_items = []
        total_general = 0.0

        for produit_id, quantite in self.items.items():
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