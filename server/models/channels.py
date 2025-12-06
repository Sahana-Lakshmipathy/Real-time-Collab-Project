from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class Channel(Base):
    __tablename__ = "channels"
    __table_args__ = {"schema": "collab"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("collab.projects.id"))
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    project = relationship("Project", back_populates="channels")
    messages = relationship("Message", back_populates="channel")
