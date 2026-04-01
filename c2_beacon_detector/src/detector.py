import numpy as np

from .features import compute_iat, coefficient_of_variation, interval_entropy, basic_stats


def beacon_score_from_iat(iat):
    """
    This is the heart of the detector.

    We score based on:
    - low CV (more regular)
    - low entropy (more repetitive)
    - enough samples (so we don't overreact)

    Score is between 0 and 1.
    """

    if iat is None or len(iat) < 6:
        # Not enough evidence. Could be anything.
        return 0.0, {"reason": "not_enough_samples"}

    cv = coefficient_of_variation(iat)
    ent = interval_entropy(iat)

    # Defensive defaults
    if cv is None:
        cv = 999.0
    if ent is None:
        ent = 999.0

    # CV scoring:
    # CV ~ 0.0 => very periodic (suspicious)
    # CV >= 1.0 => very random (less suspicious)
    cv_score = max(0.0, min(1.0, 1.0 - cv))

    # Entropy scoring:
    # Low entropy => more suspicious.
    # Entropy depends on bins, so we normalize roughly.
    # In practice: ent 0-1 is super low, 2-3 medium, 4+ high.
    ent_score = 0.0
    if ent <= 1.0:
        ent_score = 1.0
    elif ent <= 2.0:
        ent_score = 0.7
    elif ent <= 3.0:
        ent_score = 0.4
    else:
        ent_score = 0.1

    # Combine scores (simple weighted blend).
    # I prefer this to a single hard threshold, because it stays explainable.
    score = (0.65 * cv_score) + (0.35 * ent_score)

    debug = {
        "cv": float(cv),
        "entropy": float(ent),
        "cv_score": float(cv_score),
        "entropy_score": float(ent_score),
    }

    return float(score), debug


def analyze_flow_group(timestamps):
    """
    Given timestamps for a single (src_ip, dst_ip, dst_port),
    compute IAT features and return a risk score.
    """
    iat = compute_iat(timestamps)

    score, debug = beacon_score_from_iat(iat)

    # Add human-friendly stats so the output is useful
    stats = basic_stats(iat)
    debug.update(stats)
    debug["samples"] = int(len(timestamps))
    debug["iat_samples"] = int(len(iat))

    return score, debug
