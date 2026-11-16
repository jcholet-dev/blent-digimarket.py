from app import app
from models.user_model import db
from seed_user import seed_users
from seed_product import seed_products

def init_database():
    with app.app_context():
        print("🚀 Démarrage de l'initialisation de la base de données...")

        db.create_all()
        print("🛠️ Tables créées avec succès.")

        seed_users()
        seed_products()

        print("\n✨ Base de données initialisée avec succès !")

if __name__ == "__main__":
    init_database()