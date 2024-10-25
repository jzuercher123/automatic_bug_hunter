import logging
from scanning.nmap_scan import run_nmap_scan
from scanning.nikto_scan import run_nikto_scan
from reporting.report_generator import generate_reports
from reporting.email_reporter import send_email_report
from utils.error_handler import safe_run

def run_pentest_on_domain(domain):
    logger = logging.getLogger(__name__)
    logger.info(f"Initiating pentest for domain: {domain}")

    # Define output directories
    nmap_output_dir = f"reports/nmap/{domain}/"
    nikto_output_dir = f"reports/nikto/{domain}/"

    # Perform Nmap Scan
    nmap_results = safe_run(run_nmap_scan, domain, nmap_output_dir)

    # Perform Nikto Scan
    nikto_results = safe_run(run_nikto_scan, domain, nikto_output_dir)

    # Aggregate Results
    # You can customize how you aggregate Nmap and Nikto results
    aggregated_results = {
        "domain": domain,
        "nmap": nmap_results,
        "nikto": nikto_results
    }

    # Generate Reports
    generate_reports(aggregated_results, domain)

    # Define report file paths
    report_files = [
        f"reports/markdown/{domain}.md",
        f"reports/json/{domain}.json",
        f"reports/html/{domain}.html"
    ]

    # Send Reports via Email
    send_email_report(report_files)

    logger.info(f"Pentest cycle completed for domain: {domain}")
