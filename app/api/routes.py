from flask import Blueprint, jsonify

bp = Blueprint("routes", __name__, url_prefix="/api/v1")


@bp.route("/health")
def health():
    return jsonify({"status": "ok"})


@bp.route("/pokemon/<string:name>")
def get_pokemon(name: str):
    # Placeholder implementation — integrate real data source later.
    data = {"name": name, "legendary": False}
    return jsonify(data)
