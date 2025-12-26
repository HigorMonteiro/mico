"""System adapter - Interface with the operating system."""

import psutil
from typing import Protocol, List
from mico.domain.entities import MemoryInfo, SystemInfo, Process


class ISystemAdapter(Protocol):
    """Port - Interface that defines the contract."""
    
    def get_system_info(self) -> SystemInfo:
        """Returns system information."""
        ...
    
    def get_all_processes(self) -> List[Process]:
        """Returns all system processes."""
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
            percent=mem.percent,
            rss_bytes=None,
            vms_bytes=None
        )
        
        return SystemInfo(memory=memory_info)
    
    def get_all_processes(self) -> List[Process]:
        """
        Collects all system processes.
        
        Returns:
            List of Process domain objects
        """
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'username']):
            try:
                pinfo = proc.info
                memory_info = pinfo.get('memory_info')
                
                if memory_info is None:
                    continue
                
                if not hasattr(memory_info, 'rss') or not hasattr(memory_info, 'vms'):
                    continue
                
                total_memory = psutil.virtual_memory().total
                memory_percent = (memory_info.rss / total_memory) * 100
                
                memory = MemoryInfo(
                    rss_bytes=memory_info.rss,
                    vms_bytes=memory_info.vms,
                    percent=memory_percent
                )
                
                process = Process(
                    pid=pinfo['pid'],
                    name=pinfo['name'] or 'Unknown',
                    memory=memory,
                    username=pinfo.get('username')
                )
                
                processes.append(process)
                
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
            except (AttributeError, TypeError, KeyError):
                continue
        
        return processes

