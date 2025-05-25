import psutil
from typing import Dict, Any, List
from .base_collector import BaseCollector

class ServiceCollector(BaseCollector):
    """Collector for Open Horizon service metrics."""
    
    def __init__(self, service_name: str):
        super().__init__()
        self.service_name = service_name
        self._find_service_process()

    def _find_service_process(self) -> None:
        """Find the process for the Open Horizon service."""
        self.process = None
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if self.service_name in ' '.join(proc.info['cmdline'] or []):
                    self.process = proc
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def collect_metrics(self) -> Dict[str, Any]:
        """Collect metrics for the service."""
        if not self.process:
            self._find_service_process()
            if not self.process:
                return {
                    'service_name': self.service_name,
                    'error': 'Service process not found'
                }

        try:
            with self.process.oneshot():
                metrics = {
                    'service_name': self.service_name,
                    'cpu_usage': self.process.cpu_percent(),
                    'memory_usage': self.process.memory_percent(),
                    'network_in': self._calculate_network_rates()['in'],
                    'network_out': self._calculate_network_rates()['out'],
                    'disk_usage': self._get_disk_usage(),
                    'additional_metrics': {
                        'num_threads': self.process.num_threads(),
                        'num_fds': self.process.num_fds() if hasattr(self.process, 'num_fds') else None,
                        'create_time': self.process.create_time(),
                        'status': self.process.status()
                    }
                }
                return metrics
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            self.process = None
            return {
                'service_name': self.service_name,
                'error': 'Failed to collect metrics'
            } 