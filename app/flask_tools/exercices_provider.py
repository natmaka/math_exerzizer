"""Module to provide exercices"""
import os
from pathlib import Path
from app.adapters.file_read import save_file
from app.core.constants import PROBABILITE_PATH
from app.core.models.exercice import Exercice, ExerciceParser
from app.core.models.prompt import PromptBuider
from app.core.models.completion import completion


class ExercicesProvider:
    """Class to provide exercices"""

    _current_exercice: Exercice = None
    _currend_exercice_id: int = None

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

        # saving exercice
        save_file(
            file_path=PROBABILITE_PATH
            / f"exercice_generated_{cls._currend_exercice_id}.txt",
            content=f"{open_ia_exercice}\n",
        )
