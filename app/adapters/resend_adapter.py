"""
Module to resend a message to a user
"""
import resend
from app.core.constants import MY_EMAIL, MY_PERSONNAL_EMAIL, RESEND_API_KEY

resend.api_key = RESEND_API_KEY

FROM_ = f"Alex Traveylan <{MY_EMAIL}>"


def html_wraper_for_mail(message: str) -> str:
    """
    wrap a comment in html for mail

    Parameters
    ----------
    message : str
        the message to wrap

    Returns
    -------
    str
        the wrapped message
    """
    return f"""
<html>
<head>
<style>
    body {{
        font-family: Arial, sans-serif;
        background-color: #f2f2f2;
        padding: 20px;
    }}

    p {{
        font-size: 16px;
        color: #333333;
    }}
</style>
</head>
<body>
<p>
{message}
</p>
</body>
</html>
"""


def send_comment_to_mail(
    comment: str, from_: str = FROM_, to: str = MY_PERSONNAL_EMAIL
) -> dict:
    """Send a comment to me by mail

    Parameters
    ----------
    comment : str
        The comment to send

    Returns
    -------
    dict
        The response from the API
    """

    params = {
        "from": from_,
        "to": [to],
        "subject": "Message de DailyMaths",
        "html": comment,
    }

    return resend.Emails.send(params=params)
