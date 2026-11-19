from flask import Blueprint, request, jsonify, render_template
from services.product_service import ProductService
from services.cart_service import CartService

shop_bp = Blueprint('shop', __name__, url_prefix='/api/shop')

@shop_bp.route('/', methods=['GET'])
def shop_index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 8, type=int)

    pagination_data = ProductService.get_all_products_pagination(page=page, per_page=per_page)
    cart_count = CartService.get_cart_item_count()  # Récupération du total pour la topbar

    return render_template('shop/index.html', data=pagination_data, cart_count=cart_count)


@shop_bp.route('/cart/add-api', methods=['POST'])
def api_add_to_cart():
    data = request.get_json()
    produit_id = data.get('produit_id')
    quantite = data.get('quantite', 1)

    if not produit_id:
        return jsonify({"success": False, "error": "ID du produit manquant"}), 400

    CartService.add_product(produit_id, quantite)
    new_count = CartService.get_cart_item_count()

    return jsonify({
        "success": True,
        "cart_count": new_count,
        "message": "Produit ajouté au panier avec succès"
    })