from flask import Blueprint
from .scraper_routes import scraper_bp

# Export the blueprint so it can be imported in app/__init__.py
__all__ = ['scraper_bp'] 