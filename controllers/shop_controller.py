from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from services.product_service import ProductService
from services.cart_service import CartService
from services.order_service import OrderService

shop_bp = Blueprint('shop', __name__, url_prefix='/api/shop')

@shop_bp.route('/', methods=['GET'])
def shop_index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 8, type=int)

    pagination_data = ProductService.get_all_products_pagination(page=page, per_page=per_page)
    cart_count = CartService.get_cart_item_count()

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

@shop_bp.route('/cart', methods=['GET'])
def view_cart():
    cart_data = CartService.get_cart_details()
    cart_count = CartService.get_cart_item_count()
    return render_template('shop/cart.html', cart=cart_data, cart_count=cart_count)

@shop_bp.route('/cart/remove/<int:produit_id>', methods=['POST'])
def remove_from_cart(produit_id):
    CartService.remove_product(produit_id)
    return redirect(url_for('shop.view_cart'))

@shop_bp.route('/cart/update-api', methods=['POST'])
def api_update_cart():
    data = request.get_json()
    produit_id = data.get('produit_id')
    quantite = data.get('quantite')

    if not produit_id or quantite is None:
        return jsonify({"success": False, "error": "Paramètres manquants"}), 400

    CartService.update_quantity(produit_id, quantite)
    cart_data = CartService.get_cart_details()
    new_count = CartService.get_cart_item_count()

    return jsonify({
        "success": True,
        "cart_count": new_count,
        "total_general": cart_data["total_general"],
        "articles": cart_data["articles"]
    })

@shop_bp.route('/checkout', methods=['GET'])
def checkout_page():
    cart_data = CartService.get_cart_details()
    if not cart_data["articles"]:
        return redirect(url_for('shop.view_cart'))
    cart_count = CartService.get_cart_item_count()
    return render_template('shop/checkout.html', cart=cart_data, cart_count=cart_count)
@shop_bp.route('/checkout/process', methods=['POST'])
def process_checkout():
    cart_data = CartService.get_cart_details()
    if not cart_data["articles"]:
        return redirect(url_for('shop.view_cart'))

    adresse = request.form.get('adresse')
    code_postal = request.form.get('code_postal')
    ville = request.form.get('ville')

    adresse_complete = f"{adresse}, {code_postal} {ville}"

    try:
        order_id = OrderService.create_order(cart_data, adresse_complete)
        return render_template('shop/success.html', order_id=order_id, cart_count=0)
    except Exception as e:
        print(f"Erreur lors de la commande : {e}")
        return redirect(url_for('shop.view_cart'))