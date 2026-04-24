import os
import datetime
import calendar
from typing import List, Dict, Any, Tuple

from easee import EaseeClient
from priser import hentpriser


def get_report_data(year: int, month: int, region: str) -> Dict[str, Any]:
    """
    Fetches consumption data from Easee and price data, then aggregates it.
    Returns a dictionary suitable for JSON serialization.
    """
    current_date = datetime.date(year, month, 1)
    now = datetime.datetime.now()
    
    first_day = current_date.replace(day=1)
    _, last_day_in_month = calendar.monthrange(year, month)
    
    if year == now.year and month == now.month:
        last_day_no = now.day
    else:
        last_day_no = last_day_in_month

    last_day = datetime.date(year, month, last_day_no)

    # Fetch prices
    priser = hentpriser(year, month, last_day_no, region)

    # Easee API client
    client = EaseeClient()
    user = os.getenv('API_USER')
    pwd = os.getenv('API_PASSWORD')
    
    if not user or not pwd:
        raise ValueError("API_USER or API_PASSWORD not set in environment.")

    if not client.authenticate(user, pwd):
        raise ConnectionError("Authentication with Easee failed.")
        
    ladere = client.get_chargers()
    if not ladere:
        return {
            "summary": [],
            "daily_data": [],
            "total_consumption": 0,
            "total_price": 0,
            "period": f"{year}-{str(month).zfill(2)}"
        }

    report_entries: List[Dict[str, Any]] = []
    charger_summaries: Dict[str, Dict[str, Any]] = {}

    total_pris = 0.0
    total_forbruk = 0.0

    for lader_id, lader_navn in ladere.items():
        id_pris = 0.0
        id_forbruk = 0.0
        
        forbruk_data = client.get_consumption(lader_id, str(first_day), str(last_day))
        
        for entry in forbruk_data:
            consumption = entry['consumption']
            if consumption <= 0:
                continue
            
            dato = entry['date']
            factor = priser.get(dato)
            
            if factor is None:
                continue
                
            pris = consumption * factor
            id_pris += pris
            id_forbruk += consumption
            
            report_entries.append({
                "date": dato, 
                "charger": lader_navn, 
                "consumption": consumption, 
                "price": pris
            })
        
        charger_summaries[lader_id] = {
            "name": lader_navn,
            "consumption": round(id_forbruk, 2),
            "price": round(id_pris, 2)
        }
        
        total_forbruk += id_forbruk
        total_pris += id_pris

    return {
        "period": f"{year}-{str(month).zfill(2)}",
        "summary": list(charger_summaries.values()),
        "daily_entries": report_entries,
        "total_consumption": round(total_forbruk, 2),
        "total_price": round(total_pris, 2)
    }
