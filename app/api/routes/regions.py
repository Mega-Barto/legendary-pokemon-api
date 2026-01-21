from flask import Blueprint, jsonify, request

from app.auth import require_api_key
from app.extensions import db
from app.models import Region

bp = Blueprint("regions", __name__, url_prefix="/api/v1")


@bp.route("/regions", methods=["GET"])
def get_regions():
    """Get all regions."""
    regions = Region.query.all()
    return jsonify([{"id": r.id, "name": r.name} for r in regions])


@bp.route("/regions", methods=["POST"])
@require_api_key
def create_region():
    """Create one or multiple regions."""
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

            if Region.query.filter_by(name=name).first():
                errors.append(f'Region "{name}" already exists')
                continue

            region = Region(name=name)
            db.session.add(region)
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

    if Region.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Region already exists"}), 409

    region = Region(name=data["name"])
    db.session.add(region)
    db.session.commit()

    return jsonify({"id": region.id, "name": region.name}), 201
