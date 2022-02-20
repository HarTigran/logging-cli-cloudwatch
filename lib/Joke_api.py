import requests
from time import sleep


def joke( interval = 2, category = 'Any'):
    sleep(interval)
    r = requests.get(
        "https://v2.jokeapi.dev/joke/{}".format(category)
    )
    if r.json()['type'] == 'twopart':
        return r.json()['setup'],r.json()['delivery']
    else:
        return r.json()['joke']