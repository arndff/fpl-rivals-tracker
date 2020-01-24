import requests


def auth():
    session = requests.session()
    login_url = 'https://users.premierleague.com/accounts/login/'
    payload = {
        'password': "IvanIvanov90",
        'login': "deuces94@abv.bg",
        'redirect_uri': 'https://fantasy.premierleague.com/a/login',
        'app': 'plfpl-web'
    }

    session.post(login_url, data=payload)

    return session
