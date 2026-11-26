from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from database import db
from models.order_model import Command, LigneCommande
from services.cart_service import CartService
from services.order_service import OrderService
from utils.decorators import admin_required

order_bp = Blueprint('commandes', __name__, url_prefix='/api/commandes')


@order_bp.route('', methods=['POST'])
@jwt_required()
def process_checkout():
    data = request.get_json() or {}

    adresse = data.get('adresse')
    code_postal = data.get('code_postal')
    ville = data.get('ville')
    adresse_livraison = data.get('adresse_livraison') or (f"{adresse}, {code_postal} {ville}" if adresse else None)

    if not adresse_livraison:
        return jsonify({"success": False, "error": "Adresse de livraison requise"}), 400

    cart_data = CartService.get_cart_details()
    if not cart_data or not cart_data.get("articles"):
        return jsonify({"success": False, "error": "Votre panier est vide"}), 400

    try:
        order_id = OrderService.create_order(cart_data, adresse_livraison)
        return jsonify({
            "success": True,
            "message": "Commande créée avec succès",
            "id": order_id,
            "redirect_url": url_for('commandes.success_page', order_id=order_id)
        }), 200
    except Exception as e:
        print(f"Erreur lors de la commande : {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@order_bp.route('/success', methods=['GET'])
def success_page():
    cart_count = CartService.get_cart_item_count() if hasattr(CartService, 'get_cart_item_count') else 0
    return render_template('shop/success.html')

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

    data = request.get_json() or {}
    nouveau_statut = data.get('statut')
    statuts_valides = ['en_attente', 'validée', 'expédiée', 'annulée']

    if nouveau_statut not in statuts_valides:
        return jsonify({"erreur": "Statut invalide"}), 400

    commande.statut = nouveau_statut
    db.session.commit()
    return jsonify({"message": "Statut mis à jour", "statut": commande.statut}), 200


@order_bp.route('', methods=['GET'])
@jwt_required()
def get_commandes():
    claims = get_jwt()
    user_id = int(get_jwt_identity())

    if claims.get("role") == "admin":
        # L'admin voit toutes les commandes
        commandes = Command.query.order_by(Command.date_commande.desc()).all()
    else:
        # Le client ne voit que ses propres commandes
        commandes = Command.query.filter_by(
            utilisateur_id=user_id
        ).order_by(Command.date_commande.desc()).all()

    return jsonify([c.to_dict() for c in commandes]), 200