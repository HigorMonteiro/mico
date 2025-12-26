"""Use case: List processes with sorting."""

from typing import List, Literal
from mico.domain.entities import Process


SortCriteria = Literal["mem", "name", "pid"]


class ListProcessesUseCase:
    """Use case: List processes sorted by criteria."""
    
    @staticmethod
    def execute(
        processes: List[Process],
        sort_by: SortCriteria = "mem",
        reverse: bool = True,
        top_n: int = 10
    ) -> List[Process]:
        """
        List processes with sorting and limit.
        
        Args:
            processes: List of available processes
            sort_by: Sorting criteria (mem, name, pid)
            reverse: True for descending order
            top_n: Maximum number of processes to return
        
        Returns:
            Sorted and limited list of processes
        """
        if sort_by == "mem":
            sorted_processes = sorted(
                processes,
                key=lambda p: p.memory.rss_bytes or 0,
                reverse=reverse
            )
        elif sort_by == "name":
            sorted_processes = sorted(
                processes,
                key=lambda p: p.name.lower(),
                reverse=reverse
            )
        else:  # pid
            sorted_processes = sorted(
                processes,
                key=lambda p: p.pid,
                reverse=reverse
            )
        
        return sorted_processes[:top_n]

