from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models.product_model import Product
from models.order_model import Command, LigneCommande

shop_bp = Blueprint('shop', __name__, url_prefix='/api/shop')


@shop_bp.route('/products/paginated', methods=['GET'])
def list_catalog_paginated():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    try:
        result = Product.getAllProducts_pagination(page=page, per_page=per_page)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"erreur": f"Erreur lors de la pagination : {str(e)}"}), 500

@shop_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    produit_id = data.get('produit_id')
    quantite = int(data.get('quantite', 1))

    if not produit_id:
        return jsonify({"erreur": "L'ID du produit est requis."}), 400

    produit = db.session.get(Product, produit_id)
    if not produit:
        return jsonify({"erreur": "Produit introuvable."}), 404

    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']
    produit_id_str = str(produit_id)

    cart[produit_id_str] = cart.get(produit_id_str, 0) + quantite
    session.modified = True

    return jsonify({"message": "Produit ajouté au panier", "cart": cart}), 200

@shop_bp.route('/cart', methods=['GET'])
def view_cart():
    raw_cart = session.get('cart', {})
    detailed_items = []
    total_general = 0.0

    for produit_id, quantite in raw_cart.items():
        produit = db.session.get(Product, int(produit_id))
        if produit:
            sous_total = produit.prix * quantite
            total_general += sous_total
            detailed_items.append({
                "produit": produit.to_dict(),
                "quantite": quantite,
                "sous_total": sous_total
            })

    return jsonify({
        "articles": detailed_items,
        "total_general": total_general
    }), 200

@shop_bp.route('/checkout', methods=['POST'])
@jwt_required()
def checkout():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    adresse = data.get('adresse_livraison')

    if not adresse:
        return jsonify({"erreur": "L'adresse de livraison est obligatoire."}), 400
    raw_cart = session.get('cart', {})
    if not raw_cart:
        return jsonify({"erreur": "Votre panier est vide."}), 400

    try:
        nouvelle_commande = Command(
            utilisateur_id=current_user_id,
            adresse_livraison=adresse,
            statut="en_attente"
        )
        db.session.add(nouvelle_commande)
        db.session.flush()

        for produit_id_str, quantite in raw_cart.items():
            produit_id = int(produit_id_str)
            produit = db.session.get(Product, produit_id)

            if not produit:
                db.session.rollback()
                return jsonify({"erreur": f"Produit ID {produit_id} introuvable."}), 404

            if produit.quantite_stock < quantite:
                db.session.rollback()
                return jsonify(
                    {"erreur": f"Stock insuffisant pour : {produit.nom} (Disponible : {produit.quantite_stock})"}), 400

            ligne = LigneCommande(
                commande_id=nouvelle_commande.id,
                produit_id=produit.id,
                quantite=quantite,
                prix_unitaire=produit.prix
            )
            db.session.add(ligne)
            produit.updateStock(-quantite)

        db.session.commit()
        session.pop('cart', None)
        session.modified = True

        return jsonify({
            "message": "Commande validée avec succès !",
            "commande": nouvelle_commande.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"erreur": f"Erreur lors du checkout : {str(e)}"}), 500