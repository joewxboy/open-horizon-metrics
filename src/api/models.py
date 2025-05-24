from flask_restx import fields
from . import api

# Common fields
timestamp_field = fields.DateTime(description='Timestamp of the metrics')
error_field = fields.String(description='Error message if metrics collection failed')

# Service metrics model
service_metrics_model = api.model('ServiceMetrics', {
    'id': fields.Integer(description='Unique identifier'),
    'service_name': fields.String(description='Name of the service'),
    'timestamp': timestamp_field,
    'cpu_usage': fields.Float(description='CPU usage percentage'),
    'memory_usage': fields.Float(description='Memory usage percentage'),
    'network_in': fields.Float(description='Network input rate in bytes per second'),
    'network_out': fields.Float(description='Network output rate in bytes per second'),
    'disk_usage': fields.Float(description='Disk usage percentage'),
    'additional_metrics': fields.Raw(description='Additional service-specific metrics')
})

# Node metrics model
node_metrics_model = api.model('NodeMetrics', {
    'id': fields.Integer(description='Unique identifier'),
    'node_id': fields.String(description='Node identifier'),
    'timestamp': timestamp_field,
    'cpu_usage': fields.Float(description='CPU usage percentage'),
    'memory_usage': fields.Float(description='Memory usage percentage'),
    'disk_usage': fields.Float(description='Disk usage percentage'),
    'network_in': fields.Float(description='Network input rate in bytes per second'),
    'network_out': fields.Float(description='Network output rate in bytes per second'),
    'additional_metrics': fields.Raw(description='Additional node-specific metrics')
})

# Error response model
error_model = api.model('Error', {
    'error': fields.String(description='Error message')
})

# Query parameters
metrics_query_params = api.parser()
metrics_query_params.add_argument('limit', type=int, help='Number of records to return', default=1)
metrics_query_params.add_argument('offset', type=int, help='Number of records to skip', default=0)
metrics_query_params.add_argument('start_time', type=str, help='Start time in ISO format')
metrics_query_params.add_argument('end_time', type=str, help='End time in ISO format') 