"""Domain entities - Core business objects."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MemoryInfo:
    """
    Value Object - Immutable memory information.
    
    Can represent either system memory or process memory.
    
    Attributes:
        rss_bytes: Resident Set Size - physical memory used (for processes)
        vms_bytes: Virtual Memory Size - virtual memory (for processes)
        percent: Memory usage percentage
        total_gb: Total memory in GB (for system memory)
        available_gb: Available memory in GB (for system memory)
        used_gb: Used memory in GB (for system memory)
        free_gb: Free memory in GB (for system memory)
    """
    
    rss_bytes: Optional[int] = None
    vms_bytes: Optional[int] = None
    percent: Optional[float] = None
    total_gb: Optional[float] = None
    available_gb: Optional[float] = None
    used_gb: Optional[float] = None
    free_gb: Optional[float] = None
    
    @property
    def rss_mb(self) -> float:
        """Resident Set Size in MB."""
        if self.rss_bytes is None:
            return 0.0
        return self.rss_bytes / (1024 * 1024)
    
    @property
    def vms_mb(self) -> float:
        """Virtual Memory Size in MB."""
        if self.vms_bytes is None:
            return 0.0
        return self.vms_bytes / (1024 * 1024)
    
    @property
    def total_mb(self) -> float:
        """Total memory in MB."""
        if self.total_gb is None:
            return 0.0
        return self.total_gb * 1024
    
    @property
    def available_mb(self) -> float:
        """Available memory in MB."""
        if self.available_gb is None:
            return 0.0
        return self.available_gb * 1024
    
    @property
    def used_mb(self) -> float:
        """Used memory in MB."""
        if self.used_gb is None:
            return 0.0
        return self.used_gb * 1024
    
    @property
    def free_mb(self) -> float:
        """Free memory in MB."""
        if self.free_gb is None:
            return 0.0
        return self.free_gb * 1024
    
    def __lt__(self, other: 'MemoryInfo') -> bool:
        """Allow sorting by memory consumption."""
        if self.rss_bytes is None or other.rss_bytes is None:
            return False
        return self.rss_bytes < other.rss_bytes


@dataclass(frozen=True)
class Process:
    """
    Entity - Represents a system process.
    
    Attributes:
        pid: Process ID
        name: Process name
        memory: Memory information for this process
        username: Username that owns the process
    """
    
    pid: int
    name: str
    memory: MemoryInfo
    username: Optional[str] = None
    
    def matches_filter(self, filter_text: str) -> bool:
        """
        Domain logic - checks if process matches filter.
        
        Args:
            filter_text: Text to filter by (name or PID)
        
        Returns:
            True if process matches filter
        """
        if not filter_text:
            return True
        
        filter_lower = filter_text.lower()
        return (
            filter_lower in self.name.lower() or
            str(self.pid) == filter_text
        )
    
    def __str__(self) -> str:
        return f"{self.name} (PID: {self.pid}) - {self.memory.rss_mb:.2f} MB"


@dataclass(frozen=True)
class SystemInfo:
    """
    Value Object - System information.
    
    Attributes:
        memory: Memory information
    """
    
    memory: MemoryInfo

