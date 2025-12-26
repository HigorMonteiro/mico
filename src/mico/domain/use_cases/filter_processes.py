"""Use case: Filter processes by criteria."""

from typing import List
from mico.domain.entities import Process


class FilterProcessesUseCase:
    """Use case: Filter processes by name or PID."""
    
    @staticmethod
    def execute(processes: List[Process], filter_text: str) -> List[Process]:
        """
        Filter processes by name or PID.
        
        Args:
            processes: List of processes
            filter_text: Text to filter by (name or PID)
        
        Returns:
            Filtered list of processes
        """
        if not filter_text:
            return processes
        
        return [p for p in processes if p.matches_filter(filter_text)]

