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
    """Create a new region."""
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({"error": "name is required"}), 400

    region = Region(name=data["name"])
    db.session.add(region)
    db.session.commit()

    return jsonify({"id": region.id, "name": region.name}), 201
