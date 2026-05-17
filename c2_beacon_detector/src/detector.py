import numpy as np

from .features import compute_iat, coefficient_of_variation, interval_entropy, basic_stats, lag1_autocorrelation


def beacon_score_from_iat(iat):
    """
    This is the heart of the detector.

    We score based on:
    - low CV (more regular)
    - low entropy (more repetitive)
    - enough samples (so we don't overreact)


    """

    if iat is None or len(iat) < 6:
        # Not enough evidence. Could be anything.
        return 0.0, {"reason": "not_enough_samples"}

    cv = coefficient_of_variation(iat)
    ent = interval_entropy(iat)
    autocorr = lag1_autocorrelation(iat)

    # Defensive defaults
    if cv is None:
        cv = 999.0
    if ent is None:
        ent = 999.0
    if autocorr is None:
        autocorr = 0.0

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

    # Autocorr scoring:
    # High autocorr (human bursty traffic) reduces the score.
    # We penalize the score if autocorr > 0.4
    if autocorr > 0.4:
        score -= (autocorr * 0.3)
    
    score = max(0.0, float(score))

    debug = {
        "cv": float(cv),
        "entropy": float(ent),
        "autocorr": float(autocorr),
        "cv_score": float(cv_score),
        "entropy_score": float(ent_score),
    }

    return score, debug


def analyze_flow_group(timestamps, bytes_sizes=None):
    """
    Given timestamps for a single (src_ip, dst_ip, dst_port),
    compute IAT features and return a risk score.
    Optionally process payload sizes if provided.
    """
    iat = compute_iat(timestamps)

    score, debug = beacon_score_from_iat(iat)

    # Add human-friendly stats so the output is useful
    stats = basic_stats(iat)
    debug.update(stats)
    debug["samples"] = int(len(timestamps))
    debug["iat_samples"] = int(len(iat))
    
    # Optional bytes analysis
    if bytes_sizes is not None and len(bytes_sizes) > 0:
        b_cv = coefficient_of_variation(bytes_sizes)
        if b_cv is not None:
            debug["bytes_cv"] = float(b_cv)
            # If payload sizes are extremely uniform (low CV), bump score
            if b_cv < 0.1:
                score += 0.2
            elif b_cv > 1.0:
                score -= 0.1
        score = min(1.0, max(0.0, score))

    return score, debug
