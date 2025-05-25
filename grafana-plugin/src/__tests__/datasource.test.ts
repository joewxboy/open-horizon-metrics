import { DataSource } from '../datasource';
import { dateTime } from '@grafana/data';

describe('OpenHorizonMetricsDataSource', () => {
  let datasource: DataSource;

  beforeEach(() => {
    datasource = new DataSource({
      id: 1,
      uid: 'test-uid',
      type: 'openhorizon-metrics',
      name: 'Test Data Source',
      url: 'http://localhost:5000',
      jsonData: { url: 'http://localhost:5000' },
      access: 'proxy',
      readOnly: false,
      meta: {
        id: 'openhorizon-metrics',
        name: 'Open Horizon Metrics',
        type: 'datasource' as any,
        info: {
          author: { name: 'Open Horizon Team' },
          version: '1.0.0',
          description: 'Open Horizon Metrics data source for Grafana',
          links: [],
          logos: { small: '', large: '' },
          screenshots: [],
          updated: '2025-05-25',
        },
        module: 'openhorizon-metrics',
        baseUrl: 'http://localhost:5000',
      },
    });
  });

  it('should connect to the API', async () => {
    const result = await datasource.testDatasource();
    expect(result.status).toBe('success');
  });

  it('should retrieve metrics data', async () => {
    const query = { metric: 'cpu_usage', nodeId: 'node1', metricType: 'node' as const, refId: 'A' };
    const result = await datasource.query({
      targets: [query],
      requestId: 'test-request',
      interval: '1m',
      intervalMs: 60000,
      range: { from: dateTime(), to: dateTime(), raw: { from: dateTime(), to: dateTime() } },
      scopedVars: {},
      timezone: 'UTC',
      app: 'dashboard',
      startTime: Date.now(),
    });
    expect(result.data).toBeDefined();
  });
}); 