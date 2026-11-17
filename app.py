from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from database import db  # 1. On importe l'instance db en premier

app = Flask(__name__)

# Configuration
app.config["JWT_SECRET_KEY"] = "votre-cle-secrete-super-securisee"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///digimarket.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# 2. On initialise db avec l'application TOUT DE SUITE
db.init_app(app)
jwt = JWTManager(app)

# 3. ON IMPORTE LES MODELES APRES l'initialisation de db
from models.user_model import User
from models.product_model import Product

# 4. On importe et enregistre les blueprints après
from blueprints import register_blueprints
register_blueprints(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)