"""System adapter - Interface with the operating system."""

import psutil
from typing import Protocol
from mico.domain.entities import MemoryInfo, SystemInfo


class ISystemAdapter(Protocol):
    """Port - Interface that defines the contract."""
    
    def get_system_info(self) -> SystemInfo:
        """Returns system information."""
        ...


class SystemAdapter:
    """Adapter - Implementation using psutil."""
    
    def get_system_info(self) -> SystemInfo:
        """
        Collects system information.
        
        Returns:
            SystemInfo with system information
        """
        mem = psutil.virtual_memory()
        
        memory_info = MemoryInfo(
            total_gb=mem.total / (1024 ** 3),
            available_gb=mem.available / (1024 ** 3),
            used_gb=mem.used / (1024 ** 3),
            free_gb=mem.free / (1024 ** 3),
            percent=mem.percent
        )
        
        return SystemInfo(memory=memory_info)

