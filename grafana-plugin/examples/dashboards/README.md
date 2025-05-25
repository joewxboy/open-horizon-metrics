# Example Dashboards

This directory contains example Grafana dashboards for visualizing Open Horizon metrics. These dashboards demonstrate how to use the Open Horizon Metrics data source plugin to monitor services and nodes.

## Available Dashboards

1. **Service Metrics Overview** (`service-metrics.json`)
   - CPU Usage
   - Memory Usage
   - Network In/Out
   - Disk Usage
   - Auto-refresh every 5 seconds
   - Default time range: Last 1 hour

2. **Node Metrics Overview** (`node-metrics.json`)
   - CPU Usage
   - Memory Usage
   - Disk Usage
   - Network In/Out
   - Auto-refresh every 5 seconds
   - Default time range: Last 1 hour

## Importing Dashboards

1. In Grafana, go to **Dashboards > Import**
2. Click **Upload JSON file**
3. Select one of the dashboard JSON files from this directory
4. Click **Import**

## Customizing Dashboards

After importing, you can customize the dashboards by:

- Changing the service/node name in the query targets
- Adjusting the time range
- Modifying the refresh interval
- Adding new panels
- Customizing visualizations

## Dashboard Features

- **Time Series Visualization**: All metrics are displayed as time series graphs
- **Thresholds**: CPU and memory usage have warning thresholds at 80%
- **Units**: 
  - CPU, Memory, and Disk usage are shown as percentages
  - Network metrics are shown in bytes
- **Auto-refresh**: Dashboards automatically refresh every 5 seconds
- **Tooltips**: Hover over data points to see detailed information
- **Legend**: Shows min, max, and current values

## Notes

- Make sure the Open Horizon Metrics data source is properly configured before importing the dashboards
- The example service name is `example-service` and node ID is `node-1` — update these to match your environment
- You may need to adjust the time range and refresh interval based on your needs 