#!/usr/bin/env python3

"""
Adaptive Beacon Detector

This script extends basic beacon detection by:
- Building a per-host (src_ip) baseline of connection intervals
- Comparing individual (src_ip, dst_ip, dst_port) flows against the host baseline
- Flagging flows that are unusually regular (low stddev) and deviate from host baseline

Input CSV columns (required):
    timestamp, src_ip, dst_ip, dst_port
"""

import sys
import pandas as pd
import numpy as np

MIN_SAMPLES_FLOW = 5      # minimum events per flow
MIN_SAMPLES_HOST = 10     # minimum intervals per host to build baseline

def compute_intervals(series):
    """Compute time intervals in seconds between sorted timestamps."""
    ts = series.sort_values().values
    if len(ts) < 2:
        return []
    deltas = []
    for i in range(1, len(ts)):
        delta = (ts[i] - ts[i - 1]) / np.timedelta64(1, "s")
        deltas.append(float(delta))
    return deltas

def main(csv_path):
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"[ERROR] Failed to read CSV: {e}")
        sys.exit(1)

    required = {"timestamp", "src_ip", "dst_ip", "dst_port"}
    if not required.issubset(df.columns):
        print(f"[ERROR] CSV must contain: {required}")
        sys.exit(1)

    # Parse timestamps
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.dropna(subset=["timestamp"])

    # ------------------------------------------------------------------
    # 1) Build host-level baseline for each src_ip
    # ------------------------------------------------------------------
    host_baselines = {}

    for src_ip, group in df.groupby("src_ip"):
        intervals_all = []
        # take intervals across all dst_ip/dst_port for this host
        for (_, sub) in group.groupby(["dst_ip", "dst_port"]):
            intervals_all.extend(compute_intervals(sub["timestamp"]))

        if len(intervals_all) >= MIN_SAMPLES_HOST:
            baseline_avg = float(np.mean(intervals_all))
            baseline_std = float(np.std(intervals_all))
            host_baselines[src_ip] = {
                "avg": baseline_avg,
                "std": baseline_std,
                "samples": len(intervals_all),
            }

    # ------------------------------------------------------------------
    # 2) Evaluate each (src_ip, dst_ip, dst_port) flow against baseline
    # ------------------------------------------------------------------
    print("=== Adaptive Beaconing Candidates ===")
    print("src_ip,dst_ip,dst_port,avg_interval,stddev_interval,count,host_baseline_avg,host_baseline_std,host_samples,regularity_score")

    for (src_ip, dst_ip, dst_port), group in df.groupby(["src_ip", "dst_ip", "dst_port"]):
        intervals = compute_intervals(group["timestamp"])
        if len(intervals) < MIN_SAMPLES_FLOW:
            continue

        flow_avg = float(np.mean(intervals))
        flow_std = float(np.std(intervals))
        count = len(intervals)

        # Skip if host baseline is missing (not enough data)
        if src_ip not in host_baselines:
            continue

        host_base = host_baselines[src_ip]
        host_avg = host_base["avg"]
        host_std = host_base["std"]
        host_samples = host_base["samples"]

        # Regularity score: low stddev relative to host baseline
        # If host_std == 0, fall back to absolute stddev threshold
        if host_std > 0:
            regularity_score = (host_std + 1e-6) / (flow_std + 1e-6)
        else:
            regularity_score = 1.0 if flow_std < 2 else 0.1

        # Heuristic conditions:
        # - Flow is highly regular: flow_std very small
        # - Flow differs in interval from host baseline OR host baseline is noisy
        if flow_std < 2 and regularity_score > 1.5:
            print(
                f"{src_ip},{dst_ip},{dst_port},"
                f"{flow_avg:.2f},{flow_std:.2f},{count},"
                f"{host_avg:.2f},{host_std:.2f},{host_samples},{regularity_score:.2f}"
            )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 adaptive_beacon_detector.py <flows.csv>")
        sys.exit(1)

    main(sys.argv[1])
