"""System adapter - Interface with the operating system."""

import psutil
from typing import Protocol, List
from mico.domain.entities import MemoryInfo, SystemInfo, Process, SystemMetrics


class ISystemAdapter(Protocol):
    """Port - Interface that defines the contract."""
    
    def get_system_info(self) -> SystemInfo:
        """Returns system information."""
        ...
    
    def get_all_processes(self) -> List[Process]:
        """Returns all system processes."""
        ...
    
    def get_system_metrics(self) -> SystemMetrics:
        """Returns extended system metrics for health checking."""
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
    
    def get_system_metrics(self) -> SystemMetrics:
        """
        Collects extended system metrics for health checking.
        
        Returns:
            SystemMetrics with CPU, memory, and disk information
        """
        cpu_percent = psutil.cpu_percent(interval=1)
        
        mem = psutil.virtual_memory()
        memory_total_gb = mem.total / (1024 ** 3)
        memory_used_gb = mem.used / (1024 ** 3)
        memory_percent = mem.percent
        
        disk = psutil.disk_usage('/')
        disk_total_gb = disk.total / (1024 ** 3)
        disk_used_gb = disk.used / (1024 ** 3)
        disk_percent = disk.percent
        
        return SystemMetrics(
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            disk_percent=disk_percent,
            memory_total_gb=memory_total_gb,
            memory_used_gb=memory_used_gb,
            disk_total_gb=disk_total_gb,
            disk_used_gb=disk_used_gb
        )

