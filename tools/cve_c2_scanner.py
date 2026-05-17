#!/usr/bin/env python3
import requests
import argparse
import sys
import urllib3

# Suppress insecure request warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_cve_2022_39197(ip, port):
    """
    Checks for CVE-2022-39197 (Cobalt Strike Team Server XSS/RCE).
    This is a simulated check that looks for known CS signatures.
    """
    url = f"https://{ip}:{port}/"
    print(f"[*] Scanning {url} for Cobalt Strike Team Server signatures...")
    
    try:
        # Standard CS HTTP GET profile often responds with a 404 and specific headers
        response = requests.get(url, verify=False, timeout=5)
        
        # Check for common default CS team server characteristics
        if "HTTP/1.1 404 Not Found" in str(response.raw._original_response.msg) or response.status_code == 404:
            if 'Content-Type' in response.headers and response.headers['Content-Type'] == 'text/plain':
                print("[!] Warning: Potential Cobalt Strike Team Server detected.")
                print("[!] The server might be vulnerable to CVE-2022-39197 if version < 4.7.1")
                return True
        print("[+] Target does not match default Cobalt Strike signatures.")
        return False
    except requests.exceptions.RequestException as e:
        print(f"[-] Could not connect to {url}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="C2 Vulnerability Scanner (e.g., Cobalt Strike CVEs)")
    parser.add_argument("-t", "--target", required=True, help="Target IP address of the suspected C2 server")
    parser.add_argument("-p", "--port", type=int, default=443, help="Target port (default: 443)")
    
    args = parser.parse_args()
    
    print(f"=== C2 Vulnerability Scanner ===")
    print(f"Target: {args.target}:{args.port}\n")
    
    # Run checks
    check_cve_2022_39197(args.target, args.port)
    
if __name__ == "__main__":
    main()
