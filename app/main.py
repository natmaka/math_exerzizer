"""Main module of the app."""
from pathlib import Path
from app.adapters.file_read import save_file
from app.core.constants import PROBABILITE_PATH
from app.core.models.completion import completion

from app.core.models.exercice import Exercice, ExerciceParser
from app.core.models.prompt import PromptBuider


def main():
    """Main function of the app."""
    exemple_1_path = Path("app/data_exercices/probabilite/exercice_1.txt")
    exemple_2_path = Path("app/data_exercices/probabilite/exercice_2.txt")

    parsed_exemple_1 = ExerciceParser(file_path=exemple_1_path).parse()
    parsed_exemple_2 = ExerciceParser(file_path=exemple_2_path).parse()

    exemple_1 = Exercice.from_file(data_parsed=list(parsed_exemple_1))
    exemple_2 = Exercice.from_file(data_parsed=list(parsed_exemple_2))

    prompt_builder = PromptBuider(
        theme="proportionnalité", exemples=[exemple_1, exemple_2]
    )

    prompt = prompt_builder.build()

    open_ia_exercice = completion(prompt=prompt)

    save_file(
        file_path=PROBABILITE_PATH / "exercice_generated_3.txt",
        content=open_ia_exercice,
    )


if __name__ == "__main__":
    main()
