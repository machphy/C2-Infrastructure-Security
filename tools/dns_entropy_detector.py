import math
import sys
import csv
from collections import Counter

def shannon_entropy(domain: str) -> float:
    """Calculate Shannon entropy of a domain string."""
    domain = domain.lower()
    counts = Counter(domain)
    entropy = 0.0
    for char in counts:
        p = counts[char] / len(domain)
        entropy -= p * math.log2(p)
    return entropy

def analyze_dns_log(csv_file):
    print("=== High Entropy DNS Domains ===")
    print("domain,entropy,query_count")

    domain_counts = Counter()

    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain = row.get("query")
            if domain:
                domain_counts[domain] += 1

    for domain, count in domain_counts.items():
        entropy = shannon_entropy(domain)
        if entropy >= 3.5 and count >= 3:
            print(f"{domain},{entropy:.2f},{count}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 new.py dns_logs.csv")
        sys.exit(1)

    analyze_dns_log(sys.argv[1])
