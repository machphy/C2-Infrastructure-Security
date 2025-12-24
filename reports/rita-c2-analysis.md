# RITA-Based C2 Detection Analysis

## Objective
To identify Command and Control (C2) communication by analyzing
network traffic using Zeek logs and Real Intelligence Threat Analytics (RITA),
without relying on payload inspection.

## Dataset
- PCAP: rita_challenge.pcap
- Processing: PCAP converted to Zeek logs
- Analysis Tool: RITA (Active Countermeasures)

## Methodology
1. Converted PCAP files to Zeek logs using Zeek readpcap.
2. Imported Zeek logs into RITA for structured analysis.
3. Analyzed beaconing behavior, DNS anomalies, long-lived connections,
   and threat intelligence correlations.

## Key Findings
- Periodic outbound connections with low jitter indicative of C2 beaconing.
- Multiple internal hosts communicating with malicious domains.
- Long-lived connections over non-standard ports.
- RITA threat modifiers such as prevalence, rare signature, and first seen
  helped prioritize suspicious connections.

## Indicators of Compromise
- Malicious domain: rabbithole.malhare.net
- Suspicious external infrastructure identified via threat intelligence.
- Repeated connections at consistent intervals.

## Conclusion
This analysis demonstrates that encrypted C2 infrastructure can be detected
using behavioral network analytics. RITA enables SOC teams to efficiently
hunt for C2 activity using metadata and statistical indicators.

## Limitations
- Small datasets may increase false positives.
- C2 traffic over popular cloud services may blend with legitimate traffic.

## Future Work
- DNS entropy scoring for tunneling detection.
- Correlation with endpoint telemetry.
- Automated response via SOAR playbooks.




