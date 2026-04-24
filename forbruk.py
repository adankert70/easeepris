import sys
import os
import datetime
import calendar
import csv
import argparse
from typing import List, Dict, Optional

from easee import EaseeClient
from priser import hentpriser
from plotdata import plotdata
from dotenv import load_dotenv


def main() -> None:
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Hent forbruk og priser for Easee ladere.")
    parser.add_argument('-r', '--region', type=str, required=True, 
                        help='Pris region, f.eks. NO2')
    parser.add_argument('-m', '--month', type=int, required=True, 
                        help='Måned nr., feks 11')
    parser.add_argument('-y', '--year', type=int, required=True, 
                        help='Årstall')
    parser.add_argument('-c', '--csv', type=str, required=False, 
                        help='CSV filename')
    parser.add_argument('-t', '--type', choices=['a', 'n'], type=str, required=False, 
                        help='Append (a) eller Ny fil (n)')
    parser.add_argument('-p', '--plot', action='store_true', required=False, 
                        help='Plot en rapport')
    
    args = parser.parse_args()

    if args.csv and args.type is None:
        parser.error("-c/--csv krever -t/--type (a for append, n for ny fil)")

    file_mode = 'a' if args.type == 'a' else 'w' if args.type == 'n' else None
    
    region = args.region
    mnd = args.month
    yr = args.year
    
    print(f"Periode: {yr}-{str(mnd).zfill(2)}")
    
    current_date = datetime.date(yr, mnd, 1)
    now = datetime.datetime.now()
    
    first_day = current_date.replace(day=1)
    _, last_day_in_month = calendar.monthrange(yr, mnd)
    
    if yr == now.year and mnd == now.month:
        last_day_no = now.day
        print(f"Rapport for inneværende måned. Bruker dag 1 til {last_day_no}.")
    else:
        last_day_no = last_day_in_month

    last_day = datetime.date(yr, mnd, last_day_no)
    print(f"Rapport start: {first_day}")
    print(f"Rapport slutt: {last_day}")

    # Hent priser
    try:
        priser = hentpriser(yr, mnd, last_day_no, region)
    except ValueError as e:
        print(f"Feil ved henting av priser: {e}")
        sys.exit(1)

    # Easee API klient
    client = EaseeClient()
    user = os.getenv('API_USER')
    pwd = os.getenv('API_PASSWORD')
    
    if not user or not pwd:
        print("API_USER eller API_PASSWORD er ikke satt i .env eller miljøet.")
        sys.exit(1)

    if not client.authenticate(user, pwd):
        print("Logon feilet. Sjekk legitimasjon.")
        sys.exit(1)
        
    print("Logget på Easee API!")
    
    ladere = client.get_chargers()
    if not ladere:
        print("Fant ingen ladere.")
        sys.exit(1)

    report_data: List[Dict] = []
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
                # Noen ganger kan det mangle priser for fremtidige timer eller lignende
                continue
                
            pris = consumption * factor
            id_pris += pris
            id_forbruk += consumption
            
            report_data.append({
                "date": dato, 
                "charger": lader_navn, 
                "consumption": consumption, 
                "price": pris
            })
        
        print(f"Lader: {lader_navn} ({lader_id})")
        print(f"  Forbruk: {id_forbruk:.2f} kWh")
        print(f"  Pris:    {id_pris:.2f} NOK")
        
        total_forbruk += id_forbruk
        total_pris += id_pris

    print("-" * 30)
    print(f"TOTAL FORBRUK: {total_forbruk:.2f} kWh")
    print(f"TOTAL PRIS:    {total_pris:.2f} NOK")

    # Lagre til CSV
    if args.csv and file_mode:
        fields = ['date', 'charger', 'consumption', 'price']
        try:
            file_exists = os.path.isfile(args.csv) and file_mode == 'a'
            with open(args.csv, file_mode, newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                if not file_exists:
                    writer.writeheader()
                writer.writerows(report_data)
            print(f"Data lagret til {args.csv}")
        except Exception as e:
            print(f"Skriving til CSV feilet: {e}")
            sys.exit(1)

    # Plot
    if args.plot:
        plotdata(report_data)


if __name__ == "__main__":
    main()
