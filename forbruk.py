import sys
import os
import datetime
from easee import autentiser
from easee import chargers
from easee import forbruk
from priser import hentpriser
import argparse
import datetime
import calendar
import csv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--region', type=str,
                        required=True, help='Pris region, f.eks. NO2')
    parser.add_argument('-m', '--month', type=int,
                        required=True, help='Måned nr., feks 11')
    parser.add_argument('-y', '--year', type=int,
                        required=True, help='Årstall')
    parser.add_argument('-c', '--csv', type=str,
                        required=False, help='CSV filename')
    parser.add_argument('-t', '--type', choices=['a', 'n'], type=str,
                        required=False, help='Append eller Ny fil')
    args = parser.parse_args()
    if args.csv and args.type is None:
        parser.error("-c,--csv må ha -t,--type")
    else:
        if args.type == 'a':
            ft = 'a'
        elif args.type == 'n':
            ft = 'w'
    region = args.region
    mnd = args.month
    yr = args.year
    totalpris = 0
    current_date = datetime.date(yr, mnd, 1)
    first_day = current_date.replace(day=1)
    last_day_no = calendar.monthrange(yr, mnd)[1]
    last_day = datetime.date(yr, mnd, last_day_no)
    print("Rapport start: ", first_day)
    print("Rapport slutt: ", last_day)
    priser = hentpriser(yr, mnd, last_day_no, region)
    user = os.getenv('API_USER')
    pwd = os.getenv('API_PASSWORD')
    token = autentiser(user, pwd)
    if not token:
        print("Jeg gir opp, logon feilet...")
        sys.exit()
    print("Logget på Easee API!")
    ladere = chargers(token)
    if not ladere:
        sys.exit()
    for id in ladere.keys():
        idpris = 0
        fjson = forbruk(token, id, first_day,
                        last_day)
        creport = []
        for cjson in fjson:
            consumption = cjson['consumption']
            if consumption == 0:
                continue
            dato = cjson['date']
            factor = priser[dato]
            pris = consumption * factor
            idpris += pris
            creport.append(
                {"date": dato, "consumption": consumption, "price": pris})
        idpris = round(idpris, 2)
        print(f"Pris for lader {id} {ladere[id]}\t{idpris} NOK")
        totalpris += idpris
    totalpris = round(totalpris, 2)
    print(f"Totalpris for perioden:\t{totalpris} NOK")
    fields = ['date', 'consumption', 'price'] 
    with open(args.csv, ft, newline='') as file: 
        writer = csv.DictWriter(file, fieldnames = fields)
        if ft == 'w':
            writer.writeheader()
        writer.writerows(creport)



if __name__ == "__main__":
    main()
