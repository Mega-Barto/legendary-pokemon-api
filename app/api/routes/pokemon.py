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
        "region": {"id": p.region.id, "name": p.region.name},
        "types": [{"id": t.id, "name": t.name} for t in p.types],
        "mythical_info": (
            {
                "classification": p.mythical_info.classification.name,
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


@bp.route("/pokemon/<int:pokedex_number>", methods=["GET"])
def get_pokemon_by_pokedex_number(pokedex_number: int):
    """Get a Pokémon by Pokedex number."""
    pokemon = Pokemon.query.filter_by(pokedex_number=pokedex_number).first_or_404()
    return jsonify(serialize_pokemon(pokemon))


@bp.route("/pokemon/name/<string:name>", methods=["GET"])
def get_pokemon_by_name(name: str):
    """Get a Pokémon by name."""
    pokemon = Pokemon.query.filter_by(name=name).first_or_404()
    return jsonify(serialize_pokemon(pokemon))


def create_single_pokemon(data):
    """Helper to create a single Pokemon. Returns (pokemon, error)."""
    # Validate required fields
    required = ["name", "pokedex_number", "region_id", "type_ids"]
    missing = [f for f in required if f not in data]
    if missing:
        return None, f"Missing required fields: {missing}"

    # Validate max 2 types
    if len(data["type_ids"]) > 2:
        return None, "A Pokémon can have at most 2 types"

    if len(data["type_ids"]) < 1:
        return None, "A Pokémon must have at least 1 type"

    # Check if already exists
    if Pokemon.query.filter_by(name=data["name"]).first():
        return None, f"Pokemon \"{data['name']}\" already exists"

    if Pokemon.query.filter_by(pokedex_number=data["pokedex_number"]).first():
        return None, f"Pokemon with Pokedex #{data['pokedex_number']} already exists"

    # Verify region exists
    region = Region.query.get(data["region_id"])
    if not region:
        return None, f"Region with id {data['region_id']} not found"

    # Verify types exist
    types = Type.query.filter(Type.id.in_(data["type_ids"])).all()
    if len(types) != len(data["type_ids"]):
        return None, "One or more type_ids not found"

    # Create Pokemon
    pokemon = Pokemon(
        name=data["name"],
        pokedex_number=data["pokedex_number"],
        description=data.get("description"),
        region_id=data["region_id"],
    )
    pokemon.types = types

    db.session.add(pokemon)
    db.session.flush()

    # Handle mythical info if provided
    if data.get("mythical"):
        mythical_data = data["mythical"]
        classification = MythicalClassification.query.get(
            mythical_data["classification_id"]
        )
        if not classification:
            return None, "Mythical classification not found"

        mythical_info = MythicalPokemon(
            pokemon_id=pokemon.id,
            classification_id=mythical_data["classification_id"]
        )
        db.session.add(mythical_info)

    return pokemon, None


@bp.route("/pokemon", methods=["POST"])
@require_api_key
def create_pokemon():
    """
    Create one or multiple Pokémon.

    Single: {"name": "Mewtwo", "pokedex_number": 150, ...}
    Multiple: [{"name": "Mewtwo", ...}, {"name": "Mew", ...}]
    """
    data = request.get_json()

    # Si es una lista, crear múltiples
    if isinstance(data, list):
        created = []
        errors = []

        for poke_data in data:
            pokemon, error = create_single_pokemon(poke_data)
            if error:
                errors.append(f"{poke_data.get('name', 'unknown')}: {error}")
            else:
                created.append(poke_data["name"])

        db.session.commit()

        return jsonify({
            "created": created,
            "errors": errors,
            "total_created": len(created)
        }), 201

    # Si es un objeto, crear uno solo
    pokemon, error = create_single_pokemon(data)
    if error:
        db.session.rollback()
        return jsonify({"error": error}), 400

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
