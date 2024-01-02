""" This module contains the routes of the application """
import logging
from flask import Flask, request
from flask_cors import CORS
import jwt
from app.adapters.resend_adapter import html_wraper_for_mail, send_comment_to_mail
from app.core.constants import ADMIN_PASSWORD
from app.core.models.header_token import HeaderJwtToken

from app.flask_tools.check_answer import check_answer
from app.flask_tools.exercices_provider import ExercicesProvider

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost*"}})
ExercicesProvider.set_current_exercice()


@app.route("/get_combo", methods=["GET"])
def get_combo():
    """Return the combo"""
    try:
        token = HeaderJwtToken.from_jwt_token(request.headers["Authorization"][7:])
        return {"combo": token.combo}, 200

    except (jwt.exceptions.DecodeError, KeyError):
        return "Unauthorized", 401


@app.route("/check", methods=["GET"])
def check():
    """Vérifie si l'utilisateur a déjà fait une requete aujourd'hui"""
    try:
        token = HeaderJwtToken.from_jwt_token(request.headers["Authorization"][7:])
        if token.is_today_submitted():
            return "Unauthorized", 401

    except (jwt.exceptions.DecodeError, KeyError):
        pass

    return "ok", 200


@app.route("/question", methods=["GET"])
def get_question():
    """Return the current question"""
    try:
        token = HeaderJwtToken.from_jwt_token(request.headers["Authorization"][7:])
    except (jwt.exceptions.DecodeError, KeyError):
        token = HeaderJwtToken()

    token.start_timer()

    exercice = ExercicesProvider.get_current_exercice()
    data = {
        "enonce": exercice.enonce,
        "questions": exercice.questions,
        "token": token.to_jwt_token(),
    }

    return data, 200


@app.route("/first_version", methods=["GET"])
def get_first_version():
    """Return the current question"""
    exercice = ExercicesProvider.get_current_first_version_exercice()
    data = {"enonce": exercice.enonce, "questions": exercice.questions}

    return data, 200


@app.route("/reflexion", methods=["GET"])
def get_reflexion():
    """Return the current question"""
    reflexion = ExercicesProvider.get_current_reflexion()
    data = {"reflexion": reflexion}

    return data, 200


@app.route("/get_nb_propositions", methods=["GET"])
def get_nb_propositions():
    """Return the current question"""
    nb_props = ExercicesProvider.get_nb_propositions()
    nb_bonnes_reponses = ExercicesProvider.nb_bonnes_reponses

    if nb_props == 0:
        pourcentage = 0
    else:
        pourcentage = round(nb_bonnes_reponses / nb_props * 100, 2)

    data = {
        "nb_propositions": nb_props,
        "nb_bonnes_reponses": nb_bonnes_reponses,
        "pourcentage": pourcentage,
    }

    return data, 200


@app.route("/submit", methods=["POST"])
def submit_answer():
    """Submit an answer"""
    exercice = ExercicesProvider.get_current_exercice()
    if request.method == "POST":
        # recuperation de la reponse
        answers = request.get_json()["answers"]

        # Récupération du token dans la requete si il existe
        try:
            token = HeaderJwtToken.from_jwt_token(request.headers["Authorization"][7:])

        except (jwt.exceptions.DecodeError, KeyError):
            # Le token aurait du exister, on le créer sur la landing page
            return "Unauthorized", 401

        # Si une requete a été faite aujourdhui
        if token.is_today_submitted():
            return "Unauthorized", 401

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

        ExercicesProvider.increment_nb_propositions()
        ExercicesProvider.compute_nb_bonnes_reponses(results)
        final_time = token.end_timer()
        hour = int(final_time // 3600)
        minute = int((final_time % 3600) // 60)
        second = int(final_time % 60)
        final_time_formated = f"{hour:02d}:{minute:02d}:{second:02d}"

        # Incrementation du combo
        token.increment_combo()

        # Refresh du token
        token.refresh()

        # Ajout du token dans la reponse
        data["token"] = token.to_jwt_token()
        data["final_time"] = final_time_formated

        return data, 200


@app.route("/create_new_exercice", methods=["POST"])
def create_new_exercice():
    """Create a new exercice"""

    if request.method == "POST":
        admin_password = request.get_json()["admin_password"]

        if admin_password != ADMIN_PASSWORD:
            return "Unauthorized", 401

        ExercicesProvider.create_new_exercice()
        ExercicesProvider.set_current_exercice()
        return "ok", 201


@app.route("/send_email", methods=["POST"])
def send_email():
    """Send an email"""
    if request.method == "POST":
        comment = request.get_json()["comment"]
        comment_html = html_wraper_for_mail(comment)
        api_response = send_comment_to_mail(comment_html)

        logger.info(api_response)
        return "ok", 201
