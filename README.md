# easeepris
Kombinerer time for time data i fra Strømpris API med forbruks data i fra Easee API.
Perioden er alltid hele foregående måned.
Sett ditt Easee brukernavn og passord i env vars API_USER og API_PASSWORD 

Programmet finner alle ladere assosiert med din konto og rapporterer forbruk per lader samt total.

Start programmet: python3 forbruk.py

NB! Ikke verifisert korrekt! Resultatene kan være feil...og priser i fra din leverandør/avtale kan være forskjellige.