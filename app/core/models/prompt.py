"""Prompt builder"""
from io import StringIO
from typing import Literal
from app.core.app_types import OpenAiMessage

from app.core.constants import UNDERLINE
from app.core.models.exercice import Exercice


class PromptBuider:
    """Prompt builder"""

    def __init__(self, theme: Literal["probabilites"], exemples: list[Exercice]):
        self.theme = theme
        self.exemples = exemples

    def build(self) -> list[OpenAiMessage]:
        """Build the prompt"""

        prompt = []
        prompt.append(self._role())
        prompt.append(self._format())
        for exemple in self.exemples:
            prompt.append(exemple.to_openai_prompt())

        return prompt

    def _role(self) -> OpenAiMessage:
        """Return a role prompt"""

        role_prompt = StringIO()
        role_prompt.write(f"TON ROLE/n{UNDERLINE}")
        role_prompt.write("Tu dois générer des exercices de mathématiques.\n")
        role_prompt.write("Destinés à des élèves de 4ème (13ans)\n")
        role_prompt.write(f"Sur le thème: {self.theme}\n")

        return OpenAiMessage(role="system", content=role_prompt.getvalue())

    def _format(self) -> OpenAiMessage:
        """Return a format prompt"""

        format_prompt = StringIO()
        format_prompt.write(f"FORMAT DES EXERCICES\n{UNDERLINE}")
        format_prompt.write("Tu trouveras le format avec lequel tu devras répondre\n")
        format_prompt.write("Entre les balises <format><format/>\n")
        format_prompt.write("<format>\n")
        format_prompt.write(f"{UNDERLINE}")
        format_prompt.write(f"ENONCE\n{UNDERLINE}L'énoncé de l'exercice\n")
        format_prompt.write(f"{UNDERLINE}")
        format_prompt.write(f"QUESTION 1\n{UNDERLINE}La question 1\n")
        format_prompt.write(f"{UNDERLINE}")
        format_prompt.write(f"QUESTION 2\n{UNDERLINE}La question 2\n")
        format_prompt.write("...\n")
        format_prompt.write(f"{UNDERLINE}")
        format_prompt.write(f"QUESTION i\n{UNDERLINE}La question i\n")
        format_prompt.write(f"{UNDERLINE}")
        format_prompt.write(f"REPONSE 1\n{UNDERLINE}La réponse 1\n")
        format_prompt.write(f"{UNDERLINE}")
        format_prompt.write(f"EXPLICATION 1\n{UNDERLINE}L'explication 1\n")
        format_prompt.write(f"{UNDERLINE}")
        format_prompt.write(f"REPONSE 2\n{UNDERLINE}La réponse 2\n")
        format_prompt.write(f"{UNDERLINE}")
        format_prompt.write(f"EXPLICATION 2\n{UNDERLINE}L'explication 2\n")
        format_prompt.write("...\n")
        format_prompt.write(f"{UNDERLINE}")
        format_prompt.write(f"REPONSE i\n{UNDERLINE}La réponse i\n")
        format_prompt.write(f"{UNDERLINE}")
        format_prompt.write(f"EXPLICATION i\n{UNDERLINE}L'explication i\n")
        format_prompt.write(f"{UNDERLINE}")
        format_prompt.write("<format/>\n")

        return OpenAiMessage(role="system", content=format_prompt.getvalue())
