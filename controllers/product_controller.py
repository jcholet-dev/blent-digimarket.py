from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from services.product_service import ProductService
from utils.decorators import admin_required

product_bp = Blueprint('produits', __name__, url_prefix='/api/produits')

@product_bp.route('', methods=['GET'])
def get_products():
    products = ProductService.get_all_products()
    return jsonify([p.to_dict() for p in products]), 200

@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = ProductService.get_by_id(product_id)
    if not product:
        return jsonify({"erreur": "Produit non trouvé"}), 404
    return jsonify(product.to_dict()), 200

@product_bp.route('', methods=['POST'])
@admin_required
def create_product():
    data = request.get_json()
    if not data or not data.get('nom') or not data.get('prix') or not data.get('categorie'):
        return jsonify({"erreur": "Champs obligatoires manquants"}), 400

    nouveau_produit = ProductService.create_product(data)
    return jsonify({"message": "Produit créé", "produit": nouveau_produit.to_dict()}), 201

@product_bp.route('/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    product = ProductService.get_by_id(product_id)
    if not product:
        return jsonify({"erreur": "Produit non trouvé"}), 404

    data = request.get_json()
    return jsonify({"message": "Produit mis à jour", "produit": product.to_dict()}), 200

@product_bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    success = ProductService.delete_product(product_id)
    if not success:
        return jsonify({"erreur": "Produit non trouvé"}), 404
    return jsonify({"message": "Produit supprimé avec succès"}), 200