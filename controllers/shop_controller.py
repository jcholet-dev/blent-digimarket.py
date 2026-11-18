# services/shop_controller.py (ou controllers/shop_controller.py)
from flask import Blueprint, request, jsonify, render_template
from services.product_service import ProductService

shop_bp = Blueprint('shop', __name__, url_prefix='/api/shop')


@shop_bp.route('/', methods=['GET'])
def shop_index():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 8, type=int)
    try:
        # Récupération des données structurées par le service
        pagination_data = ProductService.get_all_products_pagination(page=page, per_page=per_page)
        return render_template('shop/index.html', data=pagination_data)
    except Exception as e:
        # En cas d'erreur, on renvoie une structure vide pour éviter le plantage de la vue
        empty_data = {
            "products": [],
            "total": 0,
            "pages": 1,
            "current_page": 1,
            "has_next": False,
            "has_prev": False
        }
        return render_template('shop/index.html', data=empty_data)