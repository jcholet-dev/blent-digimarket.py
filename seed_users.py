from models.user_model import db, User

def seed_users():
    if User.query.first():
        print("⚠️ Les utilisateurs existent déjà.")
        return

    print("👤 Insertion des utilisateurs...")

    # Clients
    User.create_user({"nom": "Sophie Martin", "email": "sophie@example.com", "mot_de_passe": "password123"})
    User.create_user({"nom": "Lucas Bernard", "email": "lucas@example.com", "mot_de_passe": "password123"})

    # Admins
    admin1 = User(nom="Admin Principal", email="admin@digimarket.com", role="admin")
    admin1.set_password("adminsecure123")

    admin2 = User(nom="Claire Admin", email="claire.admin@digimarket.com", role="admin")
    admin2.set_password("adminsecure456")

    db.session.add_all([admin1, admin2])
    db.session.commit()
    print("✅ 2 clients et 2 administrateurs ajoutés.")