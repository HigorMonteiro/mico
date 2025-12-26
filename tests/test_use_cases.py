"""Tests for use cases."""

import pytest
from mico.domain.entities import Process, MemoryInfo
from mico.domain.use_cases.list_processes import ListProcessesUseCase
from mico.domain.use_cases.filter_processes import FilterProcessesUseCase


def test_list_processes_use_case_sort_by_memory():
    """Test ListProcessesUseCase sorting by memory."""
    processes = [
        Process(
            pid=1,
            name="Process A",
            memory=MemoryInfo(rss_bytes=100 * 1024 * 1024, percent=10.0)
        ),
        Process(
            pid=2,
            name="Process B",
            memory=MemoryInfo(rss_bytes=200 * 1024 * 1024, percent=20.0)
        ),
        Process(
            pid=3,
            name="Process C",
            memory=MemoryInfo(rss_bytes=50 * 1024 * 1024, percent=5.0)
        ),
    ]
    
    result = ListProcessesUseCase.execute(processes, sort_by="mem", top_n=2)
    
    assert len(result) == 2
    assert result[0].pid == 2
    assert result[1].pid == 1


def test_list_processes_use_case_sort_by_name():
    """Test ListProcessesUseCase sorting by name."""
    processes = [
        Process(pid=1, name="Zebra", memory=MemoryInfo(rss_bytes=100)),
        Process(pid=2, name="Apple", memory=MemoryInfo(rss_bytes=200)),
        Process(pid=3, name="Banana", memory=MemoryInfo(rss_bytes=50)),
    ]
    
    result = ListProcessesUseCase.execute(processes, sort_by="name", top_n=3)
    
    assert result[0].name == "Zebra"
    assert result[1].name == "Banana"
    assert result[2].name == "Apple"


def test_list_processes_use_case_sort_by_pid():
    """Test ListProcessesUseCase sorting by PID."""
    processes = [
        Process(pid=3, name="Process C", memory=MemoryInfo(rss_bytes=50)),
        Process(pid=1, name="Process A", memory=MemoryInfo(rss_bytes=100)),
        Process(pid=2, name="Process B", memory=MemoryInfo(rss_bytes=200)),
    ]
    
    result = ListProcessesUseCase.execute(processes, sort_by="pid", reverse=False, top_n=3)
    
    assert result[0].pid == 1
    assert result[1].pid == 2
    assert result[2].pid == 3


def test_filter_processes_use_case_by_name():
    """Test FilterProcessesUseCase filtering by name."""
    processes = [
        Process(pid=1, name="Chrome", memory=MemoryInfo(rss_bytes=100)),
        Process(pid=2, name="Firefox", memory=MemoryInfo(rss_bytes=200)),
        Process(pid=3, name="Chrome Helper", memory=MemoryInfo(rss_bytes=50)),
    ]
    
    result = FilterProcessesUseCase.execute(processes, "chrome")
    
    assert len(result) == 2
    assert all("chrome" in p.name.lower() for p in result)


def test_filter_processes_use_case_by_pid():
    """Test FilterProcessesUseCase filtering by PID."""
    processes = [
        Process(pid=123, name="Process A", memory=MemoryInfo(rss_bytes=100)),
        Process(pid=456, name="Process B", memory=MemoryInfo(rss_bytes=200)),
        Process(pid=789, name="Process C", memory=MemoryInfo(rss_bytes=50)),
    ]
    
    result = FilterProcessesUseCase.execute(processes, "123")
    
    assert len(result) == 1
    assert result[0].pid == 123


def test_filter_processes_use_case_empty_filter():
    """Test FilterProcessesUseCase with empty filter returns all."""
    processes = [
        Process(pid=1, name="Process A", memory=MemoryInfo(rss_bytes=100)),
        Process(pid=2, name="Process B", memory=MemoryInfo(rss_bytes=200)),
    ]
    
    result = FilterProcessesUseCase.execute(processes, "")
    
    assert len(result) == 2

