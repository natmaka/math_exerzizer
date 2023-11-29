"""OpenAI Completion Model."""
from openai import OpenAI
from app.core.app_types import OpenAiMessage
from app.core.constants import OPENAI_API_KEY


def completion(prompt: list[OpenAiMessage]):
    """Send a prompt to the OpenAI API and return the response.

    Parameters
    ----------
    prompt : list[OpenAiMessage]
        The prompt to send to the API.

    Returns
    -------
    str
        The response from the API.
    """

    client = OpenAI(api_key=OPENAI_API_KEY)

    chat_completion = client.chat.completions.create(messages=prompt, model="gpt-4")

    return chat_completion.choices[0].message.content
