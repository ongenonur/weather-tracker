import os
import pandas as pd
import matplotlib.pyplot as plt

def generate_daily_plots(csv_path="pisac_weather_log.csv", output_dir="plots"):
    if not os.path.exists(csv_path):
        print(f"CSV file '{csv_path}' not found.")
        return

    # Load data and convert timestamp column
    df = pd.read_csv(csv_path)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    df["Date"] = df["Timestamp"].dt.date

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # API color mapping for consistent daily charts
    api_colors = {
        "OpenMeteo_Temp": "#3498db",   # Blue
        "OpenWeather_Temp": "#e74c3c", # Red
        "WeatherAPI_Temp": "#2ecc71",  # Green
        "TomorrowIO_Temp": "#9b59b6",  # Purple
        "MeteoBlue_Temp": "#f39c12"    # Orange
    }

    # Group by each date and render a graph
    grouped = df.groupby("Date")
    for date, group in grouped:
        plt.figure(figsize=(10, 5))
        
        for col, color in api_colors.items():
            if col in group.columns:
                # Pretty column name for legend (e.g., OpenMeteo_Temp -> OpenMeteo)
                label_name = col.replace("_Temp", "")
                plt.plot(
                    group["Timestamp"], 
                    group[col], 
                    marker="o", 
                    linewidth=2, 
                    color=color, 
                    label=label_name
                )

        plt.title(f"Pisac Weather Comparison — {date}", fontsize=14, fontweight="bold")
        plt.xlabel("Time of Day", fontsize=11)
        plt.ylabel("Temperature (°C)", fontsize=11)
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend(title="Weather API", loc="best")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save graph for each specific date
        filename = os.path.join(output_dir, f"weather_{date}.png")
        plt.savefig(filename, dpi=300)
        plt.close()
        print(f"Graph updated: {filename}")

if __name__ == "__main__":
    generate_daily_plots()


# At the end of fetch_weather.py:
if __name__ == "__main__":
    generate_daily_plots()