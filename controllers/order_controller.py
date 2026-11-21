from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from database import db
from models.order_model import Command, LigneCommande
from utils.decorators import admin_required

order_bp = Blueprint('commandes', __name__, url_prefix='/api/commandes')

@order_bp.route('', methods=['GET'])
@jwt_required()
def get_commandes():
    claims = get_jwt()
    user_id = get_jwt_identity()
    role = claims.get('role')

    if role == 'admin':
        commandes = Command.query.all()
    else:
        commandes = Command.query.filter_by(user_id=user_id).all()

    return jsonify([c.to_dict() for c in commandes]), 200

@order_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_commande(order_id):
    commande = Command.query.get(order_id)
    if not commande:
        return jsonify({"erreur": "Commande introuvable"}), 404
    return jsonify(commande.to_dict()), 200

@order_bp.route('/<int:order_id>/lignes', methods=['GET'])
@jwt_required()
def get_commande_lignes(order_id):
    commande = Command.query.get(order_id)
    if not commande:
        return jsonify({"erreur": "Commande introuvable"}), 404

    lignes = [ligne.to_dict() for ligne in commande.lignes]
    return jsonify(lignes), 200

@order_bp.route('/<int:order_id>', methods=['PATCH'])
@admin_required
def update_order_status(order_id):
    commande = Command.query.get(order_id)
    if not commande:
        return jsonify({"erreur": "Commande introuvable"}), 404

    data = request.get_json()
    nouveau_statut = data.get('statut')
    statuts_valides = ['en_attente', 'validée', 'expédiée', 'annulée']

    if nouveau_statut not in statuts_valides:
        return jsonify({"erreur": "Statut invalide"}), 400

    commande.statut = nouveau_statut
    db.session.commit()
    return jsonify({"message": "Statut mis à jour", "statut": commande.statut}), 200