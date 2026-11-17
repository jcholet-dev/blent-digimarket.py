import pytest
from models.product_model import Product
from services.product_service import ProductService

def test_create_product(app):
    """Teste la création d'un produit via le service."""
    with app.app_context():
        data = {
            "nom": "Souris Gamer",
            "description": "Souris optique RGB",
            "categorie": "Accessoires",
            "prix": 29.99,
            "quantite_stock": 50
        }

        product = ProductService.create_product(data)

        assert product.id is not None
        assert product.nom == "Souris Gamer"
        assert product.prix == 29.99
        assert product.quantite_stock == 50
        assert product.categorie == "Accessoires"


def test_get_product_by_id(app):
    """Teste la récupération d'un produit par son ID."""
    with app.app_context():
        data = {
            "nom": "Clavier",
            "categorie": "Accessoires",
            "prix": 50.0,
            "quantite_stock": 10
        }
        created = ProductService.create_product(data)

        found = ProductService.get_by_id(created.id)
        assert found is not None
        assert found.nom == "Clavier"

        # Test avec un ID inexistant
        assert ProductService.get_by_id(9999) is None


def test_update_stock(app):
    """Teste la mise à jour des stocks (ajout, retrait et protection contre les négatifs)."""
    with app.app_context():
        data = {
            "nom": "Webcam",
            "categorie": "Électronique",
            "prix": 80.0,
            "quantite_stock": 5
        }
        product = ProductService.create_product(data)

        # Ajout de stock (+5) -> 5 + 5 = 10
        updated = ProductService.update_stock(product.id, 5)
        assert updated.quantite_stock == 10

        # Retrait excessif de stock (-20) -> doit s'arrêter à 0 et non descendre en négatif
        updated_neg = ProductService.update_stock(product.id, -20)
        assert updated_neg.quantite_stock == 0


def test_delete_product(app):
    """Teste la suppression d'un produit."""
    with app.app_context():
        data = {
            "nom": "Produit à supprimer",
            "categorie": "Test",
            "prix": 10.0,
            "quantite_stock": 1
        }
        product = ProductService.create_product(data)
        product_id = product.id

        # Suppression réussie
        success = ProductService.delete_product(product_id)
        assert success is True
        assert ProductService.get_by_id(product_id) is None

        # Suppression d'un ID qui n'existe pas
        assert ProductService.delete_product(9999) is False


def test_search_products(app):
    """Teste la recherche de produits par mots-clés."""
    with app.app_context():
        ProductService.create_product({
            "nom": "Casque Bluetooth Sony",
            "description": "Son surround immersif",
            "categorie": "Audio",
            "prix": 60.0,
            "quantite_stock": 5
        })

        # Recherche par nom
        results_nom = ProductService.search_products("Bluetooth")
        assert len(results_nom) == 1
        assert results_nom[0].nom == "Casque Bluetooth Sony"

        # Recherche par catégorie
        results_cat = ProductService.search_products("Audio")
        assert len(results_cat) == 1

        # Recherche sans résultat
        results_empty = ProductService.search_products("Inexistant")
        assert len(results_empty) == 0