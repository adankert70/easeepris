import requests
from typing import Dict


def hentpriser(year: int, mnd: int, maxdag: int, region: str) -> Dict[str, float]:
    formatted_mnd = str(mnd).zfill(2)
    headers = {
        "accept": "application/json",
        "content-type": "application/*+json"
    }
    priser = {}
    
    with requests.Session() as session:
        session.headers.update(headers)
        
        for dag in range(1, maxdag + 1):
            formatted_dag = str(dag).zfill(2)
            url = f"https://www.hvakosterstrommen.no/api/v1/prices/{year}/{formatted_mnd}-{formatted_dag}_{region}.json"
            
            try:
                response = session.get(url)
                response.raise_for_status()
                
                for prisobj in response.json():
                    tid = prisobj['time_start']
                    pris = prisobj['NOK_per_kWh']
                    priser[tid] = pris
                    
            except requests.exceptions.RequestException as e:
                print(f"Failed to fetch prices for {url}: {e}")
                raise ValueError(f"Error fetching data from {url}")
                
    return priser
