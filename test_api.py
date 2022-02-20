from lib.Joke_api import joke
import requests


def test_joke(category = 'Any'):
    r = requests.get(
        "https://v2.jokeapi.dev/joke/{}".format(category)
    )
    assert r.status_code == 200