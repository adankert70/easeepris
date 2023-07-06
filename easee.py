import requests
import json


def autentiser(user, pwd):
    url = "https://api.easee.com/api/accounts/login"
    headers = {
        "accept": "application/json",
        "content-type": "application/*+json"
    }
    payload = json.dumps({
        "userName": user,
        "password": pwd
    })

    response = requests.post(url, headers=headers, data=payload)

    if (response.status_code == 200):
        token = "Bearer " + response.json()['accessToken']
        return token
    else:
        print(f"Noe gikk veldig galt. Retur kode {response.status_code}")
        return False


def chargers(token):
    url = "https://api.easee.com/api/chargers"
    headers = {
        "accept": "application/json",
        "Authorization": token
    }
    response = requests.get(url, headers=headers)
    chargers = {}
    if (response.status_code == 200):
        for obj in response.json():
            chargers[obj['id']] = obj['name']
        return chargers
    else:
        print(f"Fant ikke chargers. Retur kode {respons.status_code}")
        return False


def forbruk(token, id, start, slutt):
    url = f"https://api.easee.com/api/chargers/lifetime-energy/{id}/hourly?from={start}&to={slutt}&tz=CET"
    headers = {
        "accept": "application/json",
        "Authorization": token
    }
    response = requests.get(url, headers=headers)
    if (response.status_code == 200):
        return response.json()
    else:
        print(f"Gah, feilet. Fikk ikke hentet data for id {id} på url {url}")
        return False
