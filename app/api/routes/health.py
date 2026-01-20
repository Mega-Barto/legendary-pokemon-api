from flask import Blueprint, jsonify
from sqlalchemy import text

from app.extensions import db

bp = Blueprint("health", __name__, url_prefix="/api/v1")


@bp.route("/health")
def health():
    """Health check endpoint with database connectivity verification."""
    try:
        db.session.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    status = "ok" if db_status == "connected" else "degraded"

    return jsonify({"status": status, "database": db_status})
