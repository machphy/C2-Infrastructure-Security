"""
Adaptive per-host baselining.
Avoid global static thresholds.
"""

class HostBaseline:
    def __init__(self):
        self.intervals = []

    def learn(self, interval):
        self.intervals.append(interval)

    def is_anomalous(self, interval):
        if len(self.intervals) < 5:
            return False

        avg = sum(self.intervals) / len(self.intervals)
        return interval < (avg * 0.4)
