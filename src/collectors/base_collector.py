import psutil
import time
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseCollector(ABC):
    """Base class for metrics collectors."""
    
    def __init__(self):
        self.last_network_io = self._get_network_io()
        self.last_network_time = time.time()

    def _get_cpu_usage(self) -> float:
        """Get CPU usage percentage."""
        return psutil.cpu_percent(interval=1)

    def _get_memory_usage(self) -> float:
        """Get memory usage percentage."""
        return psutil.virtual_memory().percent

    def _get_disk_usage(self) -> float:
        """Get disk usage percentage."""
        return psutil.disk_usage('/').percent

    def _get_network_io(self) -> Dict[str, float]:
        """Get network I/O statistics."""
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv
        }

    def _calculate_network_rates(self) -> Dict[str, float]:
        """Calculate network I/O rates."""
        current_io = self._get_network_io()
        current_time = time.time()
        
        time_diff = current_time - self.last_network_time
        if time_diff == 0:
            return {'in': 0, 'out': 0}
        
        bytes_in = (current_io['bytes_recv'] - self.last_network_io['bytes_recv']) / time_diff
        bytes_out = (current_io['bytes_sent'] - self.last_network_io['bytes_sent']) / time_diff
        
        self.last_network_io = current_io
        self.last_network_time = current_time
        
        return {'in': bytes_in, 'out': bytes_out}

    @abstractmethod
    def collect_metrics(self) -> Dict[str, Any]:
        """Collect metrics. Must be implemented by subclasses."""
        pass 