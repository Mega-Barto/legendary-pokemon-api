from flask import Blueprint, jsonify, request

from app.auth import require_api_key
from app.extensions import db
from app.models import MythicalClassification

bp = Blueprint("classifications", __name__, url_prefix="/api/v1")


@bp.route("/mythical-classifications", methods=["GET"])
def get_mythical_classifications():
    """Get all mythical classifications."""
    classifications = MythicalClassification.query.all()
    return jsonify(
        [
            {"id": c.id, "name": c.name, "description": c.description}
            for c in classifications
        ]
    )


@bp.route("/mythical-classifications", methods=["POST"])
@require_api_key
def create_mythical_classification():
    """Create a new mythical classification."""
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({"error": "name is required"}), 400

    classification = MythicalClassification(
        name=data["name"], description=data.get("description")
    )
    db.session.add(classification)
    db.session.commit()

    return (
        jsonify(
            {
                "id": classification.id,
                "name": classification.name,
                "description": classification.description,
            }
        ),
        201,
    )
