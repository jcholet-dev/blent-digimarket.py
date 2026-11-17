from database import db
from models.user_model import User
from models.product_model import Product
from models.order_model import Command, LigneCommande


def seed_orders():
    if Command.query.first():
        print("⚠️ Les commandes existent déjà.")
        return

    print("📦 Insertion des commandes de test...")
    client = User.query.filter_by(role='client').first()

    produits = Product.query.limit(2).all()

    if not client:
        print("❌ Erreur : Aucun client trouvé. Veuillez exécuter seed_users d'abord.")
        return

    if not produits:
        print("❌ Erreur : Aucun produit trouvé. Veuillez exécuter seed_products d'abord.")
        return

    nouvelle_commande = Command(
        utilisateur_id=client.id,
        adresse_livraison="123 Avenue des Champs-Élysées, 75008 Paris",
        statut="en_attente"
    )
    db.session.add(nouvelle_commande)
    db.session.commit()

    for produit in produits:
        ligne = LigneCommande(
            commande_id=nouvelle_commande.id,
            produit_id=produit.id,
            quantite=1,
            prix_unitaire=produit.prix
        )
        db.session.add(ligne)

    db.session.commit()
    print("✅ Commandes et lignes de commande insérées avec succès !")