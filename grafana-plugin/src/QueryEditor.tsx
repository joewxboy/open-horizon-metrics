import React, { useState, useEffect } from 'react';
import { Select, Input, InlineField, InlineFieldRow } from '@grafana/ui';
import { QueryEditorProps } from '@grafana/data';
import { OpenHorizonQuery, OpenHorizonDataSourceOptions, DataSource } from './datasource';

const metricTypes = [
  { label: 'Service', value: 'service' },
  { label: 'Node', value: 'node' },
];

const serviceMetrics = [
  { label: 'CPU Usage', value: 'cpu_usage' },
  { label: 'Memory Usage', value: 'memory_usage' },
  { label: 'Network In', value: 'network_in' },
  { label: 'Network Out', value: 'network_out' },
  { label: 'Disk Usage', value: 'disk_usage' },
];

const nodeMetrics = [
  { label: 'CPU Usage', value: 'cpu_usage' },
  { label: 'Memory Usage', value: 'memory_usage' },
  { label: 'Disk Usage', value: 'disk_usage' },
  { label: 'Network In', value: 'network_in' },
  { label: 'Network Out', value: 'network_out' },
];

type Props = QueryEditorProps<DataSource, OpenHorizonQuery, OpenHorizonDataSourceOptions>;

export function QueryEditor({ query, onChange, onRunQuery }: Props) {
  const [services, setServices] = useState<Array<{ label: string; value: string }>>([]);
  const [nodes, setNodes] = useState<Array<{ label: string; value: string }>>([]);

  useEffect(() => {
    // Fetch available services and nodes
    const fetchServices = async () => {
      try {
        const response = await fetch('/api/datasources/proxy/1/services');
        const data = await response.json();
        setServices(data.map((service: any) => ({
          label: service.service_name,
          value: service.service_name,
        })));
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    };

    const fetchNodes = async () => {
      try {
        const response = await fetch('/api/datasources/proxy/1/nodes');
        const data = await response.json();
        setNodes(data.map((node: any) => ({
          label: node.node_id,
          value: node.node_id,
        })));
      } catch (error) {
        console.error('Error fetching nodes:', error);
      }
    };

    fetchServices();
    fetchNodes();
  }, []);

  const onMetricTypeChange = (value: string) => {
    onChange({
      ...query,
      metricType: value as 'service' | 'node',
      metric: value === 'service' ? 'cpu_usage' : 'cpu_usage',
    });
    onRunQuery();
  };

  const onMetricChange = (value: string) => {
    onChange({
      ...query,
      metric: value,
    });
    onRunQuery();
  };

  const onServiceChange = (value: string) => {
    onChange({
      ...query,
      serviceName: value,
    });
    onRunQuery();
  };

  const onNodeChange = (value: string) => {
    onChange({
      ...query,
      nodeId: value,
    });
    onRunQuery();
  };

  const onLimitChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onChange({
      ...query,
      limit: parseInt(event.target.value, 10) || undefined,
    });
    onRunQuery();
  };

  return (
    <div>
      <InlineFieldRow>
        <InlineField label="Type" labelWidth={14}>
          <Select
            width={20}
            options={metricTypes}
            value={query.metricType}
            onChange={(v) => onMetricTypeChange(v.value!)}
          />
        </InlineField>
      </InlineFieldRow>

      {query.metricType === 'service' ? (
        <InlineFieldRow>
          <InlineField label="Service" labelWidth={14}>
            <Select
              width={20}
              options={services}
              value={query.serviceName}
              onChange={(v) => onServiceChange(v.value!)}
            />
          </InlineField>
        </InlineFieldRow>
      ) : (
        <InlineFieldRow>
          <InlineField label="Node" labelWidth={14}>
            <Select
              width={20}
              options={nodes}
              value={query.nodeId}
              onChange={(v) => onNodeChange(v.value!)}
            />
          </InlineField>
        </InlineFieldRow>
      )}

      <InlineFieldRow>
        <InlineField label="Metric" labelWidth={14}>
          <Select
            width={20}
            options={query.metricType === 'service' ? serviceMetrics : nodeMetrics}
            value={query.metric}
            onChange={(v) => onMetricChange(v.value!)}
          />
        </InlineField>
      </InlineFieldRow>

      <InlineFieldRow>
        <InlineField label="Limit" labelWidth={14}>
          <Input
            width={20}
            type="number"
            value={query.limit || ''}
            onChange={onLimitChange}
            placeholder="Optional"
          />
        </InlineField>
      </InlineFieldRow>
    </div>
  );
} 