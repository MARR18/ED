"""Generate a large unsorted file for testing external sorting."""

import random
from external_sorting import FileManager


def generate_large_txt(filename: str, num_records: int):
    """Generate a text file with random integers."""
    with open(filename, "w") as f:
        for _ in range(num_records):
            f.write(str(random.randint(1, 1_000_000)) + "\n")
    print(f"Generated {num_records} records in {filename}")


if __name__ == "__main__":
    generate_large_txt("large_input.txt", 500_000)