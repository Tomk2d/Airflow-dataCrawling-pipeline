from sqlalchemy import Column, Integer, ForeignKey
from ..database.connection import db

class CollectionCharacter(db.Base):
    __tablename__ = "collection_characters"

    collection_id = Column(Integer, ForeignKey("collections.id", ondelete="CASCADE"), primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id", ondelete="CASCADE"), primary_key=True)
