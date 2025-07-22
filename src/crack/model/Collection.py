from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database.connection import db

class Collection(db.Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    page_id = Column(String, unique=True, nullable=False)
    has_hero_banner_section = Column(Boolean, default=False)
    display_index = Column(Integer)

    characters = relationship(
        "Character",
        secondary="collection_characters",
        back_populates="collections"
    )