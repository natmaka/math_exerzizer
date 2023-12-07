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
    exemple_3_path = Path("app/data_exercices/probabilite/exercice_3.txt")
    exemple_4_path = Path("app/data_exercices/probabilite/exercice_4.txt")

    parsed_exemple_1 = ExerciceParser(file_path=exemple_1_path).parse()
    parsed_exemple_2 = ExerciceParser(file_path=exemple_2_path).parse()
    parsed_exemple_3 = ExerciceParser(file_path=exemple_3_path).parse()
    parsed_exemple_4 = ExerciceParser(file_path=exemple_4_path).parse()

    exemple_1 = Exercice.from_file(data_parsed=list(parsed_exemple_1))
    exemple_2 = Exercice.from_file(data_parsed=list(parsed_exemple_2))
    exemple_3 = Exercice.from_file(data_parsed=list(parsed_exemple_3))
    exemple_4 = Exercice.from_file(data_parsed=list(parsed_exemple_4))

    exemples = [exemple_1, exemple_2, exemple_3, exemple_4]

    prompt_builder = PromptBuider(theme="proportionnalité", exemples=exemples)

    prompt = prompt_builder.build()

    save_file(
        file_path=PROBABILITE_PATH / "prompt.txt",
        content="\n\n".join([content.get("content") for content in prompt]),
    )

    open_ia_exercice = completion(prompt=prompt)

    save_file(
        file_path=PROBABILITE_PATH / "exercice_generated_2.txt",
        content=open_ia_exercice,
    )


if __name__ == "__main__":
    main()
