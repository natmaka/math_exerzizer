from flask import Flask, render_template, request
import os
from pathlib import Path

from app.core.models.exercice import Exercice, ExerciceParser

app = Flask(__name__)

exercices = os.listdir("app/data_exercices/probabilite/generated")
exercices = [
    int(exercice.split(".")[0].split("_")[-1])
    for exercice in exercices
    if exercice.startswith("exercice_generated")
]

LAST_EXERCICE_PATH = (
    Path(__file__).parent
    / "data_exercices"
    / "probabilite"
    / "generated"
    / f"exercice_generated_{max(exercices)}.txt"
)

PARSED_LAST_EXERCICE = ExerciceParser(file_path=LAST_EXERCICE_PATH).parse()
LAST_EXERCICE = Exercice.from_file(data_parsed=list(PARSED_LAST_EXERCICE))


@app.route("/", methods=["GET"])
def main_page():
    return render_template(
        "question.html",
        enonce=LAST_EXERCICE.enonce,
        question=LAST_EXERCICE.questions[0],
    )


@app.route("/submit-answer", methods=["POST"])
def submit_answer():
    if request.method == "POST":
        print(request.form)
        answer = int(request.form["answer"])

        print(LAST_EXERCICE.reponses[0])

        if answer == int(LAST_EXERCICE.reponses[0]):
            message = "Bravo !"

        else:
            message = "Mauvaise réponse"

        return render_template(
            "answer.html",
            answer=answer,
            message=message,
            explication=LAST_EXERCICE.explications[0],
        )
