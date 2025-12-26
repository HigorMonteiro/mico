"""Tests for domain entities."""

import pytest
from mico.domain.entities import MemoryInfo, SystemInfo, Process


def test_memory_info_system_properties():
    """Test MemoryInfo system memory properties."""
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


def test_memory_info_process_properties():
    """Test MemoryInfo process memory properties."""
    memory = MemoryInfo(
        rss_bytes=100 * 1024 * 1024,
        vms_bytes=200 * 1024 * 1024,
        percent=10.0
    )
    
    assert memory.rss_mb == 100.0
    assert memory.vms_mb == 200.0


def test_memory_info_comparison():
    """Test MemoryInfo comparison for sorting."""
    memory1 = MemoryInfo(rss_bytes=100 * 1024 * 1024)
    memory2 = MemoryInfo(rss_bytes=200 * 1024 * 1024)
    
    assert memory1 < memory2


def test_process_creation():
    """Test Process creation."""
    memory = MemoryInfo(rss_bytes=100 * 1024 * 1024, percent=10.0)
    process = Process(pid=123, name="Test Process", memory=memory, username="user")
    
    assert process.pid == 123
    assert process.name == "Test Process"
    assert process.memory == memory
    assert process.username == "user"


def test_process_matches_filter_by_name():
    """Test Process matches_filter by name."""
    memory = MemoryInfo(rss_bytes=100)
    process = Process(pid=123, name="Chrome Browser", memory=memory)
    
    assert process.matches_filter("chrome")
    assert process.matches_filter("CHROME")
    assert not process.matches_filter("firefox")


def test_process_matches_filter_by_pid():
    """Test Process matches_filter by PID."""
    memory = MemoryInfo(rss_bytes=100)
    process = Process(pid=12345, name="Process", memory=memory)
    
    assert process.matches_filter("12345")
    assert not process.matches_filter("123")


def test_process_matches_filter_empty():
    """Test Process matches_filter with empty filter."""
    memory = MemoryInfo(rss_bytes=100)
    process = Process(pid=123, name="Process", memory=memory)
    
    assert process.matches_filter("")


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

