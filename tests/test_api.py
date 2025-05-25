import pytest
from datetime import datetime, timedelta
from app import app
from src.utils.database import Base, engine, SessionLocal
from src.utils.models import ServiceMetrics, NodeMetrics

@pytest.fixture(scope="function")
def client():
    """Create a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    # Drop all tables and recreate them
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def sample_metrics(db_session):
    """Create sample metrics for testing."""
    # Create service metrics
    service_metrics = ServiceMetrics(
        service_name="test_service",
        cpu_usage=50.0,
        memory_usage=60.0,
        network_in=100.0,
        network_out=200.0,
        disk_usage=70.0,
        additional_metrics={"test": "data"}
    )
    db_session.add(service_metrics)

    # Create node metrics
    node_metrics = NodeMetrics(
        node_id="test_node",
        cpu_usage=40.0,
        memory_usage=50.0,
        disk_usage=60.0,
        network_in=150.0,
        network_out=250.0,
        additional_metrics={"test": "data"}
    )
    db_session.add(node_metrics)
    db_session.commit()

def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

def test_get_service_metrics(client, sample_metrics):
    """Test getting service metrics."""
    response = client.get('/api/services/test_service/metrics')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
    assert data[0]['service_name'] == "test_service"
    assert data[0]['cpu_usage'] == 50.0

def test_get_node_metrics(client, sample_metrics):
    """Test getting node metrics."""
    response = client.get('/api/nodes/test_node/metrics')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
    assert data[0]['node_id'] == "test_node"
    assert data[0]['cpu_usage'] == 40.0

def test_list_services(client, sample_metrics):
    """Test listing services."""
    response = client.get('/api/services')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
    assert data[0]['service_name'] == "test_service"

def test_list_nodes(client, sample_metrics):
    """Test listing nodes."""
    response = client.get('/api/nodes')
    assert response.status_code == 200
    data = response.json
    assert len(data) == 1
    assert data[0]['node_id'] == "test_node"

def test_metrics_not_found(client, sample_metrics):
    """Test getting metrics for non-existent service/node."""
    response = client.get('/api/services/nonexistent/metrics')
    assert response.status_code == 404
    assert response.json['error'] == 'No metrics found for service nonexistent'

    response = client.get('/api/nodes/nonexistent/metrics')
    assert response.status_code == 404
    assert response.json['error'] == 'No metrics found for node nonexistent' 