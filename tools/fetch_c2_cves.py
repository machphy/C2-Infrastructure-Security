#!/usr/bin/env python3
import requests
import json
import argparse
from datetime import datetime, timedelta

def fetch_recent_cves(keyword="cobalt strike", days=90):
    """
    Fetches recent CVEs from the NVD API that match a specific keyword.
    """
    # NVD API 2.0 Endpoint
    url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Format dates as required by NVD (YYYY-MM-DDTHH:MM:SS.000)
    pubStartDate = start_date.strftime("%Y-%m-%dT00:00:00.000")
    pubEndDate = end_date.strftime("%Y-%m-%dT23:59:59.000")
    
    params = {
        "keywordSearch": keyword,
        "pubStartDate": pubStartDate,
        "pubEndDate": pubEndDate
    }
    
    print(f"[*] Fetching CVEs related to '{keyword}' from the last {days} days...")
    print(f"[*] API URL: {url}")
    
    try:
        # We use a timeout and proper headers. Note: NVD rate limits heavily without an API key.
        headers = {"User-Agent": "C2-Infrastructure-Security-Bot/1.0"}
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            total_results = data.get("totalResults", 0)
            print(f"[+] Found {total_results} matching CVEs.\n")
            
            vulnerabilities = data.get("vulnerabilities", [])
            for item in vulnerabilities:
                cve = item.get("cve", {})
                cve_id = cve.get("id", "Unknown ID")
                descriptions = cve.get("descriptions", [])
                
                # Get English description
                desc = "No description available."
                for d in descriptions:
                    if d.get("lang") == "en":
                        desc = d.get("value")
                        break
                        
                print(f"=== {cve_id} ===")
                print(f"Description: {desc}\n")
        else:
            print(f"[-] Error fetching data from NVD API. Status Code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"[-] Network error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="C2 Framework CVE Threat Intel Fetcher")
    parser.add_argument("-k", "--keyword", default="cobalt strike", help="Keyword to search for (e.g., 'cobalt strike', 'metasploit', 'log4j')")
    parser.add_argument("-d", "--days", type=int, default=365, help="Number of days to look back (default: 365)")
    
    args = parser.parse_args()
    fetch_recent_cves(args.keyword, args.days)

if __name__ == "__main__":
    main()
