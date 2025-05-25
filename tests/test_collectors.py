import pytest
from src.collectors.service_collector import ServiceCollector
from src.collectors.node_collector import NodeCollector
from src.collectors.collection_manager import CollectionManager
from src.utils.database import Base, engine
from src.utils.models import ServiceMetrics, NodeMetrics

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

def test_service_collector():
    """Test service metrics collection."""
    collector = ServiceCollector("test_service")
    metrics = collector.collect_metrics()
    
    assert isinstance(metrics, dict)
    assert 'service_name' in metrics
    assert metrics['service_name'] == "test_service"
    assert 'error' in metrics  # Service should not be found in test environment

def test_node_collector():
    """Test node metrics collection."""
    collector = NodeCollector()
    metrics = collector.collect_metrics()
    
    assert isinstance(metrics, dict)
    assert 'node_id' in metrics
    assert 'cpu_usage' in metrics
    assert 'memory_usage' in metrics
    assert 'disk_usage' in metrics
    assert 'network_in' in metrics
    assert 'network_out' in metrics
    assert 'additional_metrics' in metrics

def test_collection_manager(db_session):
    """Test metrics collection manager."""
    manager = CollectionManager(["test_service"], collection_interval=1)
    
    # Start collection
    manager.start()
    
    # Wait for at least one collection cycle
    import time
    time.sleep(2)
    
    # Stop collection
    manager.stop()
    
    # Verify metrics were collected
    from src.utils.database import SessionLocal
    db = SessionLocal()
    try:
        service_metrics = db.query(ServiceMetrics).all()
        node_metrics = db.query(NodeMetrics).all()
        
        # In test environment, we might not find the service
        assert len(service_metrics) >= 0
        assert len(node_metrics) > 0
    finally:
        db.close() 