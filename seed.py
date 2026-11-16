from app import app
from models.user_model import db, User

def seed_database():
    with app.app_context():
        db.create_all()
        if User.query.first():
            print(" La base de données contient déjà des utilisateurs.")
            return

        print(" 🌱 Insertion des utilisateurs de test...")
        client1_data = {
            "nom": "Sophie Martin",
            "email": "sophie@example.com",
            "mot_de_passe": "password123"
        }
        client2_data = {
            "nom": "Lucas Bernard",
            "email": "lucas@example.com",
            "mot_de_passe": "password123"
        }

        User.create_user(client1_data)
        User.create_user(client2_data)

        admin1 = User(
            nom="Admin Principal",
            email="admin@digimarket.com",
            role="admin"
        )
        admin1.set_password("adminsecure123")

        admin2 = User(
            nom="Claire Admin",
            email="claire.admin@digimarket.com",
            role="admin"
        )
        admin2.set_password("adminsecure456")

        db.session.add_all([admin1, admin2])
        db.session.commit()

        print(" ✅ 2 clients et 2 administrateurs ont été créés avec succès !")

if __name__ == "__main__":
    seed_database()