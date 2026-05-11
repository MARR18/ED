"""
External Sorting Library - Professional sorting algorithms for large datasets.

This library provides three external sorting algorithms:
- Recursive Merge Sort (intercalation)
- Direct Merge Sort (bottom-up)
- Balanced K-Way Merge Sort (external memory)

It supports sorting numbers, strings, custom records from various file formats
(TXT, CSV, JSON, Excel) with custom key functions and ascending/descending order.
"""

from .merge_sort import RecursiveMergeSort
from .direct_merge import DirectMergeSort
from .balanced_merge import BalancedMergeSort
from .file_manager import FileManager
from .benchmarks import Benchmark
from .exceptions import ExternalSortingError, InvalidFileFormatError, MemoryLimitError

__all__ = [
    "RecursiveMergeSort",
    "DirectMergeSort",
    "BalancedMergeSort",
    "FileManager",
    "Benchmark",
    "ExternalSortingError",
    "InvalidFileFormatError",
    "MemoryLimitError",
]