"""Exercice model"""
from dataclasses import dataclass
from app.adapters.file_read import read_file
from app.core.app_types import PathLike, FileItem


@dataclass
class Exercice:
    """Exercice model"""

    enonce: str
    questions: list[str]
    reponses: list[str]

    @classmethod
    def from_file(cls, data_parsed=list[FileItem]):
        """Create an Exercice from a file"""
        enonce = data_parsed[0].content
        questions = [item.content for item in data_parsed if "QUESTION" in item.title]
        reponses = [item.content for item in data_parsed if "REPONSE" in item.title]

        return cls(enonce=enonce, questions=questions, reponses=reponses)


@dataclass
class ExerciceParser:
    """Parse a file and return an Exercice object"""

    file_path: PathLike
    lines: list[str] = None

    def __post_init__(self):
        self.lines = read_file(self.file_path)

    def parse(self) -> list[FileItem]:
        """Parse the file and return a list of FileItem"""
        is_title = False
        reading = False
        title = ""
        for line in self.lines:
            if line.startswith("$-----$"):
                reading = not reading
                continue
            if is_title:
                yield FileItem(title=title, content=line)
            else:
                title = line
