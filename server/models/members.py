from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base

class ProjectMember(Base):
    __tablename__ = "project_members"
    __table_args__ = {"schema": "collab"}

    project_id = Column(UUID(as_uuid=True), ForeignKey("collab.projects.id"), primary_key=True)
    user_id = Column(String, ForeignKey("collab.users.id"), primary_key=True)
    role = Column(String, default="member")
    joined_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="memberships")
    project = relationship("Project", back_populates="members")
