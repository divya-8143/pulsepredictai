from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin, GUID

class AuditLog(Base, TimestampMixin):
    __tablename__ = "audit_logs"

    user_id = Column(GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    action = Column(String(100), nullable=False, index=True)
    entity_type = Column(String(100), nullable=False, index=True)
    entity_id = Column(String(100), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(255), nullable=True)
    state_diff = Column(JSON, default=dict, nullable=False)

    user = relationship("User", back_populates="audit_logs")
