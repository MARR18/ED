"""Utility functions: logging, statistics, progress bars, and console formatting."""

import logging
import time
from functools import wraps
from typing import Callable, Optional, List, Any

import psutil
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.table import Table

console = Console()


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Configure and return a logger with colored console output."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger


logger = setup_logger("external_sorting")


class Statistics:
    """
    Collects and displays performance metrics:
    - elapsed time
    - peak memory usage
    - number of comparisons
    - number of merges performed
    """

    def __init__(self):
        self.comparisons: int = 0
        self.merges: int = 0
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None
        self._memory_samples: List[float] = []

    def start(self) -> None:
        """Start timing and record initial memory."""
        self._start_time = time.perf_counter()
        self._record_memory()

    def stop(self) -> None:
        """Stop timing and record final memory."""
        self._end_time = time.perf_counter()
        self._record_memory()

    def _record_memory(self) -> None:
        """Snapshot current RSS memory in MB."""
        mem = psutil.Process().memory_info().rss / (1024 * 1024)
        self._memory_samples.append(mem)

    def increment_comparisons(self, n: int = 1) -> None:
        self.comparisons += n

    def increment_merges(self) -> None:
        self.merges += 1

    def elapsed_time(self) -> float:
        """Return elapsed time in seconds."""
        if self._start_time and self._end_time:
            return self._end_time - self._start_time
        return 0.0

    def peak_memory(self) -> float:
        """Return maximum memory usage in MB."""
        return max(self._memory_samples) if self._memory_samples else 0.0

    def display(self) -> None:
        """Print a formatted table with statistics."""
        table = Table(title="Sorting Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        table.add_row("Time (s)", f"{self.elapsed_time():.4f}")
        table.add_row("Peak Memory (MB)", f"{self.peak_memory():.2f}")
        table.add_row("Comparisons", f"{self.comparisons:,}")
        table.add_row("Merges", f"{self.merges:,}")
        console.print(table)


def create_progress(description: str = "Processing") -> Progress:
    """Return a rich Progress bar with standard columns."""
    return Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        console=console,
    )