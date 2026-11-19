from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from database import db  # 1. On importe l'instance db en premier
from models.user_model import User
from models.product_model import Product
from models.order_model import Command, LigneCommande

app = Flask(__name__)

# Configuration
app.config["JWT_SECRET_KEY"] = "votre-cle-secrete-super-securisee"
app.config["SECRET_KEY"] = "une-cle-secrete-tres-difficile-a-deviner-pour-les-sessions"  # <-- AJOUTE CETTE LIGNE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///digimarket.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
jwt = JWTManager(app)


# 4. On importe et enregistre les blueprints après
from blueprints import register_blueprints
register_blueprints(app)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)