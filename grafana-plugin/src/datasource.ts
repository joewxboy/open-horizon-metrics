import {
  DataSourceApi,
  DataSourceInstanceSettings,
  MutableDataFrame,
  FieldType,
  DataQueryRequest,
  DataQueryResponse,
  DataSourceJsonData,
  DataQuery,
} from '@grafana/data';
import { getBackendSrv } from '@grafana/runtime';

export interface OpenHorizonQuery extends DataQuery {
  serviceName?: string;
  nodeId?: string;
  metricType: 'service' | 'node';
  metric: string;
  limit?: number;
}

export interface OpenHorizonDataSourceOptions extends DataSourceJsonData {
  url: string;
}

interface MetricPoint {
  timestamp: string;
  [key: string]: any;
}

export class DataSource extends DataSourceApi<OpenHorizonQuery, OpenHorizonDataSourceOptions> {
  url: string;

  constructor(instanceSettings: DataSourceInstanceSettings<OpenHorizonDataSourceOptions>) {
    super(instanceSettings);
    this.url = instanceSettings.url || '';
  }

  async query(options: DataQueryRequest<OpenHorizonQuery>): Promise<DataQueryResponse> {
    const { range } = options;
    const from = range?.from.toISOString();
    const to = range?.to.toISOString();

    const promises = options.targets.map(async (target) => {
      const query = this.buildQuery(target, from, to);
      const response = await this.doRequest(query);

      return new MutableDataFrame({
        refId: target.refId,
        fields: [
          { name: 'Time', type: FieldType.time, values: (response as MetricPoint[]).map(point => new Date(point.timestamp).getTime()) },
          { name: target.metric, type: FieldType.number, values: (response as MetricPoint[]).map(point => point[target.metric]) },
        ],
      });
    });

    const data = await Promise.all(promises);
    return { data };
  }

  private buildQuery(target: OpenHorizonQuery, from?: string, to?: string): string {
    const baseUrl = target.metricType === 'service' 
      ? `${this.url}/services/${target.serviceName}/metrics`
      : `${this.url}/nodes/${target.nodeId}/metrics`;

    const params = new URLSearchParams();
    if (from) params.append('start_time', from);
    if (to) params.append('end_time', to);
    if (target.limit) params.append('limit', target.limit.toString());

    return `${baseUrl}?${params.toString()}`;
  }

  private async doRequest(query: string) {
    try {
      const response = await getBackendSrv().datasourceRequest({
        url: query,
        method: 'GET',
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching data:', error);
      throw error;
    }
  }

  async testDatasource() {
    try {
      const response = await getBackendSrv().datasourceRequest({
        url: `${this.url}/health`,
        method: 'GET',
      });
      return {
        status: 'success',
        message: 'Data source is working',
      };
    } catch (error) {
      return {
        status: 'error',
        message: 'Error connecting to data source',
      };
    }
  }
} 