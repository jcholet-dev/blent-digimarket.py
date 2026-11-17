from app import app
from database import db
from seed_users import seed_users
from seed_products import seed_products

def init_database():
    with app.app_context():
        print("🚀 Démarrage de l'initialisation de la base de données...")

        # Création des tables
        db.create_all()
        print("🛠️ Tables créées avec succès.")

        # Insertion des données
        seed_users()
        seed_products()

        print("\n✨ Base de données initialisée avec succès !")

if __name__ == "__main__":
    init_database()