"""
Risk engine converts correlation into decisions.
"""

def risk_level(score):
    if score >= 2.0:
        return "HIGH"
    if score >= 1.2:
        return "MEDIUM"
    return "LOW"

def risk_decision(correlation):
    score = correlation["correlation_score"]
    return {
        "score": score,
        "risk": risk_level(score)
    }
