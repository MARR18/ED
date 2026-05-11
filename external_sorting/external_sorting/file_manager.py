"""Handles reading/writing of various file formats in chunks."""
import csv
import json
import os
import tempfile
from typing import Any, Iterator, List, Optional, Callable
import pandas as pd
from .exceptions import InvalidFileFormatError
from .utils import logger

class FileManager:
    SUPPORTED_FORMATS = (".txt", ".csv", ".json", ".xlsx", ".jsonl")

    @staticmethod
    def read_chunks(file_path: str, chunk_size: int = 10000) -> Iterator[List[Any]]:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in FileManager.SUPPORTED_FORMATS:
            raise InvalidFileFormatError(f"Unsupported format: {ext}")

        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                chunk = []
                for line in f:
                    chunk.append(line.rstrip("\n"))
                    if len(chunk) >= chunk_size:
                        yield chunk
                        chunk = []
                if chunk:
                    yield chunk

        elif ext == ".csv":
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader, None)  # skip header if any? We'll keep all rows.
                chunk = []
                for row in reader:
                    chunk.append(row)
                    if len(chunk) >= chunk_size:
                        yield chunk
                        chunk = []
                if chunk:
                    yield chunk

        elif ext == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = [data]
                for i in range(0, len(data), chunk_size):
                    yield data[i : i + chunk_size]

        elif ext == ".xlsx":
            df = pd.read_excel(file_path, engine="openpyxl")
            records = df.to_dict("records")
            for i in range(0, len(records), chunk_size):
                yield records[i : i + chunk_size]

        elif ext == ".jsonl":
            buffer = []
            for obj in FileManager.read_jsonl(file_path):
                buffer.append(obj)
                if len(buffer) >= chunk_size:
                    yield buffer
                    buffer = []
            if buffer:
                yield buffer

    @staticmethod
    def write_records(records: List[Any], file_path: str, mode: str = "w") -> None:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".txt":
            with open(file_path, mode, encoding="utf-8") as f:
                for rec in records:
                    f.write(str(rec) + "\n")
        elif ext == ".csv":
            with open(file_path, mode, newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for rec in records:
                    if isinstance(rec, (list, tuple)):
                        writer.writerow(rec)
                    else:
                        writer.writerow([rec])
        elif ext == ".json":
            if mode == "w":
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(records, f, indent=2)
            else:
                with open(file_path, "a", encoding="utf-8") as f:
                    for rec in records:
                        f.write(json.dumps(rec) + "\n")
        elif ext == ".xlsx":
            df = pd.DataFrame(records)
            if mode == "w":
                df.to_excel(file_path, index=False, engine="openpyxl")
            else:
                existing = pd.read_excel(file_path, engine="openpyxl")
                combined = pd.concat([existing, df], ignore_index=True)
                combined.to_excel(file_path, index=False, engine="openpyxl")
        elif ext == ".jsonl":
            FileManager.write_jsonl(records, file_path, mode)

    @staticmethod
    def read_all(file_path: str) -> List[Any]:
        chunks = list(FileManager.read_chunks(file_path, chunk_size=10**9))
        result = []
        for chunk in chunks:
            result.extend(chunk)
        return result

    @staticmethod
    def create_temp_file(prefix: str = "run_", suffix: str = ".jsonl") -> str:
        fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
        os.close(fd)
        return path

    @staticmethod
    def write_jsonl(records: List[Any], file_path: str, mode: str = "w") -> None:
        with open(file_path, mode, encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    @staticmethod
    def read_jsonl(file_path: str) -> Iterator[Any]:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    yield json.loads(line)