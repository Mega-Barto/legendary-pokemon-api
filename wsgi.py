"""
WSGI configuration file for PythonAnywhere deployment.

Instructions:
1. Upload your project to PythonAnywhere
2. In the Web tab, create a new web app
3. Set this file as your WSGI configuration file
4. Set the working directory to your project root
5. Reload your web app
"""

import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/legendary-pokemon-api'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables (or use .env file)
os.environ['FLASK_ENV'] = 'production'
os.environ['SECRET_KEY'] = 'your-secret-key-here'  # Change this!

# Import your Flask app
from main import app as application
