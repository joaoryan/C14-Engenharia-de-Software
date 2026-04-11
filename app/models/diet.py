from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Diet(Base):
    __tablename__ = "diets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)

    user = relationship("User", back_populates="diets")