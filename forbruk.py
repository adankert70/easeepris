import sys
import os
import datetime
from easee import autentiser
from easee import chargers
from easee import forbruk
from priser import hentpriser

def main():
    totalpris = 0
    current_date = datetime.date.today()
    first_day_current_month = current_date.replace(day=1)
    last_day_previous_month = first_day_current_month - datetime.timedelta(days=1)
    first_day_previous_month = last_day_previous_month.replace(day=1)
    last_month = first_day_previous_month.month
    year = first_day_previous_month.year
    last_day = last_day_previous_month.day
    #print(f"Måned: {last_month}")
    #print(f"Siste dag: {last_day}")
    #print(f"År: {year}")
    print("Start: ", first_day_previous_month)
    print("Slutt: ", last_day_previous_month)
    priser = hentpriser(year,last_month,last_day)
    user = os.getenv('API_USER')
    pwd = os.environ.get('API_PASSWORD')
    token = autentiser(user,pwd)
    if not token:
        print("Jeg gir opp...")
        sys.exit()
    #print (f"Fikk token! {token}")
    print("Logged on!")
    ladere = chargers(token)
    if not chargers:
        sys.exit()
    fogp = {}
    for id in ladere.keys():
        idpris = 0
        #print(f"id: {id}\tNavn: {ladere[id]}")
        fjson = forbruk(token,id,first_day_previous_month,last_day_previous_month)
        ## Parse JSON, find the consumptions by Hour
        creport = []
        for cjson in fjson:
            #print(cjson)
            consumption = cjson['consumption']
            if consumption == 0:
                continue
            dato = cjson['date']
            factor = priser[dato]
            #print(f"Factor: {factor}")
            pris = consumption * factor # Pris må finnes...
            #print(f"Pris for {dato}:forbruk {consumption} {pris}")
            idpris += pris
            creport.append({"date": dato, "consumption": consumption, "price": pris})
        fogp[id] = creport
        idpris = round(idpris,2)
        print(f"Pris for lader {id} {ladere[id]}\t{idpris}")
        totalpris += idpris
    #print(fogp)
    totalpris = round(totalpris,2)
    print(f"Totalpris for perioden:\t{totalpris}")

if __name__ == "__main__":
    main()