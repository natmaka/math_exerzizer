""" Unit tests for the SecurePrompt class."""
from app.core.app_types import SecurePrompt


def test_secure_prompt_add_lines():
    """Test the SecurePrompt class"""
    prompt_to_test = SecurePrompt(role="system", content="test\n")

    lines = prompt_to_test.prompt["content"].split("\n")

    assert len(lines) == 3
    assert ">" in lines[0] and "<PROMPT" in lines[0]
    assert lines[1] == "test"
    assert "/>" in lines[2] and "<PROMPT" in lines[2]
