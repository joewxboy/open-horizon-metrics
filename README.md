# Open Horizon Metrics

A Flask-based metrics collection and reporting system for Open Horizon services and nodes.

## Features

- Multi-architecture support (armhf, arm64, amd64, s390x, ppc64le, riscv)
- Metrics collection from Open Horizon services and nodes
- RESTful API for retrieving accumulated statistics
- Grafana integration for visualization

## Prerequisites

- Docker with buildx support
- Python 3.11 or later
- Open Horizon environment

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

## API Documentation

API documentation is available at `/api/docs` when running the application.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.