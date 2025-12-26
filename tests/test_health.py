"""Tests for health calculation use case."""

import pytest
from mico.domain.entities import SystemMetrics
from mico.domain.use_cases.calculate_health import CalculateSystemHealthUseCase


def test_calculate_health_healthy_system():
    """Test health calculation for healthy system."""
    metrics = SystemMetrics(
        cpu_percent=30.0,
        memory_percent=50.0,
        disk_percent=60.0,
        memory_total_gb=16.0,
        memory_used_gb=8.0,
        disk_total_gb=500.0,
        disk_used_gb=300.0
    )
    
    result = CalculateSystemHealthUseCase.execute(metrics)
    
    assert result["overall_score"] >= 80
    assert result["status"] == "healthy"
    assert result["is_healthy"] is True
    assert len(result["warnings"]) == 0


def test_calculate_health_warning_system():
    """Test health calculation for system with warnings."""
    metrics = SystemMetrics(
        cpu_percent=75.0,
        memory_percent=80.0,
        disk_percent=85.0,
        memory_total_gb=16.0,
        memory_used_gb=12.8,
        disk_total_gb=500.0,
        disk_used_gb=425.0
    )
    
    result = CalculateSystemHealthUseCase.execute(metrics)
    
    assert 60 <= result["overall_score"] < 80
    assert result["status"] == "warning"
    assert len(result["warnings"]) > 0


def test_calculate_health_critical_system():
    """Test health calculation for critical system."""
    metrics = SystemMetrics(
        cpu_percent=95.0,
        memory_percent=90.0,
        disk_percent=95.0,
        memory_total_gb=16.0,
        memory_used_gb=14.4,
        disk_total_gb=500.0,
        disk_used_gb=475.0
    )
    
    result = CalculateSystemHealthUseCase.execute(metrics)
    
    assert result["overall_score"] < 60
    assert result["status"] == "critical"
    assert result["is_healthy"] is False
    assert len(result["warnings"]) > 0


def test_calculate_health_scores():
    """Test individual component scores."""
    metrics = SystemMetrics(
        cpu_percent=40.0,
        memory_percent=65.0,
        disk_percent=75.0,
        memory_total_gb=16.0,
        memory_used_gb=10.4,
        disk_total_gb=500.0,
        disk_used_gb=375.0
    )
    
    result = CalculateSystemHealthUseCase.execute(metrics)
    
    assert "cpu" in result["scores"]
    assert "memory" in result["scores"]
    assert "disk" in result["scores"]
    assert all(0 <= score <= 100 for score in result["scores"].values())


def test_system_metrics_is_healthy():
    """Test SystemMetrics.is_healthy property."""
    healthy_metrics = SystemMetrics(
        cpu_percent=50.0,
        memory_percent=70.0,
        disk_percent=80.0,
        memory_total_gb=16.0,
        memory_used_gb=11.2,
        disk_total_gb=500.0,
        disk_used_gb=400.0
    )
    
    assert healthy_metrics.is_healthy is True
    
    unhealthy_metrics = SystemMetrics(
        cpu_percent=90.0,
        memory_percent=90.0,
        disk_percent=95.0,
        memory_total_gb=16.0,
        memory_used_gb=14.4,
        disk_total_gb=500.0,
        disk_used_gb=475.0
    )
    
    assert unhealthy_metrics.is_healthy is False

