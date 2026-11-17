from models.user_model import User
from services.user_service import UserService

def seed_users():
    if User.query.first():
        print("⚠️ Les utilisateurs existent déjà.")
        return

    print("👤 Insertion des utilisateurs...")

    UserService.create_user({
        "nom": "Sophie Martin",
        "email": "sophie@example.com",
        "mot_de_passe": "password123",
        "role": "client"
    })

    UserService.create_user({
        "nom": "Lucas Bernard",
        "email": "lucas@example.com",
        "mot_de_passe": "password123",
        "role": "client"
    })

    UserService.create_user({
        "nom": "Admin Principal",
        "email": "admin@digimarket.com",
        "mot_de_passe": "adminsecure123",
        "role": "admin"
    })

    UserService.create_user({
        "nom": "Claire Admin",
        "email": "claire.admin@digimarket.com",
        "mot_de_passe": "adminsecure456",
        "role": "admin"
    })

    print("✅ 2 clients et 2 administrateurs ajoutés avec succès.")