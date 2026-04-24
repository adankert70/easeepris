import requests
import json
from typing import Dict, Union, Optional, List


class EaseeClient:
    BASE_URL = "https://api.easee.com/api"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "content-type": "application/*+json"
        })
        self.token: Optional[str] = None

    def authenticate(self, user: str, pwd: str) -> bool:
        url = f"{self.BASE_URL}/accounts/login"
        payload = json.dumps({
            "userName": user,
            "password": pwd
        })

        try:
            response = self.session.post(url, data=payload)
            response.raise_for_status()
            
            self.token = f"Bearer {response.json()['accessToken']}"
            self.session.headers.update({"Authorization": self.token})
            return True
        except requests.exceptions.RequestException as e:
            print(f"Authentication failed: {e}")
            return False

    def get_chargers(self) -> Dict[str, str]:
        if not self.token:
            print("Client not authenticated.")
            return {}

        url = f"{self.BASE_URL}/chargers"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            return {obj['id']: obj['name'] for obj in response.json()}
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch chargers: {e}")
            return {}

    def get_consumption(self, charger_id: str, start_date: str, end_date: str) -> List[Dict]:
        if not self.token:
            print("Client not authenticated.")
            return []

        # Assuming CET timezone as in original code
        url = f"{self.BASE_URL}/chargers/lifetime-energy/{charger_id}/hourly"
        params = {
            "from": start_date,
            "to": end_date,
            "tz": "CET"
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch consumption for {charger_id}: {e}")
            return []


# Keep original functions for backward compatibility (optional, but good for now)
def autentiser(user, pwd):
    client = EaseeClient()
    if client.authenticate(user, pwd):
        return client.token
    return False


def chargers(token):
    client = EaseeClient()
    client.token = token
    client.session.headers.update({"Authorization": token})
    return client.get_chargers()


def forbruk(token, id, start, slutt):
    client = EaseeClient()
    client.token = token
    client.session.headers.update({"Authorization": token})
    return client.get_consumption(id, str(start), str(slutt))
