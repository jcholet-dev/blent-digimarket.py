# Controller de la gestion utilisateur : enregistrement, authentification et profil sécurisé par JWT
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from services.user_service import UserService

user_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('mot_de_passe') or not data.get('nom'):
        return jsonify({"erreur": "Veuillez fournir un email, un mot de passe et un nom"}), 400

    if UserService.get_by_email(data['email']):
        return jsonify({"erreur": "Cet email est déjà utilisé"}), 409

    new_user = UserService.create_user(data)

    return jsonify({
        "message": "Utilisateur créé avec succès",
        "utilisateur": new_user.to_dict()
    }), 201


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('mot_de_passe'):
        return jsonify({"erreur": "Email et mot de passe requis"}), 400

    user = UserService.get_by_email(data['email'])

    if not user or not UserService.verify_password(user, data['mot_de_passe']):
        return jsonify({"erreur": "Email ou mot de passe incorrect"}), 401

    # Création du token JWT avec l'ID utilisateur en identifiant et le rôle en claims additionnels
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    return jsonify({
        "message": "Connexion réussie",
        "access_token": access_token,
        "role": user.role
    }), 200


@user_bp.route('/profile', methods=['GET'])
@jwt_required()  # <-- JWT obligatoire pour accéder à cette route
def get_profile():
    # Récupération sécurisée de l'ID utilisateur stocké dans le token JWT
    current_user_id = get_jwt_identity()
    user = UserService.get_by_id(current_user_id)

    if not user:
        return jsonify({"erreur": "Utilisateur non trouvé"}), 404

    return jsonify({
        "utilisateur": user.to_dict()
    }), 200