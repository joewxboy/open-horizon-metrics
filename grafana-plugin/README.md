# Open Horizon Metrics Data Source for Grafana

This Grafana data source plugin allows you to visualize metrics from Open Horizon services and nodes.

## Features

- Query metrics from Open Horizon services and nodes
- Support for CPU, memory, network, and disk metrics
- Time-series visualization
- Configurable data points limit
- Automatic service and node discovery

## Installation

1. Download the latest release from the [releases page](https://github.com/open-horizon/open-horizon-metrics/releases)
2. Extract the plugin to your Grafana plugins directory
3. Restart Grafana

## Configuration

1. Add a new data source in Grafana
2. Select "Open Horizon Metrics" as the data source type
3. Enter the URL of your Open Horizon Metrics API (e.g., `http://localhost:5000`)
4. Click "Save & Test" to verify the connection

## Usage

1. Create a new dashboard or panel
2. Add a new query
3. Select the Open Horizon Metrics data source
4. Choose the metric type (Service or Node)
5. Select the service or node
6. Choose the metric to visualize
7. Optionally set a limit for the number of data points

## Development

### Prerequisites

- Node.js 16 or later
- npm 7 or later

### Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   npm install
   ```

### Development

Run the development server:
```bash
npm run dev
```

### Build

Build the plugin:
```bash
npm run build
```

### Test

Run tests:
```bash
npm test
```

## License

Apache License 2.0 