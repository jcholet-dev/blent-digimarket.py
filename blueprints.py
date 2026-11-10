from controllers.user_controller import user_bp

def register_blueprints(app):
    app.register_blueprint(user_bp)