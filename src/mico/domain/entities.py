"""Domain entities - Core business objects."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MemoryInfo:
    """
    Value Object - Immutable memory information.
    
    Attributes:
        total_gb: Total memory in GB
        available_gb: Available memory in GB
        used_gb: Used memory in GB
        free_gb: Free memory in GB
        percent: Memory usage percentage
    """
    
    total_gb: float
    available_gb: float
    used_gb: float
    free_gb: float
    percent: float
    
    @property
    def total_mb(self) -> float:
        """Total memory in MB."""
        return self.total_gb * 1024
    
    @property
    def available_mb(self) -> float:
        """Available memory in MB."""
        return self.available_gb * 1024
    
    @property
    def used_mb(self) -> float:
        """Used memory in MB."""
        return self.used_gb * 1024
    
    @property
    def free_mb(self) -> float:
        """Free memory in MB."""
        return self.free_gb * 1024


@dataclass(frozen=True)
class SystemInfo:
    """
    Value Object - System information.
    
    Attributes:
        memory: Memory information
    """
    
    memory: MemoryInfo

