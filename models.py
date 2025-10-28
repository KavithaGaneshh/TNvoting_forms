# models.py
from sqlalchemy import Column, Integer, String, Text
from database import Base

class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100))
    district = Column(String(100))
    candidate = Column(String(100))
    comments = Column(Text)
