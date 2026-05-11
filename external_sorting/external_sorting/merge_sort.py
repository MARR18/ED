"""Recursive Merge Sort (Intercalación) - in-memory implementation with optional visualization."""

from typing import Any, Callable, List, Optional

from rich.console import Console
from rich.tree import Tree

from .file_manager import FileManager
from .utils import Statistics, logger

console = Console()


class RecursiveMergeSort:
    """
    Classic recursive merge sort algorithm.
    Complexity: O(n log n) time, O(n) space.
    """

    def __init__(
        self,
        reverse: bool = False,
        key: Optional[Callable[[Any], Any]] = None,
        visual: bool = False,
    ):
        """
        :param reverse: If True, sort in descending order.
        :param key: Function to extract comparison key from an element.
        :param visual: If True, display recursion tree and statistics.
        """
        self.reverse = reverse
        self.key = key or (lambda x: x)
        self.visual = visual
        self.stats = Statistics()

    def sort(self, data: List[Any]) -> List[Any]:
        """Return a new sorted list."""
        self.stats.start()
        result = self._merge_sort(data)
        self.stats.stop()
        if self.visual:
            self.stats.display()
        return result

    def _merge_sort(self, arr: List[Any]) -> List[Any]:
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self._merge_sort(arr[:mid])
        right = self._merge_sort(arr[mid:])
        return self._merge(left, right)

    def _merge(self, left: List[Any], right: List[Any]) -> List[Any]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            self.stats.increment_comparisons()
            left_key = self.key(left[i])
            right_key = self.key(right[j])
            if (left_key <= right_key) ^ self.reverse:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        self.stats.increment_merges()
        return result

    def sort_file(self, input_path: str, output_path: str) -> None:
        """
        Sort a file by reading all records into memory.
        Suitable only for files that fit in RAM.
        """
        data = FileManager.read_all(input_path)
        sorted_data = self.sort(data)
        FileManager.write_records(sorted_data, output_path)
        logger.info(f"Sorted file saved to {output_path}")

    def visualize_recursion(self, data: List[Any]) -> None:
        """
        Display a tree of the recursive merge process.
        (Educational: shows how the list is divided and merged.)
        """
        tree = Tree("[bold cyan]Merge Sort Recursion Tree")
        self._build_tree(tree, data)
        console.print(tree)

    def _build_tree(self, node: Tree, arr: List[Any]) -> None:
        if len(arr) <= 1:
            node.add(f"[dim]{arr}[/dim]")
            return
        mid = len(arr) // 2
        left_node = node.add(f"[yellow]Left: {arr[:mid]}[/yellow]")
        right_node = node.add(f"[yellow]Right: {arr[mid:]}[/yellow]")
        self._build_tree(left_node, arr[:mid])
        self._build_tree(right_node, arr[mid:])