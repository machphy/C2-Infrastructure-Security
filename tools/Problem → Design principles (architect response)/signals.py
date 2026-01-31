"""
Collect weak behavioral signals.
No single signal should alert by itself.
"""

def beacon_signal(avg_interval, stddev):
    if avg_interval <= 30 and stddev < 2:
        return 0.7
    return 0.0

def dns_entropy_signal(entropy):
    if entropy >= 3.5:
        return 0.6
    return 0.0

def tls_anomaly_signal(is_rare):
    return 0.5 if is_rare else 0.0

def ioc_signal(match):
    return 0.9 if match else 0.0
