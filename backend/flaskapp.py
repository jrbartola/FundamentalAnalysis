# __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

db = SQLAlchemy()


def create_app(script_info=None):
    app = Flask(__name__)

    # Grab confiruation from the local env variables
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # Set up extensions
    db.init_app(app)

    # Register our API blueprints
    from api.stocks import stocks_blueprint
    from api.earnings import eps_blueprint
    from api.revenue import revenue_blueprint
    app.register_blueprint(stocks_blueprint)
    app.register_blueprint(eps_blueprint)
    app.register_blueprint(revenue_blueprint)

    # Attach shell context for the CLI
    app.shell_context_processor({'app': app, 'db': db})
    return app