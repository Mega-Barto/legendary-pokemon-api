"""
Authentication utilities for protecting API endpoints.
"""
import os
from functools import wraps

from flask import request, jsonify


def require_api_key(f):
    """
    Decorator that requires a valid API key for access.
    
    The API key should be sent in the 'X-API-Key' header.
    The expected key is read from the API_KEY environment variable.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get("X-API-Key")
        expected_key = os.environ.get("API_KEY")
        
        if not expected_key:
            # If no API_KEY is configured, deny all requests for safety
            return jsonify({"error": "Server misconfigured: API_KEY not set"}), 500
        
        if not api_key:
            return jsonify({"error": "Missing API key. Include 'X-API-Key' header"}), 401
        
        if api_key != expected_key:
            return jsonify({"error": "Invalid API key"}), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
