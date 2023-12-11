from flask import Flask, request
from flask_cors import CORS

from app.flask_tools.check_answer import check_answer
from app.flask_tools.exercices_provider import ExercicesProvider

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
ExercicesProvider.set_current_exercice()


@app.route("/question", methods=["GET"])
def get_question():
    exercice = ExercicesProvider.get_current_exercice()
    data = {"enonce": exercice.enonce, "questions": exercice.questions}

    return data, 200


@app.route("/submit", methods=["POST"])
def submit_answer():
    exercice = ExercicesProvider.get_current_exercice()
    if request.method == "POST":
        # recuperation de la reponse
        answers = request.get_json()["answers"]

        is_valid = check_answer(answers=answers, correct_answer=exercice.reponses)

        if is_valid is not None:
            return is_valid

        answers = [float(answer) for answer in answers]

        results = [ans == float(rep) for ans, rep in zip(answers, exercice.reponses)]

        data = {
            "answers": answers,
            "results": results,
            "explications": exercice.explications,
        }

        return data, 200


@app.route("/create_new_exercice", methods=["GET"])
def create_new_exercice():
    """Create a new exercice"""
    ExercicesProvider.create_new_exercice()
    ExercicesProvider.set_current_exercice()
    return "ok", 201
