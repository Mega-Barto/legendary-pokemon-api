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
    """Create one or multiple Pokémon types."""
    data = request.get_json()

    # Si es una lista, crear múltiples
    if isinstance(data, list):
        created = []
        errors = []

        for item in data:
            name = item.get("name") if isinstance(item, dict) else item

            if not name:
                errors.append("Missing name field")
                continue

            if Type.query.filter_by(name=name).first():
                errors.append(f'Type "{name}" already exists')
                continue

            pokemon_type = Type(name=name)
            db.session.add(pokemon_type)
            created.append(name)

        db.session.commit()

        return jsonify({
            "created": created,
            "errors": errors,
            "total_created": len(created)
        }), 201

    # Si es un objeto, crear uno solo
    if not data or not data.get("name"):
        return jsonify({"error": "name is required"}), 400

    if Type.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Type already exists"}), 409

    pokemon_type = Type(name=data["name"])
    db.session.add(pokemon_type)
    db.session.commit()

    return jsonify({"id": pokemon_type.id, "name": pokemon_type.name}), 201
