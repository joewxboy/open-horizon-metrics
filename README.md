# Open Horizon Metrics

A Flask-based metrics collection and reporting system for Open Horizon services and nodes.

## Features

- Multi-architecture support (armhf, arm64, amd64, s390x, ppc64le, riscv)
- Metrics collection from Open Horizon services and nodes
- RESTful API for retrieving accumulated statistics
- Grafana integration for visualization
- Comprehensive API documentation with OpenAPI/Swagger
- Time-based filtering and pagination
- Support for custom metrics

## Prerequisites

- Docker with buildx support
- Python 3.11 or later
- Open Horizon environment
- SQLite (default) or PostgreSQL database

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/joewxboy/open-horizon-metrics.git
   cd open-horizon-metrics
   ```

2. Build the Docker image:
   ```bash
   docker buildx build --platform linux/amd64,linux/arm64,linux/arm/v7,linux/s390x,linux/ppc64le,linux/riscv64 -t open-horizon-metrics .
   ```

3. Run the container:
   ```bash
   docker run -p 5000:5000 open-horizon-metrics
   ```

4. Test the health endpoint:
   ```bash
   curl http://localhost:5000/health
   ```

## Development Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   python app.py
   ```

## Configuration

The application can be configured using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection URL | `sqlite:///data/metrics.db` |
| `SERVICE_NAMES` | Comma-separated list of services to monitor | `''` |
| `COLLECTION_INTERVAL` | Metrics collection interval in seconds | `60` |
| `PORT` | Port to run the server on | `5000` |

Example `.env` file:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/metrics
SERVICE_NAMES=service1,service2,service3
COLLECTION_INTERVAL=30
PORT=5000
```

## API Documentation

API documentation is available at `/api/docs` when running the application. The API provides the following endpoints:

### Service Metrics

- `GET /api/services` - List all services
- `GET /api/services/{service_name}/metrics` - Get metrics for a specific service

Query Parameters:
- `limit` (int): Number of records to return (default: 1, max: 100)
- `offset` (int): Number of records to skip (default: 0)
- `start_time` (string): Start time in ISO 8601 format
- `end_time` (string): End time in ISO 8601 format

Example:
```bash
# Get latest metrics for a service
curl http://localhost:5000/api/services/example-service/metrics

# Get metrics with time range and pagination
curl "http://localhost:5000/api/services/example-service/metrics?start_time=2024-02-20T00:00:00Z&end_time=2024-02-20T23:59:59Z&limit=10&offset=0"
```

### Node Metrics

- `GET /api/nodes` - List all nodes
- `GET /api/nodes/{node_id}/metrics` - Get metrics for a specific node

Query Parameters:
- Same as service metrics endpoints

Example:
```bash
# Get latest metrics for a node
curl http://localhost:5000/api/nodes/node-1/metrics

# Get metrics with time range and pagination
curl "http://localhost:5000/api/nodes/node-1/metrics?start_time=2024-02-20T00:00:00Z&end_time=2024-02-20T23:59:59Z&limit=10&offset=0"
```

### Health Check

- `GET /health` - Check API health status

Example:
```bash
curl http://localhost:5000/health
```

## Metrics Data

The API collects and provides the following metrics:

### Service Metrics
- CPU usage percentage
- Memory usage percentage
- Network input/output rates
- Disk usage percentage
- Additional custom metrics

### Node Metrics
- CPU usage percentage
- Memory usage percentage
- Disk usage percentage
- Network input/output rates
- Additional custom metrics

## API Usage Guide

The Open Horizon Metrics API provides endpoints to retrieve metrics for services and nodes, with support for pagination and time-based filtering.

### Example: Get Service Metrics

```
GET /api/services/<service_name>/metrics?limit=5&start_time=2024-02-20T00:00:00Z&end_time=2024-02-20T23:59:59Z
```

**Response Example:**
```
[
  {
    "id": 1,
    "service_name": "example-service",
    "timestamp": "2024-02-20T12:00:00Z",
    "cpu_usage": 45.5,
    "memory_usage": 60.2,
    "network_in": 1024.0,
    "network_out": 2048.0,
    "disk_usage": 75.0,
    "additional_metrics": {"custom_metric": "value"}
  }
]
```

### Example: Get Node Metrics

```
GET /api/nodes/<node_id>/metrics?limit=5
```

**Response Example:**
```
[
  {
    "id": 1,
    "node_id": "node-1",
    "timestamp": "2024-02-20T12:00:00Z",
    "cpu_usage": 35.5,
    "memory_usage": 50.2,
    "disk_usage": 65.0,
    "network_in": 1536.0,
    "network_out": 3072.0,
    "additional_metrics": {"custom_metric": "value"}
  }
]
```

### Error Response Example

```
{
  "error": "No metrics found for service example-service"
}
```

### Authentication

No authentication is required to access the API endpoints.

### Rate Limiting

There is currently no rate limiting implemented. All endpoints are open for use without restriction.

## Environment Variables

The following environment variables can be used to configure the service:

| Variable Name         | Description                                      | Example / Default                |
|----------------------|--------------------------------------------------|----------------------------------|
| `DATABASE_URL`       | Database connection string (SQLite/PostgreSQL)   | `sqlite:///data/metrics.db`      |
| `API_HOST`           | Host for the API server                          | `0.0.0.0`                        |
| `API_PORT`           | Port for the API server                          | `5000`                           |
| `LOG_LEVEL`          | Logging level                                    | `INFO`                           |
| `CORS_ORIGINS`       | Allowed CORS origins (comma-separated)           | `*`                              |
| `GRAFANA_API_KEY`    | (Optional) API key for Grafana integration       |                                  |

**Example `.env` file:**
```
DATABASE_URL=sqlite:///data/metrics.db
API_HOST=0.0.0.0
API_PORT=5000
LOG_LEVEL=INFO
CORS_ORIGINS=*
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.