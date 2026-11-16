from models.product_model import db, Product

def seed_products():
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

    for data in products_data:
        Product.createProduct(data)
    print("✅ Produits de test ajoutés.")