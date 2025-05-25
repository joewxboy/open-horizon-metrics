from flask_restx import fields, Api

# Create API instance
api = Api(
    title='Open Horizon Metrics API',
    version='1.0',
    description='''
    API for retrieving Open Horizon service and node metrics.
    
    This API provides endpoints to:
    - Retrieve metrics for specific services and nodes
    - List all available services and nodes
    - Filter metrics by time range
    - Paginate results
    
    All timestamps are in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ).
    ''',
    doc='/api/docs',  # Set the documentation URL to match the API prefix
    prefix='/api'  # Add API prefix for better organization
)

# Common fields
timestamp_field = fields.DateTime(
    description='Timestamp of the metrics in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)'
)
error_field = fields.String(
    description='Error message if metrics collection failed'
)

# Service metrics model
service_metrics_model = api.model('ServiceMetrics', {
    'id': fields.Integer(
        description='Unique identifier for the metrics record',
        example=1
    ),
    'service_name': fields.String(
        description='Name of the service',
        example='example-service'
    ),
    'timestamp': timestamp_field,
    'cpu_usage': fields.Float(
        description='CPU usage percentage (0-100)',
        example=45.5
    ),
    'memory_usage': fields.Float(
        description='Memory usage percentage (0-100)',
        example=60.2
    ),
    'network_in': fields.Float(
        description='Network input rate in bytes per second',
        example=1024.0
    ),
    'network_out': fields.Float(
        description='Network output rate in bytes per second',
        example=2048.0
    ),
    'disk_usage': fields.Float(
        description='Disk usage percentage (0-100)',
        example=75.0
    ),
    'additional_metrics': fields.Raw(
        description='Additional service-specific metrics in JSON format',
        example={'custom_metric': 'value'}
    )
})

# Node metrics model
node_metrics_model = api.model('NodeMetrics', {
    'id': fields.Integer(
        description='Unique identifier for the metrics record',
        example=1
    ),
    'node_id': fields.String(
        description='Node identifier',
        example='node-1'
    ),
    'timestamp': timestamp_field,
    'cpu_usage': fields.Float(
        description='CPU usage percentage (0-100)',
        example=35.5
    ),
    'memory_usage': fields.Float(
        description='Memory usage percentage (0-100)',
        example=50.2
    ),
    'disk_usage': fields.Float(
        description='Disk usage percentage (0-100)',
        example=65.0
    ),
    'network_in': fields.Float(
        description='Network input rate in bytes per second',
        example=1536.0
    ),
    'network_out': fields.Float(
        description='Network output rate in bytes per second',
        example=3072.0
    ),
    'additional_metrics': fields.Raw(
        description='Additional node-specific metrics in JSON format',
        example={'custom_metric': 'value'}
    )
})

# Error response model
error_model = api.model('Error', {
    'error': fields.String(
        description='Error message describing what went wrong',
        example='No metrics found for service example-service'
    )
})

# Define query parameters for metrics endpoints
metrics_query_params = {
    'limit': {
        'type': int,
        'default': 100,
        'help': 'Number of records to return',
        'location': 'args'
    },
    'start_time': {
        'type': str,
        'help': 'Start time in ISO 8601 format (e.g., 2024-02-20T00:00:00Z)',
        'location': 'args'
    },
    'end_time': {
        'type': str,
        'help': 'End time in ISO 8601 format (e.g., 2024-02-20T23:59:59Z)',
        'location': 'args'
    }
} 