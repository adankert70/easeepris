import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict


def plotdata(data: List[Dict[str, Any]]) -> None:
    """
    Plots the daily consumption price data per charger, stacked.
    """
    if not data:
        print("No data to plot.")
        return

    # Aggregate data per charger and per day
    chargers_daily: Dict[str, Dict[datetime.date, float]] = defaultdict(lambda: defaultdict(float))
    
    for entry in data:
        charger = entry["charger"]
        try:
            dt = datetime.fromisoformat(entry["date"].replace("Z", "+00:00"))
            day = dt.date()
            chargers_daily[charger][day] += entry["price"]
        except (ValueError, KeyError) as e:
            print(f"Error processing entry {entry}: {e}")

    if not chargers_daily:
        print("No valid data processed for plotting.")
        return

    # Identify all unique days and sort them
    all_days = sorted({day for daily in chargers_daily.values() for day in daily.keys()})
    
    # Prepare the plot
    fig, ax = plt.subplots(figsize=(12, 6))

    # Keep track of the bottom height for stacking
    bottoms = [0.0] * len(all_days)

    # Plot each charger's data stacked
    for charger, daily_data in chargers_daily.items():
        # Get prices for each day in the master list, defaulting to 0.0 if no charging occurred
        prices = [daily_data.get(day, 0.0) for day in all_days]
        
        ax.bar(all_days, prices, bottom=bottoms, label=charger, alpha=0.8)
        
        # Update bottoms for the next layer of the stack
        bottoms = [b + p for b, p in zip(bottoms, prices)]
    
    # Format x-axis for daily view
    ax.xaxis.set_major_formatter(DateFormatter("%d-%m"))
    plt.xticks(rotation=45)
    
    ax.set_xlabel("Dato")
    ax.set_ylabel("Total pris per dag (NOK)")
    ax.set_title("Daglig kostnad for lading (stabled)")
    ax.legend()
    
    plt.tight_layout()
    print("Viser daglig stabled plot...")
    plt.show()
