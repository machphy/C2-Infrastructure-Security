import sys
import pandas as pd
from datetime import datetime
import numpy as np

def main(csv_file):
    try:
        df = pd.read_csv(csv_file)
    except Exception as e:
        print("Error reading CSV:", e)
        sys.exit(1)

    required_cols = {"timestamp", "src_ip", "dst_ip", "dst_port"}
    if not required_cols.issubset(df.columns):
        print("CSV must contain columns:", required_cols)
        sys.exit(1)

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    print("=== Potential Beaconing Flows ===")
    print("src_ip,dst_ip,dst_port,avg_interval_sec,stddev_interval_sec,count")

    grouped = df.groupby(["src_ip", "dst_ip", "dst_port"])

    for (src, dst, port), group in grouped:
        times = group["timestamp"].sort_values().values

        if len(times) < 4:
            continue

        intervals = []
        for i in range(1, len(times)):
            delta = (times[i] - times[i-1]) / np.timedelta64(1, 's')
            intervals.append(delta)

        avg_interval = np.mean(intervals)
        stddev = np.std(intervals)

        if stddev < 2:
            print(f"{src},{dst},{port},{avg_interval:.2f},{stddev:.2f},{len(times)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 beacon_detector.py <flows.csv>")
        sys.exit(1)

    main(sys.argv[1]_)