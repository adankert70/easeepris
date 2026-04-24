# easeepris
Reports the cost of charging via an Easee charger for a specified month and price region.

Combines hourly data from the [Hva koster strømmen? API](https://www.hvakosterstrommen.no/strompris-api) with consumption data from the Easee API.

## Setup

1. **Create a virtual environment:**
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure credentials:**
   Copy `.env.example` to `.env` and enter your Easee username and password:
   ```env
   API_USER=your_username
   API_PASSWORD=your_password
   ```

## Usage

The program finds all chargers associated with your account and reports the consumption per charger as well as the total.

```powershell
python forbruk.py -r REGION -m MONTH -y YEAR [-c CSV] [-t {a,n}] [-p]
```

### Arguments:
- `-h, --help`: Show help message.
- `-r, --region REGION`: Price region (e.g., `NO1`, `NO2`, `NO3`, `NO5`).
- `-m, --month MONTH`: Month number (e.g., `11`).
- `-y, --year YEAR`: Year (e.g., `2024`).
- `-c, --csv CSV`: CSV filename for export.
- `-t, --type {a,n}`: Use `a` for append or `n` for a new file (overwrite).
- `-p, --plot`: Show a graphical report of the consumption.

### Example:
```powershell
python forbruk.py --region NO2 -m 4 -y 2026 -p
```

## Disclaimer
Note: The results are not verified for accuracy. Actual prices from your electricity provider may vary depending on your specific contract.

## Plot
If `-p` is used, a graph showing the cost of consumption aggregated by day is displayed.
