#controller de la gestion utilisateur : enregistrement, authentification
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user_model import User

# Création du Blueprint
user_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validation des données
    if not data or not data.get('email') or not data.get('mot_de_passe') or not data.get('nom'):
        return jsonify({"erreur": "Veuillez fournir un email, un mot de passe et un nom"}), 400

    # Vérification si l'email existe déjà
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"erreur": "Cet email est déjà utilisé"}), 409

    # Création de l'utilisateur via le modèle
    new_user = User.create_user(data)
    print(new_user.to_dict())
    return jsonify({
        "message": "Utilisateur créé avec succès",
        "utilisateur": new_user.to_dict()
    }), 201


@user_bp.route('/login', methods=['POST'])  # ✅ Corrigé ici (/login au lieu de /auth)
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('mot_de_passe'):
        return jsonify({"erreur": "Email et mot de passe requis"}), 400

    # Recherche de l'utilisateur
    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['mot_de_passe']):
        return jsonify({"erreur": "Email ou mot de passe incorrect"}), 401

    # Génération du token JWT
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role  # 👈 Utiliser un point (.) au lieu des crochets ([])
        }
    )

    return jsonify({
        "message": "Connexion réussie",
        "access_token": access_token,
        "role": user.role
    }), 200