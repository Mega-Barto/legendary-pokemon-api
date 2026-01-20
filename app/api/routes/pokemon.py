from flask import Blueprint, jsonify, request

from app.auth import require_api_key
from app.extensions import db
from app.models import Pokemon, Region, Type, MythicalClassification, MythicalPokemon

bp = Blueprint("pokemon", __name__, url_prefix="/api/v1")


def serialize_pokemon(p):
    """Serialize a Pokemon object to dict."""
    return {
        "id": p.id,
        "name": p.name,
        "pokedex_number": p.pokedex_number,
        "image_url": p.image_url,
        "description": p.description,
        "generation": p.generation,
        "region": {"id": p.region.id, "name": p.region.name},
        "types": [{"id": t.id, "name": t.name} for t in p.types],
        "mythical_info": (
            {
                "classification": p.mythical_info.classification.name,
                "event_exclusive": p.mythical_info.event_exclusive,
            }
            if p.mythical_info
            else None
        ),
        "created_at": p.created_at.isoformat() if p.created_at else None,
    }


@bp.route("/pokemon", methods=["GET"])
def get_all_pokemon():
    """Get all Pokémon."""
    pokemon_list = Pokemon.query.all()
    return jsonify([serialize_pokemon(p) for p in pokemon_list])


@bp.route("/pokemon/<int:pokemon_id>", methods=["GET"])
def get_pokemon_by_id(pokemon_id: int):
    """Get a Pokémon by ID."""
    pokemon = Pokemon.query.get_or_404(pokemon_id)
    return jsonify(serialize_pokemon(pokemon))


@bp.route("/pokemon/name/<string:name>", methods=["GET"])
def get_pokemon_by_name(name: str):
    """Get a Pokémon by name."""
    pokemon = Pokemon.query.filter_by(name=name).first_or_404()
    return jsonify(serialize_pokemon(pokemon))


@bp.route("/pokemon", methods=["POST"])
@require_api_key
def create_pokemon():
    """
    Create a new Pokémon.

    Expected JSON:
    {
        "name": "Mewtwo",
        "pokedex_number": 150,
        "description": "A Pokemon created by genetic manipulation...",
        "generation": 1,
        "region_id": 1,
        "type_ids": [14],  // Psychic
        "mythical": {  // optional - only for mythical Pokemon
            "classification_id": 1,
            "event_exclusive": false
        }
    }
    """
    data = request.get_json()

    # Validate required fields
    required = ["name", "pokedex_number", "generation", "region_id", "type_ids"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing required fields: {missing}"}), 400

    # Validate max 2 types (like real Pokemon)
    if len(data["type_ids"]) > 2:
        return jsonify({"error": "A Pokémon can have at most 2 types"}), 400

    if len(data["type_ids"]) < 1:
        return jsonify({"error": "A Pokémon must have at least 1 type"}), 400

    # Verify region exists
    region = Region.query.get(data["region_id"])
    if not region:
        return jsonify({"error": f"Region with id {data['region_id']} not found"}), 404

    # Verify types exist
    types = Type.query.filter(Type.id.in_(data["type_ids"])).all()
    if len(types) != len(data["type_ids"]):
        return jsonify({"error": "One or more type_ids not found"}), 404

    # Create Pokemon
    pokemon = Pokemon(
        name=data["name"],
        pokedex_number=data["pokedex_number"],
        description=data.get("description"),
        generation=data["generation"],
        region_id=data["region_id"],
    )
    pokemon.types = types

    db.session.add(pokemon)
    db.session.flush()  # Get the ID before committing

    # Handle mythical info if provided
    if data.get("mythical"):
        mythical_data = data["mythical"]
        classification = MythicalClassification.query.get(
            mythical_data["classification_id"]
        )
        if not classification:
            db.session.rollback()
            return jsonify({"error": "Mythical classification not found"}), 404

        mythical_info = MythicalPokemon(
            pokemon_id=pokemon.id,
            classification_id=mythical_data["classification_id"],
            event_exclusive=mythical_data.get("event_exclusive", False),
        )
        db.session.add(mythical_info)

    db.session.commit()

    return jsonify(serialize_pokemon(pokemon)), 201


@bp.route("/pokemon/<int:pokemon_id>", methods=["DELETE"])
@require_api_key
def delete_pokemon(pokemon_id: int):
    """Delete a Pokémon."""
    pokemon = Pokemon.query.get_or_404(pokemon_id)

    # Delete mythical info first if exists
    if pokemon.mythical_info:
        db.session.delete(pokemon.mythical_info)

    db.session.delete(pokemon)
    db.session.commit()

    return jsonify({"message": f"Pokemon {pokemon.name} deleted"}), 200
