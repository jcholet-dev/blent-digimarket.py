from flask import request, jsonify
from flask_jwt_extended import create_access_token
from models.user_model import db, User


class UserController:

    @staticmethod
    def register():
        """Logique métier pour l'inscription d'un utilisateur"""
        data = request.get_json()

        # 1. Validation des données
        if not data or not data.get('email') or not data.get('mot_de_passe') or not data.get('nom'):
            return jsonify({"erreur": "Veuillez fournir un email, un mot de passe et un nom"}), 400

        # 2. Vérification si l'email existe déjà
        if User.query.filter_by(email=data['email']).first():
            return jsonify({"erreur": "Cet email est déjà utilisé"}), 409

        # 3. Création et sauvegarde de l'utilisateur
        new_user = User(
            email=data['email'],
            nom=data['nom'],
            role=data.get('role', 'client')  # 'client' par défaut
        )
        new_user.set_password(data['mot_de_passe'])

        db.session.add(new_user)
        db.session.commit()

        # 4. Retour de la réponse (Vue JSON)
        return jsonify({
            "message": "Utilisateur créé avec succès",
            "utilisateur": new_user.to_dict()
        }), 201

    @staticmethod
    def login():
        """Logique métier pour la connexion et l'émission du JWT"""
        data = request.get_json()

        if not data or not data.get('email') or not data.get('mot_de_passe'):
            return jsonify({"erreur": "Email et mot de passe requis"}), 400

        # Recherche de l'utilisateur
        user = User.query.filter_by(email=data['email']).first()

        # Vérification du mot de passe haché
        if not user or not user.check_password(data['mot_de_passe']):
            return jsonify({"erreur": "Email ou mot de passe incorrect"}), 401

        # Génération du token JWT
        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            "message": "Connexion réussie",
            "access_token": access_token,
            "role": user.role
        }), 200