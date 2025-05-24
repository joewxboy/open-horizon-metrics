from flask_restx import Api, Resource
from flask import request
from datetime import datetime
from sqlalchemy import desc
from ..utils.database import get_db
from ..utils.models import ServiceMetrics, NodeMetrics
from .models import (
    service_metrics_model,
    node_metrics_model,
    error_model,
    metrics_query_params
)

api = Api(
    title='Open Horizon Metrics API',
    version='1.0',
    description='API for retrieving Open Horizon service and node metrics'
)

@api.route('/services/<string:service_name>/metrics')
@api.param('service_name', 'Name of the service')
@api.response(404, 'Service not found', error_model)
class ServiceMetricsResource(Resource):
    @api.doc('get_service_metrics', params=metrics_query_params)
    @api.marshal_list_with(service_metrics_model)
    def get(self, service_name):
        """Get metrics for a specific service."""
        args = metrics_query_params.parse_args()
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
@api.param('node_id', 'ID of the node')
@api.response(404, 'Node not found', error_model)
class NodeMetricsResource(Resource):
    @api.doc('get_node_metrics', params=metrics_query_params)
    @api.marshal_list_with(node_metrics_model)
    def get(self, node_id):
        """Get metrics for a specific node."""
        args = metrics_query_params.parse_args()
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
class ServicesResource(Resource):
    @api.doc('list_services')
    @api.marshal_list_with(service_metrics_model)
    def get(self):
        """List all services with metrics."""
        db = next(get_db())
        services = db.query(ServiceMetrics.service_name).distinct().all()
        return [{'service_name': service[0]} for service in services]

@api.route('/nodes')
class NodesResource(Resource):
    @api.doc('list_nodes')
    @api.marshal_list_with(node_metrics_model)
    def get(self):
        """List all nodes with metrics."""
        db = next(get_db())
        nodes = db.query(NodeMetrics.node_id).distinct().all()
        return [{'node_id': node[0]} for node in nodes]
