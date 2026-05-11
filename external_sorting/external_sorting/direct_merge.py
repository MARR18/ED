"""Direct Merge Sort (Bottom-Up / Iterative Merge Sort) - non‑recursive, in‑memory."""

from typing import Any, Callable, List, Optional

from .file_manager import FileManager
from .utils import Statistics, logger


class DirectMergeSort:
    """
    Bottom-up iterative merge sort.
    No recursion, works on blocks that double in size each pass.
    Complexity: O(n log n) time, O(n) space.
    """

    def __init__(
        self,
        reverse: bool = False,
        key: Optional[Callable[[Any], Any]] = None,
        show_block_sizes: bool = False,
    ):
        self.reverse = reverse
        self.key = key or (lambda x: x)
        self.show_block_sizes = show_block_sizes
        self.stats = Statistics()

    def sort(self, data: List[Any]) -> List[Any]:
        """Return a new sorted list using bottom-up merging."""
        self.stats.start()
        arr = data.copy()
        width = 1
        n = len(arr)

        while width < n:
            if self.show_block_sizes:
                logger.info(f"Merging blocks of size {width}")
            for i in range(0, n, 2 * width):
                left = arr[i : i + width]
                right = arr[i + width : i + 2 * width]
                merged = self._merge(left, right)
                arr[i : i + len(merged)] = merged
            width *= 2

        self.stats.stop()
        return arr

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
        """Read entire file, sort in memory, write back (only for small files)."""
        data = FileManager.read_all(input_path)
        sorted_data = self.sort(data)
        FileManager.write_records(sorted_data, output_path)
        logger.info(f"Sorted file saved to {output_path}")