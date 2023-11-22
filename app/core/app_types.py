"""Application types"""
from dataclasses import dataclass
from pathlib import Path


PathLike = str | Path


@dataclass
class FileItem:
    """File item"""

    title: str
    content: str
