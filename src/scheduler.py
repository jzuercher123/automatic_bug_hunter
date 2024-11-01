import threading
from src.reporting.email_reporter import send_email
from src.reporting.report_generator import parse_zap_alerts, generate_reports
from src.scanning.owasp_zap import run_owasp_zap


def run_pentest_on_domain(domain):
    report_path = f"reports/{domain}"
    run_owasp_zap(domain, f"{report_path}.json")
    vulnerabilities = parse_zap_alerts(f"{report_path}.json")
    generate_reports(vulnerabilities, report_path)
    send_email([f"{report_path}.md", f"{report_path}.json", f"{report_path}.html"], 'your_email@example.com')

def execute_pentests(domains):
    threads = []
    for domain in domains:
        thread = threading.Thread(target=run_pentest_on_domain, args=(domain,))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
