import numpy as np


def safe_float(x, default=0.0):
    """
    Small helper: because real logs are messy.
    I'd rather return a default than crash the whole pipeline.
    """
    try:
        return float(x)
    except Exception:
        return default


def compute_iat(timestamps):
    """
    Compute inter-arrival times (IAT) from a list of timestamps.

    timestamps: list/array of unix timestamps (seconds)
    returns: numpy array of diffs (seconds)
    """
    ts = np.array(timestamps, dtype=float)

    # Sort because some log sources aren't perfectly ordered
    ts = np.sort(ts)

    if len(ts) < 2:
        return np.array([])

    iat = np.diff(ts)

    # Sometimes you get duplicates or clock weirdness.
    # We keep only positive diffs.
    iat = iat[iat > 0]

    return iat


def coefficient_of_variation(arr):
    """
    CV = std / mean
    For beaconing, CV tends to be low (more regular).
    """
    if arr is None or len(arr) == 0:
        return None

    mean = np.mean(arr)
    std = np.std(arr)

    if mean <= 0:
        return None

    return float(std / mean)


def interval_entropy(iat, bins=10):
    """
    Rough entropy estimate of the interval distribution.
    Lower entropy often means more regular callbacks.

    Not perfect, but surprisingly useful as a feature.
    """
    if iat is None or len(iat) < 3:
        return None

    hist, _ = np.histogram(iat, bins=bins)
    total = np.sum(hist)

    if total == 0:
        return None

    probs = hist / total
    probs = probs[probs > 0]

    # Shannon entropy
    ent = -np.sum(probs * np.log2(probs))
    return float(ent)


def basic_stats(arr):
    """
    Quick stats for explainability.
    """
    if arr is None or len(arr) == 0:
        return {}

    return {
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
        "mean": float(np.mean(arr)),
        "std": float(np.std(arr)),
        "median": float(np.median(arr)),
    }
