"""Thinking model"""
from io import StringIO
from app.core.app_types import OpenAiMessage
from app.core.constants import SEPARATOR
from app.core.models.completion import completion
import logging

logger = logging.getLogger(__name__)


class Thinking:
    """Force openai to think and produce a beter exercice"""

    def __init__(self, initial_prompt: list[OpenAiMessage], generated_exercice: str):
        self.initial_prompt = initial_prompt
        self.generated_exercice = generated_exercice

    def get_thinking_fruit(self) -> str:
        """Return a thinking fruit"""

        thinking_prompt = self._thinking_prompt()
        reflexion = self._get_reflexion(thinking_prompt)
        logger.info(reflexion.get("content"))
        reformat_response = self._get_reformat(reflexion)

        return reformat_response

    def _thinking_prompt(self) -> OpenAiMessage:
        """Return a thinking prompt"""

        thinking_prompt = StringIO()
        thinking_prompt.write(f"TON ROLE\n{SEPARATOR}")
        thinking_prompt.write("Regarde cet exercice en tant qu'un élève de 4ème\n")
        thinking_prompt.write(f"EXERCICE\n{SEPARATOR}")
        thinking_prompt.write(f"{self.generated_exercice}\n")
        thinking_prompt.write(f"REFLECHI\n{SEPARATOR}")
        thinking_prompt.write("Est-ce que tu comprends l'énoncé et les questions ?\n")
        thinking_prompt.write("Est-ce que les reponses te semblent correspondre ?\n")
        thinking_prompt.write("Est-ce que les explications sont claire\n")

        return OpenAiMessage(role="system", content=thinking_prompt.getvalue())

    def _get_reflexion(self, thinking_prompt: OpenAiMessage) -> OpenAiMessage:
        """Return a reflexion prompt"""

        response = completion([thinking_prompt])

        if response is None:
            raise ValueError("OpenAI API is not responding")

        return OpenAiMessage(role="assistant", content=response)

    def _get_reformat(self, reflexion: OpenAiMessage) -> str:
        """Return a reformat prompt"""

        prompt = [*self.initial_prompt]
        exercice_p = OpenAiMessage(role="system", content=self.generated_exercice)
        prompt.append(exercice_p)

        new_system_prompt = StringIO()
        new_system_prompt.write(f"CONSIGNE SUPPLEMENTAIRE\n{SEPARATOR}")
        new_system_prompt.write("Voici les remarques d'un eleve de 4eme :\n")
        new_system_prompt.write("prends en compte ses remarques\n")
        new_system_prompt.write("et reformule ton exercice si necessaire\n")
        new_system_prompt.write(f"REMARQUES DE L'ELEVE\n{SEPARATOR}")
        new_system_prompt.write(f"{reflexion.get('content')}\n")
        new_system_prompt.write(f"FORMAT DE TA REPONSE\n{SEPARATOR}")
        new_system_prompt.write(
            "Répond en utilisant strictement le format d'exercice\n"
        )
        new_system_prompt.write(
            f"Respecte les '{SEPARATOR}' contenus, n'ajoute pas de balises '<></>'\n"
        )

        prompt.append(
            OpenAiMessage(role="system", content=new_system_prompt.getvalue())
        )

        response = completion(prompt)

        return response
