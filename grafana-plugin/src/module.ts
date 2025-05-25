import { DataSourcePlugin } from '@grafana/data';
import { DataSource, OpenHorizonQuery, OpenHorizonDataSourceOptions } from './datasource';
import { QueryEditor } from './QueryEditor';
import { ConfigEditor } from './ConfigEditor';

export const plugin = new DataSourcePlugin<DataSource, OpenHorizonQuery, OpenHorizonDataSourceOptions>(DataSource)
  .setConfigEditor(ConfigEditor)
  .setQueryEditor(QueryEditor); 
