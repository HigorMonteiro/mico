"""Tests for adapters."""

import pytest
from mico.adapters.system import SystemAdapter
from mico.domain.entities import SystemInfo, MemoryInfo


def test_system_adapter_get_system_info():
    """Test SystemAdapter.get_system_info returns SystemInfo."""
    adapter = SystemAdapter()
    system_info = adapter.get_system_info()
    
    assert isinstance(system_info, SystemInfo)
    assert isinstance(system_info.memory, MemoryInfo)
    assert system_info.memory.total_gb > 0
    assert system_info.memory.percent >= 0
    assert system_info.memory.percent <= 100

