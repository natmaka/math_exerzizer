""" Unit tests for the PromptBuilder class. """
from app.core.models.prompt import PromptBuider


def test_prompt_builder_role():
    """Test the PromptBuilder class for the role prompt"""
    builder = PromptBuider(theme="test", exemples=[])

    prompt = builder._role()

    assert prompt["role"] == "system"
    assert "TON ROLE" in prompt["content"]


def test_prompt_builder_format():
    """Test the PromptBuilder class for the format prompt"""
    builder = PromptBuider(theme="test", exemples=[])

    prompt = builder._format()

    assert prompt["role"] == "system"
    assert "FORMAT DES EXERCICES" in prompt["content"]
