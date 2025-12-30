import json
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import matplotlib
matplotlib.use("Agg")

CHART_DIR = Path("static/charts")
CHART_DIR.mkdir(parents=True, exist_ok=True)

def generate_charts(report_path="output.json"):
    with open(report_path, "r") as f:
        data = json.load(f)

    top_df = pd.DataFrame(data["top_2_restaurants"])
    least_df = pd.DataFrame(data["least_2_restaurants"])

    # Top performers
    plt.figure()
    bars = plt.bar(top_df["restaurant_name"], top_df["total_revenue"])
    plt.title("Top Performing Restaurants")
    plt.ylabel("Total Revenue")

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.2f}",
                ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(CHART_DIR / "top.png")
    plt.close()

    # Least performers
    plt.figure()
    bars = plt.bar(least_df["restaurant_name"], least_df["total_revenue"])
    plt.title("Least Performing Restaurants")
    plt.ylabel("Total Revenue")

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.2f}",
                ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(CHART_DIR / "least.png")
    plt.close()