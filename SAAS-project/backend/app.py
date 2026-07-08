import os

from flask import Flask


from config import Config
from flask_cors import CORS

# Import route blueprints (these files are created in later steps)
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.dashboard_routes import dashboard_bp
from routes.settings_routes import settings_bp


def create_app(config_overrides=None):
    """Creates and configures the Flask app.

    config_overrides: optional dict of extra config values, used by our
    test suite to point the app at an isolated in-memory database instead
    of the real one.
    """

    app = Flask(__name__)
    app.config.from_object(Config)

    if config_overrides:
        app.config.update(config_overrides)
        
    # Register all our route blueprints with a common /api prefix
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(product_bp, url_prefix="/api")
    app.register_blueprint(dashboard_bp, url_prefix="/api")
    app.register_blueprint(settings_bp, url_prefix="/api")


    return app


# Create the app so it can be run directly with "python app.py"
app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
