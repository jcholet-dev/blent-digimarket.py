# services/product_service.py
from datetime import datetime, timezone
from database import db
from models.product_model import Product

class ProductService:

    @staticmethod
    def create_product(data):
        new_product = Product(
            nom=data.get('nom'),
            description=data.get('description', ''),
            categorie=data.get('categorie'),
            prix=float(data.get('prix', 0.0)),
            quantite_stock=int(data.get('quantite_stock', 0)),
            date_creation=datetime.now(timezone.utc)
        )
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @staticmethod
    def delete_product(product_id):
        product = Product.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_stock(product_id, quantity_change):
        product = Product.query.get(product_id)
        if not product:
            return None

        product.quantite_stock += quantity_change
        if product.quantite_stock < 0:
            product.quantite_stock = 0  # Évite les stocks négatifs

        db.session.commit()
        return product

    @staticmethod
    def get_by_id(product_id):
        return Product.query.get(product_id)

    @staticmethod
    def get_all_products():
        return Product.query.all()

    @staticmethod
    def count_products():
        return Product.query.count()

    @staticmethod
    def search_products(query_string):
        search_term = f"%{query_string}%"
        return Product.query.filter(
            db.or_(
                Product.nom.ilike(search_term),
                Product.description.ilike(search_term),
                Product.categorie.ilike(search_term)
            )
        ).all()

    @staticmethod
    def get_all_products_pagination(page=1, per_page=10):
        pagination = Product.query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            "products": [product.to_dict() for product in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }