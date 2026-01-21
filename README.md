# Legendary Pokédex API

A production-ready Flask REST API for managing legendary and mythical Pokémon data with API key authentication.

## Quick Start

### 1. Install Dependencies

Using uv (recommended):

```powershell
uv sync
```

Or using pip:

```powershell
pip install -r requirements.txt
```

### 2. Run Locally (Development)

```powershell
uv run python main.py
```

Or set environment variables:

```powershell
$Env:FLASK_ENV = 'development'
uv run python main.py
```

The API will be available at `http://localhost:5000`

### 3. Run Tests

```powershell
uv run pytest -q
```

### 4. Add New Dependencies

```powershell
uv add package-name
uv export --no-hashes > requirements.txt  # For deployment (PythonAnywhere, etc.)
```

## API Endpoints

### Main Endpoints

These are the primary endpoints for retrieving Pokémon data and related information.

#### GET `/api/v1/pokemon`

Retrieves all Pokémon (legendary and mythical).

**Response:**

```json
[
  {
    "id": 1,
    "name": "Articuno",
    "pokedex_number": 144,
    "description": "Legendary Ice/Flying type Pokémon.",
    "generation": 1,
    "legendary": {
      "classification": "Legendary"
    },
    "region": {
      "id": 1,
      "name": "Kanto"
    },
    "types": [
      { "id": 6, "name": "Ice" },
      { "id": 18, "name": "Flying" }
    ]
  }
]
```

#### GET `/api/v1/pokemon/<int:id>`

Retrieves a specific Pokémon by ID.

#### GET `/api/v1/regions`

Lists all Pokémon regions.

#### GET `/api/v1/types`

Lists all Pokémon types.

#### GET `/api/v1/classifications`

Lists all legendary classifications.

### Administrative Endpoints

These endpoints require an API key for authentication. Include the API key in the request header:

```
X-API-Key: your-api-key-here
```

The default API key is `secret-api-key` (configured in `main.py`).

#### POST `/api/v1/pokemon`

Creates one or multiple Pokémon.

**Request Body (Single Pokémon):**

```json
{
  "name": "Zapdos",
  "pokedex_number": 145,
  "description": "Legendary Electric/Flying type Pokémon.",
  "region_id": 1,
  "type_ids": [3, 18],
  "mythical": {
    "classification_id": 1
  }
}
```

**Request Body (Multiple Pokémon):**

```json
[
  {
    "name": "Zapdos",
    "pokedex_number": 145,
    "description": "Legendary Electric/Flying type Pokémon.",
    "region_id": 1,
    "type_ids": [3, 18],
    "mythical": {
      "classification_id": 1
    }
  },
  {
    "name": "Mew",
    "pokedex_number": 151,
    "description": "Mythical Pokémon from the first generation.",
    "region_id": 1,
    "type_ids": [14],
    "mythical": {
      "classification_id": 2
    }
  }
]
```

**Note:** The `mythical` field is only required for mythical Pokémon. For legendary Pokémon, you can omit this field.

#### DELETE `/api/v1/pokemon/<int:id>`

Deletes a Pokémon by ID.

#### POST `/api/v1/seed`

Reseeds the database with initial data. This endpoint clears all existing data and populates the database with regions, types, classifications, and sample Pokémon.

## Database

The project stores data in a MySQL database.

## Database Schema

### Regions

- Kanto, Johto, Hoenn, Sinnoh, Unova, Kalos, Alola, Galar, Paldea

### Types

- All 18 Pokémon types (Normal, Fire, Water, Grass, etc.)

### Classifications

- Sub-Legendary
- Mythical
- Restriction Legendary

### Pokémon

- Basic fields: name, pokedex_number, description, generation
- Foreign keys: region_id
- Relationships: types (many-to-many), legendary (one-to-one), mythical (one-to-one)

## Development Notes

- The application uses Flask's application factory pattern for better scalability
- SQLAlchemy is used as the ORM with Flask-SQLAlchemy
- Marshmallow handles serialization/deserialization
- Blueprints organize routes by functionality
- The seed data only creates valid records according to the current model
- The web form validates and enforces business rules (max 2 types)

## Deployment

For production deployment, set the following environment variables:

```powershell
$Env:FLASK_ENV = 'production'
$Env:SECRET_KEY = 'your-secret-key-here'
$Env:API_KEY = 'your-api-key-here'
$Env:DATABASE_URL = 'your-database-url'
```

The application is ready for deployment on platforms like PythonAnywhere, Heroku, or any WSGI-compatible hosting service.
