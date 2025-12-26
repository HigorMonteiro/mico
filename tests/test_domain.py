"""Tests for domain entities."""

import pytest
from mico.domain.entities import MemoryInfo, SystemInfo


def test_memory_info_properties():
    """Test MemoryInfo properties."""
    memory = MemoryInfo(
        total_gb=16.0,
        available_gb=8.0,
        used_gb=8.0,
        free_gb=8.0,
        percent=50.0
    )
    
    assert memory.total_mb == 16384.0
    assert memory.available_mb == 8192.0
    assert memory.used_mb == 8192.0
    assert memory.free_mb == 8192.0


def test_system_info_creation():
    """Test SystemInfo creation."""
    memory = MemoryInfo(
        total_gb=16.0,
        available_gb=8.0,
        used_gb=8.0,
        free_gb=8.0,
        percent=50.0
    )
    
    system_info = SystemInfo(memory=memory)
    
    assert system_info.memory == memory

