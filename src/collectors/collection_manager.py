import schedule
import time
import threading
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..utils.database import SessionLocal
from ..utils.models import ServiceMetrics, NodeMetrics
from .service_collector import ServiceCollector
from .node_collector import NodeCollector

class CollectionManager:
    """Manager for metrics collection process."""
    
    def __init__(self, service_names: List[str], collection_interval: int = 60):
        self.service_names = service_names
        self.collection_interval = collection_interval
        self.service_collectors = [ServiceCollector(name) for name in service_names]
        self.node_collector = NodeCollector()
        self.running = False
        self.thread = None

    def _collect_and_store_metrics(self):
        """Collect and store metrics for all services and node."""
        db = SessionLocal()
        try:
            # Collect and store service metrics
            for collector in self.service_collectors:
                metrics = collector.collect_metrics()
                if 'error' not in metrics:
                    service_metrics = ServiceMetrics(
                        service_name=metrics['service_name'],
                        cpu_usage=metrics['cpu_usage'],
                        memory_usage=metrics['memory_usage'],
                        network_in=metrics['network_in'],
                        network_out=metrics['network_out'],
                        disk_usage=metrics['disk_usage'],
                        additional_metrics=metrics['additional_metrics']
                    )
                    db.add(service_metrics)

            # Collect and store node metrics
            node_metrics = self.node_collector.collect_metrics()
            if 'error' not in node_metrics:
                metrics = NodeMetrics(
                    node_id=node_metrics['node_id'],
                    cpu_usage=node_metrics['cpu_usage'],
                    memory_usage=node_metrics['memory_usage'],
                    disk_usage=node_metrics['disk_usage'],
                    network_in=node_metrics['network_in'],
                    network_out=node_metrics['network_out'],
                    additional_metrics=node_metrics['additional_metrics']
                )
                db.add(metrics)

            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error collecting metrics: {str(e)}")
        finally:
            db.close()

    def _collection_loop(self):
        """Background collection loop."""
        while self.running:
            self._collect_and_store_metrics()
            time.sleep(self.collection_interval)

    def start(self):
        """Start the metrics collection process."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._collection_loop)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        """Stop the metrics collection process."""
        self.running = False
        if self.thread:
            self.thread.join() 