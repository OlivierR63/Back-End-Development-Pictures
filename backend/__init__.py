from flask import Flask

# Create Flask application
app = Flask(__name__)

# Import routes after creating the app to avoid circular imports
# This import is necessary to register the routes with the Flask app
from backend import routes  # pylint: disable=unused-import
