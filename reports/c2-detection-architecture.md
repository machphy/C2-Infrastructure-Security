# C2 Detection Architecture Overview

## Detection Philosophy
This project follows a defense-in-depth approach to detecting
Command and Control (C2) activity by correlating multiple weak
signals into high-confidence alerts.

Rather than relying on signatures or payload inspection, the
framework focuses on behavioral indicators observable in
network metadata.

## Detection Layers

### 1. Timing-Based Beacon Detection
Identifies periodic outbound connections with low variance in
inter-arrival times, commonly associated with automated C2 callbacks.

### 2. Adaptive Host Baselining
Builds per-host behavioral baselines to reduce false positives
in environments with noisy or scheduled traffic.

### 3. DNS Behavior Analysis
Detects high-entropy domains and abnormal query patterns
associated with DGA-based malware and DNS tunneling.

### 4. TLS Metadata Analysis
Flags rare or anomalous TLS handshake characteristics that
deviate from standard browser behavior.

### 5. Risk Scoring & Alert Prioritization
Combines multiple detection signals into a unified risk score
to prioritize alerts and reduce analyst fatigue.

## Operational Integration
Detection outputs are designed to be consumed by SOC tooling,
including SIEM platforms, IOC repositories, and incident
response workflows.

## Outcome
This layered approach enables reliable detection of encrypted
C2 infrastructure while maintaining scalability and low
false-positive rates in real-world SOC environments.
