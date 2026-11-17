# services/user_service.py
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from models.user_model import User

class UserService:

    @staticmethod
    def create_user(data):
        hashed_password = generate_password_hash(data.get('mot_de_passe'))

        new_user = User(
            email=data.get('email'),
            nom=data.get('nom'),
            mot_de_passe=hashed_password,
            role=data.get('role', 'client'),
            date_creation=datetime.now(timezone.utc)
        )

        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user.mot_de_passe, password)