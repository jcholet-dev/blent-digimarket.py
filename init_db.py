from app import app
from database import db
from seed.seed_users import seed_users
from seed.seed_products import seed_products
from seed.seed_orders import seed_orders

def init_database():
    with app.app_context():
        print("🚀 Démarrage de l'initialisation de la base de données...")

        db.drop_all()
        db.create_all()
        print("🛠️ Tables réinitialisées avec succès.")

        seed_users()
        seed_products()
        seed_orders()

        print("\n✨ Base de données initialisée avec succès !")

if __name__ == "__main__":
    init_database()