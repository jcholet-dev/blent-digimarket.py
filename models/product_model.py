from database import db  # <--- Utilisation de l'instance unique partagée
from datetime import datetime, timezone

class Product(db.Model):
    __tablename__ = 'produit'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    categorie = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    quantite_stock = db.Column(db.Integer, nullable=False, default=0)
    date_creation = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    # Ajout d'un nouveau produit
    @classmethod
    def createProduct(cls, data):
        new_product = cls(
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

    # Suppression d'un produit
    def deleteProduct(self):
        db.session.delete(self)
        db.session.commit()

    # Gestion des stocks (ajout ou retrait de quantité)
    def updateStock(self, quantity_change):
        self.quantite_stock += quantity_change
        if self.quantite_stock < 0:
            self.quantite_stock = 0  # Évite les stocks négatifs
        db.session.commit()
        return self

    # Recherche un produit par son ID et retourne sa fiche détaillée
    @classmethod
    def getProduct(cls, product_id):
        product = db.session.get(cls, product_id)
        return product.to_dict() if product else None

    # Récupère tous les produits de la base et les renvoie au format json
    @classmethod
    def getAllProducts(cls):
        products = cls.query.all()
        return [product.to_dict() for product in products]

    # Renvoi le nombre total de produits en base
    @classmethod
    def countProducts(cls):
        return cls.query.count()

    # Recherche des produits par nom, description ou catégorie
    @classmethod
    def searchProducts(cls, query_string):
        search_term = f"%{query_string}%"
        products = cls.query.filter(
            db.or_(
                cls.nom.ilike(search_term),
                cls.description.ilike(search_term),
                cls.categorie.ilike(search_term)
            )
        ).all()
        return [product.to_dict() for product in products]

    # Lister les produits avec pagination
    @classmethod
    def getAllProducts_pagination(cls, page=1, per_page=10):
        """Récupère une liste de produits avec pagination et métadonnées"""
        pagination = cls.query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "products": [product.to_dict() for product in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }

    # Convertit l'objet produit en dictionnaire pour les réponses JSON
    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "description": self.description,
            "categorie": self.categorie,
            "prix": self.prix,
            "quantite_stock": self.quantite_stock,
            "date_creation": self.date_creation.isoformat() if self.date_creation else None
        }