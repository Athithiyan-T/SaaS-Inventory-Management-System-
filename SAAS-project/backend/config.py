"""
Config file for the StockFlow Flask app.

This file reads settings from the .env file and makes them
available to the rest of the app through the Config class.
"""

import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

# Absolute path to the backend/ folder (where this file lives)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _get_database_url():
    """
    Decide which database to use.

    - If a DATABASE_URL is provided (e.g. by Render/Railway for Postgres),
      use that. Some hosts still give old-style "postgres://" URLs, but
      SQLAlchemy 2.x requires "postgresql://", so we fix that up here.
    - Otherwise, fall back to a local SQLite file for development.
    """
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        return database_url

    return "sqlite:///" + os.path.join(BASE_DIR, "database", "database.db")


class Config:
    # Used by Flask to keep sessions and cookies secure
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Used by Flask-JWT-Extended to sign login tokens
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-key")

    # Where our database lives - SQLite locally, Postgres in production
    SQLALCHEMY_DATABASE_URI = _get_database_url()

    # Turns off a feature we don't need, saves some memory/warnings
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # How long a login token stays valid (in seconds). 1 day here.
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24
