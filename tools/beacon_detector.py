import sys
import pandas as pd
import numpy as np

MIN_SAMPLES = 4
STDDEV_THRESHOLD_SEC = 2


def compute_intervals(timestamps):
    ts = timestamps.sort_values().to_numpy()
    if len(ts) < 2:
        return np.array([])
    deltas = np.diff(ts) / np.timedelta64(1, "s")
    return deltas.astype(float)

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

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    if df.empty:
        print("No valid timestamps found after parsing.")
        sys.exit(1)

    print("=== Potential Beaconing Flows ===")
    print("src_ip,dst_ip,dst_port,avg_interval_sec,stddev_interval_sec,count")

    grouped = df.groupby(["src_ip", "dst_ip", "dst_port"])

    for (src, dst, port), group in grouped:
        times = group["timestamp"].sort_values().values
        if len(times) < MIN_SAMPLES:
            continue

        intervals = compute_intervals(group["timestamp"])
        if len(intervals) < MIN_SAMPLES - 1:
            continue

        avg_interval = float(np.mean(intervals))
        stddev = float(np.std(intervals))

        if stddev < STDDEV_THRESHOLD_SEC:
            print(f"{src},{dst},{port},{avg_interval:.2f},{stddev:.2f},{len(times)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 beacon_detector.py <flows.csv>")
        sys.exit(1)

    main(sys.argv[1])
