from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.core.database import Base

class Message(Base):
    __tablename__ = "messages"
    __table_args__ = {"schema": "collab"}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    channel_id = Column(UUID(as_uuid=True), ForeignKey("collab.channels.id"))
    user_id = Column(String, ForeignKey("collab.users.id"))
    content = Column(Text, nullable=False)
    metadata = Column(JSONB)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    channel = relationship("Channel", back_populates="messages")
    user = relationship("User", back_populates="messages")
