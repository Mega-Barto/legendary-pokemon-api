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
    """Create one or multiple mythical classifications."""
    data = request.get_json()

    # Si es una lista, crear múltiples
    if isinstance(data, list):
        created = []
        errors = []

        for item in data:
            if isinstance(item, dict):
                name = item.get("name")
                description = item.get("description")
            else:
                name = item
                description = None

            if not name:
                errors.append("Missing name field")
                continue

            if MythicalClassification.query.filter_by(name=name).first():
                errors.append(f'Classification "{name}" already exists')
                continue

            classification = MythicalClassification(name=name, description=description)
            db.session.add(classification)
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

    if MythicalClassification.query.filter_by(name=data["name"]).first():
        return jsonify({"error": "Classification already exists"}), 409

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
