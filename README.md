# Legendary Pokedex API

Project layout: production-ready Flask application with application factory, blueprints, and extensions.

## Quick start

### 1. Install dependencies using uv:

```powershell
uv sync
```

### 2. Run locally (development):

```powershell
uv run python main.py
```

Or with environment variables:
```powershell
$Env:FLASK_ENV = 'development'
uv run python main.py
```

### 3. Run tests:

```powershell
uv run pytest -q
```

### 4. Add new dependencies:

```powershell
uv add package-name
uv export --no-hashes > requirements.txt  # Para despliegue en PythonAnywhere
```

## Deployment

Ver [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones de despliegue en PythonAnywhere.
