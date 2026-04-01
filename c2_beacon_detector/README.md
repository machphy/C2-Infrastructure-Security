# C2 Beacon Detector (Defensive)

This is a small defensive project that looks for **beacon-like traffic** patterns
in network flow logs.

It does NOT decrypt traffic.
It does NOT do anything offensive.
It only analyzes timestamps and basic flow metadata.

## What it detects (high level)
- Repeated callbacks to the same destination
- Low jitter / semi-regular intervals
- Suspiciously consistent behavior

## Quick run
```bash
pip install -r requirements.txt
python -m src.main --csv data/flows.csv
