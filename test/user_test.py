import pytest
from models.user_model import User, db

def test_create_user(app):
    with app.app_context():
        data = {
            "nom": "Alice Dupont",
            "email": "alice@example.com",
            "mot_de_passe": "secret123"
        }

        user = User.create_user(data)

        assert user.id is not None
        assert user.nom == "Alice Dupont"
        assert user.email == "alice@example.com"
        assert user.role == "client"
        assert user.mot_de_passe != "secret123"


def test_password_hashing(app):
    with app.app_context():
        user = User(nom="Bob", email="bob@example.com")
        user.set_password("mon_super_mdp")
        assert user.mot_de_passe != "mon_super_mdp"
        assert user.check_password("mon_super_mdp") is True
        assert user.check_password("mauvais_mdp") is False


def test_user_to_dict(app):
    with app.app_context():
        user = User(nom="Charlie", email="charlie@example.com", role="admin")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        user_dict = user.to_dict()
        assert user_dict["nom"] == "Charlie"
        assert user_dict["email"] == "charlie@example.com"
        assert user_dict["role"] == "admin"
        assert "mot_de_passe" not in user_dict