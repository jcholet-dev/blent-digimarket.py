from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from models.user_model import db
from blueprints import register_blueprints

app = Flask(__name__)

# Clé secrète pour les JWT
app.config["JWT_SECRET_KEY"] = "votre-cle-secrete-super-securisee"

# Configuration de la base de données SQLite (digimarket.db à la racine du projet)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///digimarket.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialisations
db.init_app(app)
jwt = JWTManager(app)

# Enregistrement des Blueprints et routes
register_blueprints(app)

@app.route('/')
def home():
    return render_template('index.html')

# Création automatique des tables dans digimarket.db au premier lancement
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)