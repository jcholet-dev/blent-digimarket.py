from models.product_model import Product  # Nécessaire pour vérifier si la table contient déjà des données
from services.product_service import ProductService

def seed_products():
    # Vérification si des produits existent déjà
    if Product.query.first():
        print("⚠️ Les produits existent déjà.")
        return

    print("📦 Insertion des produits...")
    products_data = [
        {
            "nom": "Casque Audio Sans Fil",
            "description": "Casque Bluetooth à réduction de bruit active.",
            "categorie": "Électronique",
            "prix": 79.99,
            "quantite_stock": 24
        },
        {
            "nom": "Clavier Mécanique RGB",
            "description": "Clavier de gaming rétroéclairé.",
            "categorie": "Accessoires",
            "prix": 45.50,
            "quantite_stock": 12
        },
        {
            "nom": "Chaise de Bureau Ergonomique",
            "description": "Chaise réglable en hauteur.",
            "categorie": "Mobilier",
            "prix": 149.00,
            "quantite_stock": 3
        },
        {
            "nom": "Écran 27 pouces 4K",
            "description": "Moniteur UHD IPS.",
            "categorie": "Électronique",
            "prix": 299.99,
            "quantite_stock": 7
        }
    ]

    # Utilisation du service pour créer chaque produit
    for data in products_data:
        ProductService.create_product(data)

    print("✅ Produits de test ajoutés avec succès.")
