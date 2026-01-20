from flask import Blueprint, jsonify, request

from app.auth import require_api_key
from app.extensions import db
from app.models import Type

bp = Blueprint("types", __name__, url_prefix="/api/v1")


@bp.route("/types", methods=["GET"])
def get_types():
    """Get all Pokémon types."""
    types = Type.query.all()
    return jsonify([{"id": t.id, "name": t.name} for t in types])


@bp.route("/types", methods=["POST"])
@require_api_key
def create_type():
    """Create a new Pokémon type."""
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({"error": "name is required"}), 400

    pokemon_type = Type(name=data["name"])
    db.session.add(pokemon_type)
    db.session.commit()

    return jsonify({"id": pokemon_type.id, "name": pokemon_type.name}), 201


@bp.route("/types/bulk", methods=["POST"])
@require_api_key
def create_types_bulk():
    """Create multiple types at once. Expects: {"names": ["Fire", "Water", ...]}"""
    data = request.get_json()

    if not data or not data.get("names"):
        return jsonify({"error": "names array is required"}), 400

    created = []
    for name in data["names"]:
        pokemon_type = Type(name=name)
        db.session.add(pokemon_type)
        created.append(pokemon_type)

    db.session.commit()

    return jsonify([{"id": t.id, "name": t.name} for t in created]), 201
