from controllers.user_controller import user_bp
from controllers.admin_controller import admin_bp
from controllers.shop_controller import shop_bp
from controllers.product_controller import product_bp
from controllers.order_controller import order_bp

def register_blueprints(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)