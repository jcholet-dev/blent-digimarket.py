from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt

def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        # Vérifie si le claim 'role' est bien 'admin'
        if claims.get("role") != "admin":
            return jsonify({"erreur": "Accès refusé : privilèges administrateur requis."}), 403
        return fn(*args, **kwargs)
    return wrapper