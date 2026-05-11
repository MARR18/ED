"""Balanced K-Way Merge Sort - external sorting for large files using disk and heap."""
import heapq
import os
from multiprocessing import Pool, cpu_count
from typing import Any, Callable, Iterator, List, Optional, Tuple

from .file_manager import FileManager
from .utils import Statistics, create_progress, logger, console

class BalancedMergeSort:
    def __init__(
        self,
        k: int = 8,
        chunk_size: int = 100000,
        reverse: bool = False,
        key: Optional[Callable[[Any], Any]] = None,
        use_multiprocessing: bool = False,
    ):
        self.k = k
        self.chunk_size = chunk_size
        self.reverse = reverse
        self.key = key or (lambda x: x)
        self.use_multiprocessing = use_multiprocessing
        self.stats = Statistics()

    def sort_file(
        self, input_path: str, output_path: str, temp_dir: Optional[str] = None
    ) -> None:
        self.stats.start()
        run_files = self._create_sorted_runs(input_path, temp_dir)
        logger.info(f"Created {len(run_files)} sorted runs")
        if not run_files:
            open(output_path, "w").close()
            return
        self._merge_runs(run_files, output_path)
        for f in run_files:
            os.unlink(f)
        self.stats.stop()
        self.stats.display()

    def _create_sorted_runs(
        self, input_path: str, temp_dir: Optional[str]
    ) -> List[str]:
        run_files = []
        chunks = list(FileManager.read_chunks(input_path, self.chunk_size))
        if self.use_multiprocessing and len(chunks) > 1:
            with Pool(processes=cpu_count()) as pool:
                args = [(chunk, self.key, self.reverse) for chunk in chunks]
                sorted_chunks = pool.starmap(self._sort_chunk_worker, args)
        else:
            sorted_chunks = [self._sort_chunk(chunk) for chunk in chunks]
        for idx, sorted_chunk in enumerate(sorted_chunks):
            temp_path = FileManager.create_temp_file(
                prefix=f"run_{idx:05d}_", suffix=".jsonl"
            )
            FileManager.write_records(sorted_chunk, temp_path)
            run_files.append(temp_path)
            logger.debug(f"Run #{idx} written to {temp_path}")
        return run_files

    @staticmethod
    def _sort_chunk_worker(
        chunk: List[Any], key: Callable, reverse: bool
    ) -> List[Any]:
        return sorted(chunk, key=key, reverse=reverse)

    def _sort_chunk(self, chunk: List[Any]) -> List[Any]:
        return sorted(chunk, key=self.key, reverse=self.reverse)

    def _merge_runs(self, run_files: List[str], output_path: str) -> None:
        generators = [self._yield_records(f) for f in run_files]
        heap: List[Tuple[Any, int, Any, Iterator]] = []
        for idx, gen in enumerate(generators):
            try:
                record = next(gen)
                key_val = self.key(record)
                heapq.heappush(heap, (key_val, idx, record, gen))
            except StopIteration:
                continue
        buffer_size = 10000
        buffer = []
        progress = create_progress()
        task = progress.add_task("Merging runs...", total=None)
        with progress:
            while heap:
                key_val, idx, record, gen = heapq.heappop(heap)
                buffer.append(record)
                if len(buffer) >= buffer_size:
                    FileManager.write_records(buffer, output_path, mode="a")
                    buffer.clear()
                try:
                    next_record = next(gen)
                    next_key = self.key(next_record)
                    heapq.heappush(heap, (next_key, idx, next_record, gen))
                except StopIteration:
                    pass
                progress.update(task, advance=1)
            if buffer:
                FileManager.write_records(buffer, output_path, mode="a")

    def _yield_records(self, file_path: str) -> Iterator[Any]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".jsonl":
            yield from FileManager.read_jsonl(file_path)
        else:
            for chunk in FileManager.read_chunks(file_path, chunk_size=1):
                for rec in chunk:
                    yield rec

    def sort(self, data: List[Any]) -> List[Any]:
        if len(data) <= self.chunk_size:
            return self._sort_chunk(data)
        chunks = [
            data[i : i + self.chunk_size] for i in range(0, len(data), self.chunk_size)
        ]
        sorted_chunks = [self._sort_chunk(chunk) for chunk in chunks]
        iterators = [iter(chunk) for chunk in sorted_chunks]
        heap = []
        for idx, it in enumerate(iterators):
            try:
                val = next(it)
                key_val = self.key(val)
                heapq.heappush(heap, (key_val, idx, val, it))
            except StopIteration:
                pass
        result = []
        while heap:
            key_val, idx, val, it = heapq.heappop(heap)
            result.append(val)
            try:
                nxt = next(it)
                nxt_key = self.key(nxt)
                heapq.heappush(heap, (nxt_key, idx, nxt, it))
            except StopIteration:
                pass
        return result