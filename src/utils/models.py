from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base

class ServiceMetrics(Base):
    """Model for storing service metrics."""
    __tablename__ = "service_metrics"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    network_in = Column(Float)
    network_out = Column(Float)
    disk_usage = Column(Float)
    additional_metrics = Column(JSON)

class NodeMetrics(Base):
    """Model for storing node metrics."""
    __tablename__ = "node_metrics"

    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(String, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    cpu_usage = Column(Float)
    memory_usage = Column(Float)
    disk_usage = Column(Float)
    network_in = Column(Float)
    network_out = Column(Float)
    additional_metrics = Column(JSON) 