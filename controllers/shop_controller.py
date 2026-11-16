from flask import Blueprint, request, jsonify

shop_bp = Blueprint('shop', __name__, url_prefix='/api/shop')