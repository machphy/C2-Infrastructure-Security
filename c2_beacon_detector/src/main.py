import argparse
import pandas as pd

from .detector import analyze_flow_group


def parse_args():
    p = argparse.ArgumentParser(
        description="Defensive beaconing detector for flow logs (C2-style behavior)."
    )
    p.add_argument("--csv", required=True, help="Path to flows.csv")
    p.add_argument("--min-events", type=int, default=6, help="Minimum events per group")
    p.add_argument("--top", type=int, default=20, help="How many results to show")
    return p.parse_args()


def main():
    args = parse_args()

    # Load
    df = pd.read_csv(args.csv)

    required = {"src_ip", "dst_ip", "dst_port", "ts"}
    missing = required - set(df.columns)

    if missing:
        raise SystemExit(f"CSV missing columns: {sorted(list(missing))}")

    # Clean types
    df["dst_port"] = df["dst_port"].astype(int)
    df["ts"] = df["ts"].astype(float)

    # Group flows
    results = []

    for (src, dst, port), g in df.groupby(["src_ip", "dst_ip", "dst_port"]):
        if len(g) < args.min_events:
            continue

        timestamps = g["ts"].tolist()
        score, debug = analyze_flow_group(timestamps)

        results.append(
            {
                "src_ip": src,
                "dst_ip": dst,
                "dst_port": port,
                "score": score,
                "events": len(g),
                **debug,
            }
        )

    if not results:
        print("No groups met the minimum event threshold.")
        return

    out = pd.DataFrame(results)
    out = out.sort_values("score", ascending=False)

    # Print top suspicious
    print("\n=== Top suspicious beacon-like flows ===\n")
    cols = [
        "src_ip",
        "dst_ip",
        "dst_port",
        "score",
        "events",
        "cv",
        "entropy",
        "mean",
        "std",
        "min",
        "max",
    ]

    # Some columns might not exist if data is tiny
    cols = [c for c in cols if c in out.columns]

    print(out[cols].head(args.top).to_string(index=False))

    print("\nTip:")
    print("- Score closer to 1.0 means more periodic / beacon-like.")
    print("- This is NOT a verdict, it's just a hunting signal.\n")


if __name__ == "__main__":
    main()
