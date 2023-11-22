"""
Test the exercice parser
Author: Alex Traveylan
Date: 22-11-2023
"""
from app.core.app_types import FileItem
from app.core.models.exercice import Exercice, ExerciceParser


def test_exercice_parseur(exercice_test):
    """Test the exercice parser"""

    expected_result = [
        FileItem(title="ENONCE", content="test1"),
        FileItem(title="QUESTION 1", content="test2"),
        FileItem(title="QUESTION 2", content="test3"),
        FileItem(title="REPONSE 1", content="test4"),
        FileItem(title="REPONSE 2", content="test5"),
    ]

    parseur = ExerciceParser(file_path=exercice_test)
    results = parseur.parse()

    compare_tuple = zip(results, expected_result)

    assert all(result.title == expected.title for result, expected in compare_tuple)
    assert all(result.content == expected.content for result, expected in compare_tuple)


def test_exercice_builder():
    """Test the exercice builder"""

    expected_result = Exercice(
        enonce="test1",
        questions=["test2", "test3"],
        reponses=["test4", "test5"],
    )

    parser_result = [
        FileItem(title="ENONCE", content="test1"),
        FileItem(title="QUESTION 1", content="test2"),
        FileItem(title="QUESTION 2", content="test3"),
        FileItem(title="REPONSE 1", content="test4"),
        FileItem(title="REPONSE 2", content="test5"),
    ]

    exercice = Exercice.from_file(data_parsed=parser_result)

    assert exercice.enonce == expected_result.enonce

    questions_tuple = zip(exercice.questions, expected_result.questions)

    assert all(question == expected for question, expected in questions_tuple)

    reponses_tuple = zip(exercice.reponses, expected_result.reponses)

    assert all(reponse == expected for reponse, expected in reponses_tuple)
