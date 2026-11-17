from services.user_service import UserService

def test_create_user(app):
    with app.app_context():
        data = {
            "nom": "Alice Dupont",
            "email": "alice@example.com",
            "mot_de_passe": "secret123"
        }

        user = UserService.create_user(data)

        assert user.id is not None
        assert user.nom == "Alice Dupont"
        assert user.email == "alice@example.com"
        assert user.role == "client"
        assert user.mot_de_passe != "secret123"

def test_password_verification(app):
    with app.app_context():
        data = {
            "nom": "Bob",
            "email": "bob@example.com",
            "mot_de_passe": "mon_super_mdp"
        }

        user = UserService.create_user(data)

        assert user.mot_de_passe != "mon_super_mdp"
        assert UserService.verify_password(user, "mon_super_mdp") is True
        assert UserService.verify_password(user, "mauvais_mdp") is False

def test_user_to_dict(app):
    with app.app_context():
        data = {
            "nom": "Charlie",
            "email": "charlie@example.com",
            "mot_de_passe": "password123",
            "role": "admin"
        }

        user = UserService.create_user(data)

        user_dict = user.to_dict()
        assert user_dict["nom"] == "Charlie"
        assert user_dict["email"] == "charlie@example.com"
        assert user_dict["role"] == "admin"
        assert "mot_de_passe" not in user_dict