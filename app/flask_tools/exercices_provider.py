"""Module to provide exercices"""
import logging
import os
from pathlib import Path
from app.adapters.file_read import save_file
from app.core.constants import PROBABILITE_PATH
from app.core.models.exercice import Exercice, ExerciceParser
from app.core.models.prompt import PromptBuider
from app.core.models.completion import completion
from app.core.models.thinking import Thinking
from app.core.models.verif import verif_exercice

logger = logging.getLogger(__name__)


class ExercicesProvider:
    """Class to provide exercices"""

    _current_exercice: Exercice = None
    _currend_exercice_id: int = None
    _nb_propositions: int = 0
    nb_bonnes_reponses: int = 0

    @classmethod
    def compute_nb_bonnes_reponses(cls, results: list[bool]) -> None:
        """Compute the number of good answers"""
        all_ok = all(results)

        if all_ok:
            cls.nb_bonnes_reponses += 1

    @classmethod
    def get_nb_propositions(cls) -> int:
        """Return the number of propositions"""
        return cls._nb_propositions

    @classmethod
    def increment_nb_propositions(cls) -> None:
        """Increment the number of propositions"""
        cls._nb_propositions += 1

    @classmethod
    def get_current_first_version_exercice(cls) -> Exercice:
        """Return the first version of the current exercice"""

        first_version_path = (
            Path(__file__).parent.parent
            / "data_exercices"
            / "probabilite"
            / "generated"
            / "first_versions"
            / f"exercice_generated_{cls._currend_exercice_id}.txt"
        )

        parsed_first_version = ExerciceParser(file_path=first_version_path).parse()
        first_version = Exercice.from_file(data_parsed=list(parsed_first_version))

        return first_version

    @classmethod
    def get_current_reflexion(cls) -> str:
        """Return the reflexion of the current exercice"""

        reflexion_path = (
            Path(__file__).parent.parent
            / "data_exercices"
            / "probabilite"
            / "generated"
            / "motifs"
            / f"motif_{cls._currend_exercice_id}.txt"
        )

        with open(reflexion_path, "r", encoding="utf-8") as file:
            reflexion = file.read()

        return reflexion

    @classmethod
    def get_current_exercice(cls) -> Exercice:
        """Return the current exercice"""
        return cls._current_exercice

    @classmethod
    def set_current_exercice(cls) -> None:
        """Set the current exercice"""

        exercices = os.listdir("app/data_exercices/probabilite/generated")
        exercices_ids = [
            int(exercice.split(".")[0].split("_")[-1])
            for exercice in exercices
            if exercice.startswith("exercice_generated")
        ]

        cls._currend_exercice_id = max(exercices_ids)

        last_exercice_path = (
            Path(__file__).parent.parent
            / "data_exercices"
            / "probabilite"
            / "generated"
            / f"exercice_generated_{cls._currend_exercice_id}.txt"
        )

        parsed_last_exercice = ExerciceParser(file_path=last_exercice_path).parse()
        last_exercice = Exercice.from_file(data_parsed=list(parsed_last_exercice))

        cls._current_exercice = last_exercice
        cls._nb_propositions = 0
        cls.nb_bonnes_reponses = 0

    @classmethod
    def create_new_exercice(cls):
        """Create a new exercice"""

        # database of exercices
        exemple_1_path = Path("app/data_exercices/probabilite/exercice_1.txt")
        exemple_2_path = Path("app/data_exercices/probabilite/exercice_2.txt")
        exemple_3_path = Path("app/data_exercices/probabilite/exercice_3.txt")
        exemple_4_path = Path("app/data_exercices/probabilite/exercice_4.txt")

        # parsing of exercices
        parsed_exemple_1 = ExerciceParser(file_path=exemple_1_path).parse()
        parsed_exemple_2 = ExerciceParser(file_path=exemple_2_path).parse()
        parsed_exemple_3 = ExerciceParser(file_path=exemple_3_path).parse()
        parsed_exemple_4 = ExerciceParser(file_path=exemple_4_path).parse()

        # making objects of exercices
        exemple_1 = Exercice.from_file(data_parsed=list(parsed_exemple_1))
        exemple_2 = Exercice.from_file(data_parsed=list(parsed_exemple_2))
        exemple_3 = Exercice.from_file(data_parsed=list(parsed_exemple_3))
        exemple_4 = Exercice.from_file(data_parsed=list(parsed_exemple_4))

        # list of exercices
        exemples = [exemple_1, exemple_2, exemple_3, exemple_4]

        # creating prompt
        prompt_builder = PromptBuider(theme="proportionnalité", exemples=exemples)

        # building prompt
        prompt = prompt_builder.build()

        # openai completion
        open_ia_exercice = completion(prompt=prompt)

        # incrementing exercice id
        cls._currend_exercice_id += 1

        # verif exercice
        corrected_exercice = verif_exercice(open_ia_exercice)

        # saving exercice
        save_file(
            file_path=PROBABILITE_PATH
            / "first_versions"
            / f"exercice_generated_{cls._currend_exercice_id}.txt",
            content=f"{corrected_exercice}",
        )

        logger.info("First version of exercice generated")

        # thinking
        thinking = Thinking(prompt, open_ia_exercice)
        thinking_prompt = thinking.thinking_prompt()
        reflexion = thinking.get_reflexion(thinking_prompt)

        logger.info("Reflexion generated")

        # saving reflexion
        save_file(
            file_path=PROBABILITE_PATH
            / "motifs"
            / f"motif_{cls._currend_exercice_id}.txt",
            content=reflexion.get("content"),
        )

        beter_exercice = thinking.get_reformat(reflexion)

        # verif exercice
        beter_exercice_verified = verif_exercice(beter_exercice)

        # saving exercice
        save_file(
            file_path=PROBABILITE_PATH
            / f"exercice_generated_{cls._currend_exercice_id}.txt",
            content=beter_exercice_verified,
        )

        logger.info("Second version of exercice generated")
