from flask import Flask
from flask_jwt_extended import JWTManager
from models.user_model import db
from controllers.user_controller import UserController

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "votre-cle-secrete-super-securisee"
jwt = JWTManager(app)

# Liaison des routes aux méthodes du Contrôleur
app.route('/api/auth/register', methods=['POST'])(UserController.register)
app.route('/api/auth/login', methods=['POST'])(UserController.login)

if __name__ == '__main__':
    app.run(debug=True)