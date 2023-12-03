"""Exercice model"""
import re
from dataclasses import dataclass
from io import StringIO
from typing import Generator
from app.adapters.file_read import read_file
from app.core.app_types import EncapsulatePrompt, OpenAiMessage, PathLike, FileItem
from app.core.constants import UNDERLINE


@dataclass
class Exercice:
    """Exercice model"""

    enonce: str
    questions: list[str]
    reponses: list[str]
    explications: list[str]

    @classmethod
    def from_file(cls, data_parsed=list[FileItem]):
        """Create an Exercice from a file"""
        enonce = data_parsed[0].content
        questions = [item.content for item in data_parsed if "QUESTION" in item.title]
        reponses = [item.content for item in data_parsed if "REPONSE" in item.title]
        explications = [
            item.content for item in data_parsed if "EXPLICATION" in item.title
        ]

        return cls(
            enonce=enonce,
            questions=questions,
            reponses=reponses,
            explications=explications,
        )

    def to_openai_prompt(self) -> OpenAiMessage:
        """Return a prompt to send to openai"""

        content = StringIO()
        content.write(f"{UNDERLINE}ENONCE\n{UNDERLINE}")
        content.write(f"{self.enonce}")
        for index, question in enumerate(self.questions):
            content.write(f"{UNDERLINE}QUESTION {index + 1}\n{UNDERLINE}")
            content.write(f"{question}")

        for index, (rep, expli) in enumerate(zip(self.reponses, self.explications)):
            content.write(f"{UNDERLINE}REPONSE {index + 1}\n{UNDERLINE}")
            content.write(f"{rep}")
            content.write(f"{UNDERLINE}EXPLICATION {index + 1}\n{UNDERLINE}")
            content.write(f"{expli}")
        content.write(f"{UNDERLINE}")

        capsule = "Exemple d'exercice de mathématiques"

        secure_prompt = EncapsulatePrompt(content.getvalue(), capsule)

        return secure_prompt.prompt


@dataclass
class ExerciceParser:
    """Parse a file and return an Exercice object"""

    file_path: PathLike
    lines: list[str] = None

    def __post_init__(self):
        lines = read_file(self.file_path)
        lines = "".join(lines)

        self.lines = lines.split(UNDERLINE)[1:-1]

    def parse(self) -> Generator[FileItem, None, None]:
        """Parse the file and return a list of FileItem"""

        title = None
        for line in self.lines:
            if title is not None:
                yield FileItem(title=title, content=line)
                title = None
            else:
                title = line
