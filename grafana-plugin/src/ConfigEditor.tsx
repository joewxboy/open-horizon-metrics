import React from 'react';
import { InlineField, Input } from '@grafana/ui';
import { DataSourcePluginOptionsEditorProps } from '@grafana/data';
import { OpenHorizonDataSourceOptions } from './datasource';

type Props = DataSourcePluginOptionsEditorProps<OpenHorizonDataSourceOptions>;

export function ConfigEditor({ options, onOptionsChange }: Props) {
  const onURLChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    onOptionsChange({
      ...options,
      url: event.target.value,
    });
  };

  return (
    <div>
      <InlineField label="URL" labelWidth={14}>
        <Input
          width={40}
          value={options.url}
          onChange={onURLChange}
          placeholder="http://localhost:5000"
        />
      </InlineField>
    </div>
  );
}
