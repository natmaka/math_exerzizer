"""Exercice model"""
from dataclasses import dataclass
from io import StringIO
from typing import Generator
from app.adapters.file_read import read_file
from app.core.app_types import OpenAiMessage, PathLike, FileItem
from app.core.constants import UNDERLINE


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

    def to_openai_prompt(self):
        """Return a prompt string"""

        content = StringIO()
        content.write("Voici un exemple d'exercice de mathématiques:\n")
        content.write(f"{UNDERLINE}DEBUT DE L'EXERCICE\n{UNDERLINE}")
        content.write(f"ENONCE\n{UNDERLINE}{self.enonce}\n")
        for index, (question, reponse) in enumerate(zip(self.questions, self.reponses)):
            content.write(f"QUESTION_{index+1}\n{UNDERLINE}{question}\n")
            content.write(f"REPONSE_{index+1}\n{UNDERLINE}{reponse}\n")
        content.write(f"{UNDERLINE}FIN DE L'EXERCICE\n{UNDERLINE}")

        return OpenAiMessage(role="system", content=content.getvalue())


@dataclass
class ExerciceParser:
    """Parse a file and return an Exercice object"""

    file_path: PathLike
    lines: list[str] = None

    def __post_init__(self):
        self.lines = read_file(self.file_path)

    def parse(self) -> Generator[FileItem, None, None]:
        """Parse the file and return a list of FileItem"""
        is_title = False
        reading = False
        title = ""
        content = ""
        for line in self.lines:
            # Skip empty lines and set reading mode
            if line.startswith("$-----$"):
                reading = not reading

                # If we are reading and we have a title, yield the content
                if is_title and reading:
                    yield FileItem(title=title, content=content)
                    # Reset the content
                    content = ""
                    is_title = False

                continue

            # If we are reading, and title is set, add the line to the content
            elif is_title:
                content += line

            # If we are not reading, set the title
            else:
                title = line
                is_title = True
