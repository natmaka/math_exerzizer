""" Unit tests for the SecurePrompt class."""
from app.core.app_types import EncapsulatePrompt


def test_encapsulate_prompt_add_lines():
    """Test the SecurePrompt class"""
    prompt_to_test = EncapsulatePrompt(content="test\n", capsule="PROMPT")

    lines = prompt_to_test.prompt["content"].split("\n")

    assert len(lines) == 3
    assert ">" in lines[0] and "<PROMPT" in lines[0]
    assert lines[1] == "test"
    assert "/>" in lines[2] and "<PROMPT" in lines[2]
