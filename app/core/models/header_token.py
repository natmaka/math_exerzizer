""" Un module qui contient le model de l'entete de la requete 

Le but est d'ajouter dans la requete un cookie qui contient la date du jour
pour eviter qu'il ne fasse plusieurs requetes par jour.

Le token doit etre valable pendant 48h pour stocker une variable de combo, s'il
vient plusieurs jours de suite, il doit pouvoir continuer son combo.

Le JWT token doit pouvoir etre refresh pour continuer le combo.

Exemple d'utilisation:

    # Creation du token
    token = HeaderJwtToken()

    # Ajout du token dans la requete
    response = requests.get(
        "http://localhost:5000/question",
        headers={"Authorization": f"Bearer {token.to_jwt_token()}"},
    )

    # Recuperation du token dans la requete
    token = HeaderJwtToken.from_jwt_token(request.headers["Authorization"][7:])

    # Refresh du token
    token.refresh()

    # Verification du token
    token.is_valid()

    # Incrementation du combo
    token.increment_combo()

    # Recuperation du combo
    token.combo
"""
import datetime
import logging
import time
import jwt

from app.core.constants import SECRET_KEY

logger = logging.getLogger(__name__)


class HeaderJwtToken:
    """
    Classe qui créer un JWT token pour l'entete de la requete
    Ainsi qu'un refesh token, il contient un combo qui est incrémenté à chaque
    requete et la date de la dernière requete.
    """

    def __init__(
        self, combo: int = 0, last_request: datetime.datetime = None, timer: int = 0
    ):
        self.combo = combo
        self.last_request = last_request
        self.timer = timer

    def to_dict(self):
        """Convert the object to a dict"""
        return {
            "combo": self.combo,
            "last_request": self.last_request.timestamp()
            if self.last_request
            else None,
            "timer": self.timer,
        }

    def __repr__(self):
        return f"HeaderJwtToken(combo={self.combo}, last_request={self.last_request}, timer={self.timer})"

    @classmethod
    def from_dict(cls, data: dict):
        """Create a HeaderJwtToken object from a dict"""
        try:
            last_request = datetime.datetime.fromtimestamp(data["last_request"])
        except TypeError:
            last_request = None

        return cls(
            combo=data["combo"],
            last_request=last_request,
            timer=data["timer"],
        )

    def to_jwt_token(self):
        """Create a jwt token from the object"""
        return jwt.encode(
            self.to_dict(),
            key=SECRET_KEY,
            algorithm="HS256",
            headers={"alg": "HS256", "typ": "JWT"},
        )

    @classmethod
    def from_jwt_token(cls, token: str):
        """Create a HeaderJwtToken object from a jwt token"""
        data = jwt.decode(token, key=SECRET_KEY, algorithms=["HS256"])
        token = cls.from_dict(data)
        return token

    def refresh(self):
        """Refresh the token"""
        self.last_request = datetime.datetime.now()

    def is_today_submitted(self):
        """
        Return True
        Si une requete a déjà été faite aujourd"hui
        """
        if self.last_request is None:
            return False

        return self.last_request.date() == datetime.datetime.now().date()

    def is_combo_break(self):
        """Return True s'il n'a la date de la dernière requete n'est pas hier"""
        if self.last_request is None:
            return True

        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        return self.last_request.date() != yesterday.date()

    def increment_combo(self):
        """Increment the combo"""
        self.combo += 1

    def start_timer(self):
        """Start the timer"""
        self.timer = time.time()

    def end_timer(self) -> float:
        """End the timer"""
        final_time = time.time() - self.timer
        self.timer = 0

        return final_time
