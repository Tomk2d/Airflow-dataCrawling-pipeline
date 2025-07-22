# Database package
from .connection import db

# Import models to register them with SQLAlchemy
from ..model.Character import Character
from ..model.Category import Category

# Export the database instance
__all__ = ['db', 'Character', 'Category'] 