"""Module de verification de la reponse de l'utilisateur"""


def check_answer(
    answers: list[str], correct_answer: list[float]
) -> tuple[str, int] | None:
    """Verification de la reponse de l'utilisateur

    Parameters
    ----------
    answers : list[str]
        Reponses de l'utilisateur
    correct_answer : list[float]
        Reponses correctes

    Returns
    -------
    tuple[str, int] | None
        Reponse de l'utilisateur si elle est incorrecte, None sinon
    """
    # verification du format list de la reponse
    is_array = isinstance(answers, list)
    if not is_array:
        return "Bad request", 400
    # verification du type de la reponse
    try:
        [float(answer) for answer in answers]
    except ValueError:
        return "Values must be numbers", 400

    # verification du nombre de reponses
    if len(answers) != len(correct_answer):
        return f"You must send {len(correct_answer)} data", 400

    return None
