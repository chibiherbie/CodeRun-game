import requests
from .config import URL, TOKEN_SITE


def get_user_from_sh(email: str, password: str) -> bool:
    response = requests.post(URL + 'login', data={'email': email, "password": password, 'api': '123'})
    return response.json()['result']


def get_all_money_from_sh() -> dict:
    response = requests.get(URL + f"get_users/{TOKEN_SITE}")
    return response.json()
