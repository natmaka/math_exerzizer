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


class EncapsulatePrompt:
    """Encapsulate a prompt with a secret key"""

    def __init__(self, content: str, capsule: str, role: ROLE = "system") -> None:
        """Init"""
        capsuled_content = f"<{capsule}>\n{content}<{capsule}/>"
        self.prompt = OpenAiMessage(role=role, content=capsuled_content)
