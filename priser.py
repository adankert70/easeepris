import requests
import json
import sys


def hentpriser(year, mnd, maxdag, region):
    mnd = int(str(mnd).zfill(2))
    headers = {
        "accept": "application/json",
        "content-type": "application/*+json"
    }
    priser = {}
    for dag in range(1, maxdag+1):
        dag = str(dag).zfill(2)
        mnd = str(mnd).zfill(2)
        url = f"https://www.hvakosterstrommen.no/api/v1/prices/{year}/{mnd}-{dag}_{region}.json"
        response = requests.get(url, headers=headers)
        # print(response.json())
        if (response.status_code == 200):
            for prisobj in response.json():
                tid = prisobj['time_start']
                pris = prisobj['NOK_per_kWh']
                priser[tid] = pris
        else:
            raise ValueError(
                f"Elendig retur kode for {url}: {response.status_code}")
    return priser
