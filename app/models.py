from datetime import datetime
from .extensions import db


class Region(db.Model):
    """Region where legendary/mythical Pokémon can be found."""
    __tablename__ = "region"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Relationships
    pokemon = db.relationship("Pokemon", back_populates="region", lazy="dynamic")

    def __repr__(self):
        return f"<Region {self.name}>"


class MythicalClassification(db.Model):
    """Classification for mythical Pokémon (e.g., event-exclusive, etc.)."""
    __tablename__ = "mythical_classification"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)

    # Relationships
    mythical_pokemon = db.relationship(
        "MythicalPokemon", back_populates="classification", lazy="dynamic"
    )

    def __repr__(self):
        return f"<MythicalClassification {self.name}>"


class Type(db.Model):
    """Pokémon type (e.g., Fire, Water, Psychic, etc.)."""
    __tablename__ = "type"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"<Type {self.name}>"


# Association table for Pokemon <-> Type (many-to-many)
pokemon_type = db.Table(
    "pokemon_type",
    db.Column(
        "pokemon_id", db.Integer, db.ForeignKey("pokemon.id"), primary_key=True
    ),
    db.Column(
        "type_id", db.Integer, db.ForeignKey("type.id"), primary_key=True
    ),
)


class Pokemon(db.Model):
    """Legendary or mythical Pokémon."""
    __tablename__ = "pokemon"
    
    MAX_TYPES = 2  # Pokémon can have at most 2 types

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    pokedex_number = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    region_id = db.Column(
        db.Integer, db.ForeignKey("region.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    region = db.relationship("Region", back_populates="pokemon")
    types = db.relationship(
        "Type", secondary=pokemon_type, backref=db.backref("pokemon", lazy="dynamic")
    )
    mythical_info = db.relationship(
        "MythicalPokemon", back_populates="pokemon", uselist=False
    )

    @property
    def image_url(self):
        """Generate image URL based on Pokédex number."""
        return f"https://www.pokemon.com/static-assets/content-assets/cms2/img/pokedex/full/{self.pokedex_number:03d}.png"

    def add_type(self, pokemon_type):
        """Add a type to the Pokémon with validation."""
        if len(self.types) >= self.MAX_TYPES:
            raise ValueError(f"A Pokémon can have at most {self.MAX_TYPES} types")
        if pokemon_type not in self.types:
            self.types.append(pokemon_type)

    def set_types(self, types_list):
        """Set types with validation."""
        if len(types_list) > self.MAX_TYPES:
            raise ValueError(f"A Pokémon can have at most {self.MAX_TYPES} types")
        if len(types_list) < 1:
            raise ValueError("A Pokémon must have at least 1 type")
        self.types = types_list

    def __repr__(self):
        return f"<Pokemon #{self.pokedex_number} {self.name}>"


class MythicalPokemon(db.Model):
    """Extra info for mythical Pokémon."""
    __tablename__ = "mythical_pokemon"

    pokemon_id = db.Column(
        db.Integer, db.ForeignKey("pokemon.id"), primary_key=True
    )
    classification_id = db.Column(
        db.Integer, db.ForeignKey("mythical_classification.id"), nullable=False
    )

    # Relationships
    pokemon = db.relationship("Pokemon", back_populates="mythical_info")
    classification = db.relationship(
        "MythicalClassification", back_populates="mythical_pokemon"
    )

    def __repr__(self):
        return f"<MythicalPokemon pokemon_id={self.pokemon_id}>"
