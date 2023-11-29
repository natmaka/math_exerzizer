""" Unit tests for the PromptBuilder class. """
from app.core.models.prompt import PromptBuider


def test_prompt_builder_security():
    """Test the PromptBuilder class for the security prompt"""
    builder = PromptBuider(theme="test", exemples=[])

    prompt = builder._security()

    assert prompt["role"] == "system"
    assert prompt["content"].startswith("<PROMPT")
    assert prompt["content"].endswith("/>")
    assert "SECURITE" in prompt["content"]


def test_prompt_builder_role():
    """Test the PromptBuilder class for the role prompt"""
    builder = PromptBuider(theme="test", exemples=[])

    prompt = builder._role()

    assert prompt["role"] == "system"
    assert prompt["content"].startswith("<PROMPT")
    assert prompt["content"].endswith("/>")
    assert "TON ROLE" in prompt["content"]


def test_prompt_builder_format():
    """Test the PromptBuilder class for the format prompt"""
    builder = PromptBuider(theme="test", exemples=[])

    prompt = builder._format()

    assert prompt["role"] == "system"
    assert prompt["content"].startswith("<PROMPT")
    assert prompt["content"].endswith("/>")
    assert "FORMAT DES EXERCICES" in prompt["content"]
