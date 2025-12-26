"""Use case: Calculate system health score."""

from typing import Dict, Any
from mico.domain.entities import SystemMetrics


class CalculateSystemHealthUseCase:
    """Use case: Calculate overall system health score."""
    
    @staticmethod
    def execute(system_metrics: SystemMetrics) -> Dict[str, Any]:
        """
        Calculates system health score based on metrics.
        
        Args:
            system_metrics: System metrics to evaluate
        
        Returns:
            Dict with score, status, warnings, and recommendations
        """
        scores = {
            "cpu": CalculateSystemHealthUseCase._calculate_cpu_score(system_metrics.cpu_percent),
            "memory": CalculateSystemHealthUseCase._calculate_memory_score(system_metrics.memory_percent),
            "disk": CalculateSystemHealthUseCase._calculate_disk_score(system_metrics.disk_percent),
        }
        
        warnings = []
        
        if system_metrics.cpu_percent > 80:
            warnings.append(f"High CPU usage: {system_metrics.cpu_percent:.1f}%")
        elif system_metrics.cpu_percent > 60:
            warnings.append(f"CPU usage elevated: {system_metrics.cpu_percent:.1f}%")
        
        if system_metrics.memory_percent > 85:
            warnings.append(f"High memory usage: {system_metrics.memory_percent:.1f}%")
        elif system_metrics.memory_percent > 70:
            warnings.append(f"Memory usage elevated: {system_metrics.memory_percent:.1f}%")
        
        if system_metrics.disk_percent > 90:
            warnings.append(f"Disk space critical: {system_metrics.disk_percent:.1f}% used")
        elif system_metrics.disk_percent > 80:
            warnings.append(f"Disk space low: {system_metrics.disk_percent:.1f}% used")
        
        overall_score = (
            scores["cpu"] * 0.4 +
            scores["memory"] * 0.4 +
            scores["disk"] * 0.2
        )
        
        if overall_score >= 80:
            status = "healthy"
            emoji = "🟢"
        elif overall_score >= 60:
            status = "warning"
            emoji = "🟡"
        else:
            status = "critical"
            emoji = "🔴"
        
        return {
            "overall_score": round(overall_score, 1),
            "status": status,
            "emoji": emoji,
            "scores": scores,
            "warnings": warnings,
            "is_healthy": system_metrics.is_healthy,
        }
    
    @staticmethod
    def _calculate_cpu_score(cpu_percent: float) -> float:
        """Calculate CPU health score (0-100)."""
        if cpu_percent < 50:
            return 100.0
        elif cpu_percent < 70:
            return 100.0 - ((cpu_percent - 50) * 1.5)
        elif cpu_percent < 85:
            return 70.0 - ((cpu_percent - 70) * 2.0)
        else:
            return max(0.0, 40.0 - ((cpu_percent - 85) * 2.5))
    
    @staticmethod
    def _calculate_memory_score(memory_percent: float) -> float:
        """Calculate memory health score (0-100)."""
        if memory_percent < 60:
            return 100.0
        elif memory_percent < 75:
            return 100.0 - ((memory_percent - 60) * 1.33)
        elif memory_percent < 85:
            return 80.0 - ((memory_percent - 75) * 2.0)
        else:
            return max(0.0, 60.0 - ((memory_percent - 85) * 3.0))
    
    @staticmethod
    def _calculate_disk_score(disk_percent: float) -> float:
        """Calculate disk health score (0-100)."""
        if disk_percent < 70:
            return 100.0
        elif disk_percent < 80:
            return 100.0 - ((disk_percent - 70) * 2.0)
        elif disk_percent < 90:
            return 80.0 - ((disk_percent - 80) * 3.0)
        else:
            return max(0.0, 50.0 - ((disk_percent - 90) * 5.0))

