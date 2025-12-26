"""Tests for adapters."""

import pytest
from mico.adapters.system import SystemAdapter
from mico.domain.entities import SystemInfo, MemoryInfo, Process, SystemMetrics


def test_system_adapter_get_system_info():
    """Test SystemAdapter.get_system_info returns SystemInfo."""
    adapter = SystemAdapter()
    system_info = adapter.get_system_info()
    
    assert isinstance(system_info, SystemInfo)
    assert isinstance(system_info.memory, MemoryInfo)
    assert system_info.memory.total_gb > 0
    assert system_info.memory.percent >= 0
    assert system_info.memory.percent <= 100


def test_system_adapter_get_all_processes():
    """Test SystemAdapter.get_all_processes returns list of Process."""
    adapter = SystemAdapter()
    processes = adapter.get_all_processes()
    
    assert isinstance(processes, list)
    assert len(processes) > 0
    
    for process in processes[:5]:
        assert isinstance(process, Process)
        assert process.pid > 0
        assert process.name
        assert isinstance(process.memory, MemoryInfo)
        assert process.memory.rss_bytes is not None


def test_system_adapter_get_system_metrics():
    """Test SystemAdapter.get_system_metrics returns SystemMetrics."""
    adapter = SystemAdapter()
    metrics = adapter.get_system_metrics()
    
    assert isinstance(metrics, SystemMetrics)
    assert metrics.cpu_percent >= 0
    assert metrics.cpu_percent <= 100
    assert metrics.memory_percent >= 0
    assert metrics.memory_percent <= 100
    assert metrics.disk_percent >= 0
    assert metrics.disk_percent <= 100
    assert metrics.memory_total_gb > 0
    assert metrics.disk_total_gb > 0

