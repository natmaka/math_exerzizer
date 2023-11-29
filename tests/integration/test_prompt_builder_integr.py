""" Integration tests for the prompt builder. """

from app.core.models.prompt import PromptBuider


def test_prompt_builder():
    """Test the PromptBuilder class"""
    builder = PromptBuider(theme="test", exemples=[])

    prompt = builder.build()

    assert len(prompt) == 3
    assert all(isinstance(item, dict) for item in prompt)
