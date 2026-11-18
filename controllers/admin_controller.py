# Controller d'administration : gestion des produits, dashboard
from functools import wraps
from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from services.user_service import UserService
from services.product_service import ProductService

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def decorator(*args, **kwargs):
        current_user_id = get_jwt_identity()

        user = UserService.get_by_id(current_user_id)

        if not user or getattr(user, 'role', 'client') != 'admin':
            return jsonify({"erreur": "Accès refusé : administrateur requis"}), 403

        return fn(*args, **kwargs)
    return decorator


@admin_bp.route('/dashboard', methods=['GET'])
#@admin_required
def admin_dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/orders', methods=['GET'])
# @admin_required
def admin_orders():
    return render_template('admin/orders.html')

@admin_bp.route('/products/<int:product_id>', methods=['PUT'])
@admin_required
def admin_update_product(product_id):

    product = ProductService.get_by_id(product_id)
    if not product:
        return jsonify({"erreur": "Produit non trouvé"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"erreur": "Aucune donnée fournie"}), 400

    if 'nom' in data:
        product.nom = data['nom']
    if 'description' in data:
        product.description = data['description']
    if 'categorie' in data:
        product.categorie = data['categorie']
    if 'prix' in data:
        product.prix = float(data['prix'])
    if 'quantite_stock' in data:
        product.quantite_stock = int(data['quantite_stock'])

    db.session.commit()

    return jsonify({
        "message": "Produit mis à jour avec succès",
        "produit": product.to_dict()
    }), 200


@admin_bp.route('/products/<int:product_id>', methods=['DELETE'])
@admin_required
def admin_delete_product(product_id):
    success = ProductService.delete_product(product_id)
    if not success:
        return jsonify({"erreur": "Produit non trouvé"}), 404

    return jsonify({"message": "Produit supprimé avec succès"}), 200

@admin_bp.route('/products', methods=['POST'])
@admin_required
def admin_create_product():
    data = request.get_json()

    if not data or not data.get('nom') or not data.get('prix') or not data.get('categorie'):
        return jsonify({"erreur": "Les champs obligatoires (nom, prix, categorie) sont manquants"}), 400

    try:
        # Utilisation de la méthode de classe du modèle ou du service
        nouveau_produit = Product.createProduct(data)

        return jsonify({
            "message": "Produit créé avec succès",
            "produit": nouveau_produit.to_dict()
        }), 201
    except Exception as e:
        return jsonify({"erreur": f"Erreur lors de la création : {str(e)}"}), 500