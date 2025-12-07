from sqlalchemy import Column, String, TIMESTAMP, text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "collab"}

    id = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("now()"))

    # Relationships
    projects_created = relationship("Project", back_populates="creator")
    memberships = relationship("ProjectMember", back_populates="user")
    messages = relationship("Message", back_populates="user")
    activities = relationship("ActivityLog", back_populates="user")
