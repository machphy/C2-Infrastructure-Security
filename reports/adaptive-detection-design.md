# Adaptive Beacon Detection Design

## Motivation

The initial beacon detection logic relied on a static threshold for interval variance (for example, stddev < 2 seconds). This approach is effective in clean lab environments but can introduce false positives in noisy production networks where hosts naturally generate diverse network traffic patterns.

To address this, an adaptive approach is introduced, where each host (src_ip) is assigned a baseline of its normal connection timing behaviour. Individual flows are then evaluated relative to this baseline.

## Data Model

Input data:
- Flow-level log in CSV format
- Required fields:
  - timestamp
  - src_ip
  - dst_ip
  - dst_port

## Baseline Construction (Per Host)

For each src_ip:

1. Group all flows originating from this host.
2. For each (dst_ip, dst_port), compute sorted timestamps and inter-arrival intervals.
3. Aggregate all intervals across all destinations for the host.
4. If the host has at least N intervals (MIN_SAMPLES_HOST), compute:
   - baseline_avg_interval
   - baseline_stddev_interval

This defines the host's normal timing behaviour.

## Flow Evaluation

For each (src_ip, dst_ip, dst_port) flow:

1. Compute inter-arrival intervals.
2. Compute:
   - flow_avg_interval
   - flow_stddev_interval
3. Require at least M samples (MIN_SAMPLES_FLOW) to avoid unstable statistics.
4. Look up the host baseline for src_ip.

A regularity_score is then derived:

- If host_stddev > 0:
  - regularity_score = host_stddev / flow_stddev
- If host_stddev == 0:
  - Fall back to an absolute stddev threshold.

A flow is considered a beaconing candidate when:

- flow_stddev is very small (high regularity), and
- regularity_score exceeds a chosen threshold (for example, > 1.5).

This heuristic highlights flows that are significantly more regular than the host's typical behaviour.

## Benefits

- Reduces dependency on static global thresholds.
- Adapts to each host's behaviour, which is critical in heterogeneous environments.
- Remains effective when payloads are encrypted, as it operates purely on timing metadata.

## Limitations and Future Work

- Requires sufficient historical data per host to build reliable baselines.
- Very low-activity hosts may not produce enough intervals.
- Adversaries can introduce jitter to evade timing-based detection.
- Future improvements can include:
  - Time-of-day aware baselines.
  - Integration with DNS and TLS metadata.
  - Alert scoring that combines timing anomalies with IOC matches.

