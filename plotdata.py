import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime


def get_date(item):
    return datetime.fromisoformat(item["date"])

def plotdata(data):
    # Separate data per lader
    chargers = {}
    for d in data:
        charger = d["charger"]
        if charger not in chargers:
            chargers[charger] = {"date": [], "price": []}
        chargers[charger]["date"].append(datetime.fromisoformat(d["date"]))
        chargers[charger]["price"].append(d["price"])

    # kolonne graf per lader
    for charger, charger_data in chargers.items():
        dates = charger_data["date"]
        price = charger_data["price"]
        plt.bar(dates, price, label=f"{charger} Pris")
    
    # Pene x-axis labels
    date_formatter = DateFormatter("%d-%m")
    plt.gca().xaxis.set_major_formatter(date_formatter)
    plt.xticks(rotation='vertical')
    # lag forståelig plot
    plt.xlabel("Dato")
    plt.ylabel("Pris NOK")
    plt.title("Lader pris")
    plt.legend()

    # Vis plot
    plt.show()