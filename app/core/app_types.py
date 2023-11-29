"""Application types"""
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, TypedDict

from app.core.constants import SECRET_KEY


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


class SecurePrompt:
    """Encapsulate a prompt with a secret key"""

    def __init__(self, role: ROLE, content: str) -> None:
        """Init"""
        secure_content = f"<PROMPT {SECRET_KEY}>\n{content}<PROMPT {SECRET_KEY}/>"
        self.prompt = OpenAiMessage(role=role, content=secure_content)
