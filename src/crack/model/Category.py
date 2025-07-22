from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from ..database.connection import db

class Category(db.Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    recommend_description = Column(Text, nullable=True)

    characters = relationship("Character", back_populates="category")
