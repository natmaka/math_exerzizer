"""Application types"""
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict


PathLike = str | Path


@dataclass
class FileItem:
    """File item"""

    title: str
    content: str


ROLE = Literal["system", "user", "assistant"]


class OpenAiMessage(TypedDict):
    """OpenAI message"""

    role: ROLE
    content: str
