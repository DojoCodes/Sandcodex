from connexion.exceptions import OAuthProblem
from flask import current_app
import sys


def is_key_exists(token):
    if "API_KEYS" not in current_app.config:
        return False
    keys = current_app.config["API_KEYS"].replace(" ", "").split(",")
    return token in keys


def apikey_auth(token, required_scopes):
    if not is_key_exists(token):
        raise OAuthProblem('Invalid token')

    return {
        "uid": 1
    }