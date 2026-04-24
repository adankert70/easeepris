import sys
import os
import csv
import argparse
from typing import List, Dict

from logic import get_report_data
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
    
    try:
        data = get_report_data(args.year, args.month, args.region)
    except Exception as e:
        print(f"Feil: {e}")
        sys.exit(1)

    print(f"Periode: {data['period']}")
    
    for summary in data['summary']:
        print(f"Lader: {summary['name']}")
        print(f"  Forbruk: {summary['consumption']:.2f} kWh")
        print(f"  Pris:    {summary['price']:.2f} NOK")

    print("-" * 30)
    print(f"TOTAL FORBRUK: {data['total_consumption']:.2f} kWh")
    print(f"TOTAL PRIS:    {data['total_price']:.2f} NOK")

    # Lagre til CSV
    if args.csv and file_mode:
        fields = ['date', 'charger', 'consumption', 'price']
        try:
            file_exists = os.path.isfile(args.csv) and file_mode == 'a'
            with open(args.csv, file_mode, newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                if not file_exists:
                    writer.writeheader()
                writer.writerows(data['daily_entries'])
            print(f"Data lagret til {args.csv}")
        except Exception as e:
            print(f"Skriving til CSV feilet: {e}")
            sys.exit(1)

    # Plot
    if args.plot:
        plotdata(data['daily_entries'])


if __name__ == "__main__":
    main()
