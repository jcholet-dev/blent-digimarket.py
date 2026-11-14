from flask import Blueprint, request, jsonify

shop_bp = Blueprint('admin', __name__, url_prefix='/api/shop')