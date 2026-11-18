import random
from database import db
from models.user_model import User
from models.product_model import Product
from models.order_model import Command, LigneCommande


def seed_orders():
    # Optionnel : décommente la ligne suivante si tu veux vider les anciennes commandes avant de relancer le seed
    # Command.query.delete()
    # db.session.commit()

    if Command.query.first():
        print("⚠️ Des commandes existent déjà en base de données.")
        return

    print("📦 Insertion massive de commandes de test...")

    # Récupérer les clients et les produits
    clients = User.query.filter_by(role='client').all()
    if not clients:
        clients = User.query.all() # Fallback si les rôles ne sont pas stricts

    produits = Product.query.all()

    if not clients:
        print("❌ Erreur : Aucun client trouvé. Veuillez exécuter le seed des utilisateurs d'abord.")
        return

    if not produits:
        print("❌ Erreur : Aucun produit trouvé. Veuillez exécuter le seed des produits d'abord.")
        return

    adresses = [
        "123 Avenue des Champs-Élysées, 75008 Paris",
        "45 Rue de la République, 69002 Lyon",
        "12 Boulevard Victor Hugo, 06000 Nice",
        "8 Place de la Comédie, 34000 Montpellier",
        "56 Rue Paradis, 13006 Marseille",
        "9 Rue de la Paix, 75002 Paris",
        "14 Quai des Belges, 13001 Marseille",
        "77 Rue Saint-Ferréol, 13001 Marseille"
    ]

    statuts_possibles = ["en_attente", "validée", "expédiée", "annulée"]

    # Créer par exemple 8 à 10 commandes variées
    nombre_commandes = 8

    for _ in range(nombre_commandes):
        client = random.choice(clients)
        adresse = random.choice(adresses)
        statut = random.choice(statuts_possibles)

        nouvelle_commande = Command(
            utilisateur_id=client.id,
            adresse_livraison=adresse,
            statut=statut
        )
        db.session.add(nouvelle_commande)
        db.session.flush() # Permet d'obtenir l'ID de la commande généré avant le commit

        # Choisir entre 1 et 3 produits aléatoires pour cette commande
        nb_produits_dans_panier = random.randint(1, min(3, len(produits)))
        produits_selectionnes = random.sample(produits, nb_produits_dans_panier)

        for produit in produits_selectionnes:
            quantite = random.randint(1, 3) # Quantité entre 1 et 3
            ligne = LigneCommande(
                commande_id=nouvelle_commande.id,
                produit_id=produit.id,
                quantite=quantite,
                prix_unitaire=produit.prix
            )
            db.session.add(ligne)

    db.session.commit()
    print(f"✅ {nombre_commandes} commandes avec leurs lignes de commande ont été insérées avec succès !")

if __name__ == "__main__":
    from app import app
    with app.app_context():
        seed_orders()