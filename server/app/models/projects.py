from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {"schema": "collab"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_by = Column(String, ForeignKey("collab.users.id"))
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    creator = relationship("User", back_populates="projects_created")
    members = relationship("ProjectMember", back_populates="project")
    channels = relationship("Channel", back_populates="project")
