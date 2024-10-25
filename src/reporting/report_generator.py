import json
import markdown
from jinja2 import Template
import logging

logger = logging.getLogger(__name__)


def generate_reports(aggregated_results, domain):
    logger.debug(f"Generating reports for {domain}")
    try:
        # JSON Report
        with open(f"reports/json/{domain}.json", 'w') as f:
            json.dump(aggregated_results, f, indent=4)

        # Markdown Report
        md_content = f"# Pentest Report for {domain}\n\n"

        # Nmap Section
        md_content += "## Nmap Scan Results\n"
        md_content += f"### Summary\n```\n{json.dumps(aggregated_results['nmap']['scaninfo'], indent=4)}\n```\n"
        md_content += f"### Ports and Services\n```\n{json.dumps(aggregated_results['nmap']['host']['ports'], indent=4)}\n```\n"

        # Nikto Section
        md_content += "## Nikto Scan Results\n"
        md_content += f"### Vulnerabilities Found\n```\n{json.dumps(aggregated_results['nikto']['vulnerabilities'], indent=4)}\n```\n"

        with open(f"reports/markdown/{domain}.md", 'w') as f:
            f.write(md_content)

        # HTML Report using Jinja2 Template
        template = Template("""
        <html>
        <head><title>Pentest Report for {{ domain }}</title></head>
        <body>
            <h1>Pentest Report for {{ domain }}</h1>

            <h2>Nmap Scan Results</h2>
            <h3>Summary</h3>
            <pre>{{ nmap.scaninfo | tojson(indent=4) }}</pre>
            <h3>Ports and Services</h3>
            <pre>{{ nmap.host.ports | tojson(indent=4) }}</pre>

            <h2>Nikto Scan Results</h2>
            <h3>Vulnerabilities Found</h3>
            <pre>{{ nikto.vulnerabilities | tojson(indent=4) }}</pre>
        </body>
        </html>
        """)
        html_content = template.render(
            domain=domain,
            nmap=aggregated_results['nmap'],
            nikto=aggregated_results['nikto']
        )
        with open(f"reports/html/{domain}.html", 'w') as f:
            f.write(html_content)

        logger.info(f"Reports generated for {domain}")
    except Exception as e:
        logger.error(f"Failed to generate reports for {domain}: {e}")
        raise
