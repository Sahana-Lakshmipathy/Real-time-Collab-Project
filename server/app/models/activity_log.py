from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, BIGINT
from app.core.database import Base

class ActivityLog(Base):
    __tablename__ = "activity_log"
    __table_args__ = {"schema": "collab"}

    id = Column(BIGINT, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("collab.users.id"))
    action = Column(String, nullable=False)
    meta_data = Column(JSONB)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationship
    user = relationship("User", back_populates="activities")
