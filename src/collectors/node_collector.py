import psutil
import socket
from typing import Dict, Any
from .base_collector import BaseCollector

class NodeCollector(BaseCollector):
    """Collector for Open Horizon node metrics."""
    
    def __init__(self):
        super().__init__()
        self.node_id = socket.gethostname()

    def collect_metrics(self) -> Dict[str, Any]:
        """Collect metrics for the node."""
        try:
            metrics = {
                'node_id': self.node_id,
                'cpu_usage': self._get_cpu_usage(),
                'memory_usage': self._get_memory_usage(),
                'disk_usage': self._get_disk_usage(),
                'network_in': self._calculate_network_rates()['in'],
                'network_out': self._calculate_network_rates()['out'],
                'additional_metrics': {
                    'cpu_count': psutil.cpu_count(),
                    'cpu_freq': psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None,
                    'memory_total': psutil.virtual_memory().total,
                    'memory_available': psutil.virtual_memory().available,
                    'disk_total': psutil.disk_usage('/').total,
                    'disk_free': psutil.disk_usage('/').free,
                    'boot_time': psutil.boot_time()
                }
            }
            return metrics
        except Exception as e:
            return {
                'node_id': self.node_id,
                'error': f'Failed to collect metrics: {str(e)}'
            } 