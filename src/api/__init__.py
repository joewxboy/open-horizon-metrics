from flask_restx import Resource, reqparse
from flask import request
from datetime import datetime
from sqlalchemy import desc
from ..utils.database import get_db
from ..utils.models import ServiceMetrics, NodeMetrics
from .models import (
    api,
    service_metrics_model,
    node_metrics_model,
    error_model,
    metrics_query_params
)

# Create request parser for query parameters
parser = reqparse.RequestParser()
for param, config in metrics_query_params.items():
    parser.add_argument(param, **config)

# Define API tags
api_tags = {
    'services': 'Service metrics operations',
    'nodes': 'Node metrics operations'
}

@api.route('/services/<string:service_name>/metrics')
@api.param('service_name', 'Name of the service to get metrics for')
@api.response(404, 'Service not found', error_model)
@api.tag('services')
class ServiceMetricsResource(Resource):
    @api.doc('get_service_metrics',
             params=metrics_query_params,
             description='Get metrics for a specific service. Supports pagination and time-based filtering.',
             responses={
                 200: 'Success',
                 404: 'Service not found'
             },
             example={
                 'service_name': 'example-service',
                 'cpu_usage': 45.5,
                 'memory_usage': 60.2,
                 'network_in': 1024.0,
                 'network_out': 2048.0,
                 'disk_usage': 75.0,
                 'timestamp': '2024-02-20T12:00:00Z'
             })
    @api.marshal_list_with(service_metrics_model)
    def get(self, service_name):
        """Get metrics for a specific service.
        
        Returns a list of metrics for the specified service, ordered by timestamp.
        Supports pagination and time-based filtering.
        """
        args = parser.parse_args()
        db = next(get_db())
        
        query = db.query(ServiceMetrics).filter(
            ServiceMetrics.service_name == service_name
        )
        
        # Apply time filters if provided
        if args['start_time']:
            start_time = datetime.fromisoformat(args['start_time'])
            query = query.filter(ServiceMetrics.timestamp >= start_time)
        if args['end_time']:
            end_time = datetime.fromisoformat(args['end_time'])
            query = query.filter(ServiceMetrics.timestamp <= end_time)
        
        # Apply pagination
        query = query.order_by(desc(ServiceMetrics.timestamp))
        query = query.offset(args['offset']).limit(args['limit'])
        
        metrics = query.all()
        if not metrics:
            api.abort(404, error=f'No metrics found for service {service_name}')
        
        return metrics

@api.route('/nodes/<string:node_id>/metrics')
@api.param('node_id', 'ID of the node to get metrics for')
@api.response(404, 'Node not found', error_model)
@api.tag('nodes')
class NodeMetricsResource(Resource):
    @api.doc('get_node_metrics',
             params=metrics_query_params,
             description='Get metrics for a specific node. Supports pagination and time-based filtering.',
             responses={
                 200: 'Success',
                 404: 'Node not found'
             },
             example={
                 'node_id': 'node-1',
                 'cpu_usage': 35.5,
                 'memory_usage': 50.2,
                 'network_in': 1536.0,
                 'network_out': 3072.0,
                 'disk_usage': 65.0,
                 'timestamp': '2024-02-20T12:00:00Z'
             })
    @api.marshal_list_with(node_metrics_model)
    def get(self, node_id):
        """Get metrics for a specific node.
        
        Returns a list of metrics for the specified node, ordered by timestamp.
        Supports pagination and time-based filtering.
        """
        args = parser.parse_args()
        db = next(get_db())
        
        query = db.query(NodeMetrics).filter(
            NodeMetrics.node_id == node_id
        )
        
        # Apply time filters if provided
        if args['start_time']:
            start_time = datetime.fromisoformat(args['start_time'])
            query = query.filter(NodeMetrics.timestamp >= start_time)
        if args['end_time']:
            end_time = datetime.fromisoformat(args['end_time'])
            query = query.filter(NodeMetrics.timestamp <= end_time)
        
        # Apply pagination
        query = query.order_by(desc(NodeMetrics.timestamp))
        query = query.offset(args['offset']).limit(args['limit'])
        
        metrics = query.all()
        if not metrics:
            api.abort(404, error=f'No metrics found for node {node_id}')
        
        return metrics

@api.route('/services')
@api.tag('services')
class ServicesResource(Resource):
    @api.doc('list_services',
             description='List all services that have metrics data.',
             responses={
                 200: 'Success'
             },
             example=[{
                 'service_name': 'example-service'
             }])
    @api.marshal_list_with(service_metrics_model)
    def get(self):
        """List all services with metrics.
        
        Returns a list of all services that have metrics data in the system.
        """
        db = next(get_db())
        services = db.query(ServiceMetrics.service_name).distinct().all()
        return [{'service_name': service[0]} for service in services]

@api.route('/nodes')
@api.tag('nodes')
class NodesResource(Resource):
    @api.doc('list_nodes',
             description='List all nodes that have metrics data.',
             responses={
                 200: 'Success'
             },
             example=[{
                 'node_id': 'node-1'
             }])
    @api.marshal_list_with(node_metrics_model)
    def get(self):
        """List all nodes with metrics.
        
        Returns a list of all nodes that have metrics data in the system.
        """
        db = next(get_db())
        nodes = db.query(NodeMetrics.node_id).distinct().all()
        return [{'node_id': node[0]} for node in nodes]
