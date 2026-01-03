def calculate_c2_risk(beacon=False, dns_entropy=False,
                      rare_tls=False, ioc_match=False):
    score = 0

    if beacon:
        score += 30
    if dns_entropy:
        score += 25
    if rare_tls:
        score += 20
    if ioc_match:
        score += 25

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level

if __name__ == "__main__":
    score, level = calculate_c2_risk(
        beacon=True,
        dns_entropy=True,
        rare_tls=False,
        ioc_match=True
    )

    print(f"C2 Risk Score: {score}")
    print(f"Risk Level: {level}")
