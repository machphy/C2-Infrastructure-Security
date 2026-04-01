"""
Correlation layer.
Weak signals become strong only when combined.
"""

def correlate(signals: dict):
    correlation_score = sum(signals.values())

    correlated = {
        "signals": signals,
        "correlation_score": round(correlation_score, 2)
    }
    return correlated
