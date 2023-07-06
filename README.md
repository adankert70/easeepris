# easeepris
Kombinerer time for time data i fra Strømpris API med forbruks data i fra Easee API.
Perioden er alltid hele foregående måned.
Sett ditt Easee brukernavn og passord i env vars ```API_USER``` og ```API_PASSWORD``` 

Programmet finner alle ladere assosiert med din konto og rapporterer forbruk per lader samt total.
Region er satt til Norge, NO2.

Start programmet: 

        python3 forbruk.py --region <region>

NB! Ikke verifisert korrekt! Resultatene kan være feil...og priser i fra din leverandør/avtale kan være forskjellige.

Eksempel:
```
python3 forbruk.py --region NO2
Rapport start:  2023-05-01
Rapport slutt:  2023-05-31
Logged on to Easee API!
Pris for lader EH-----9 Lader1        76.86 NOK
Pris for lader EH-----4 Lader2        96.54 NOK
Totalpris for perioden: 173.4 NOK
```