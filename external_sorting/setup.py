from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="external_sorting",
    version="0.1.0",
    author="Your Name",
    description="Professional external sorting algorithms: recursive merge, direct merge, and balanced K‑way merge.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/external_sorting",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.0.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
        "psutil>=5.9.0",
        "tqdm>=4.66.0",
    ],
    entry_points={
        "console_scripts": [
            "extsort=external_sorting.cli:app",
        ],
    },
)