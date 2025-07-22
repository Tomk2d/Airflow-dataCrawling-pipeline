from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..database.connection import db


class Character(db.Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    profile_image = Column(JSONB)  
    initial_messages = Column(Text)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    category = relationship("Category", back_populates="characters")
    collections = relationship(
        "Collection",
        secondary="collection_characters",
        back_populates="characters"
    )
