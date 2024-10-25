import subprocess
import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def run_nikto_scan(target, output_dir):
    """
    Executes a Nikto scan on the specified target and saves the results.

    Args:
        target (str): The domain or IP address to scan.
        output_dir (str): The directory where scan results will be stored.

    Returns:
        dict: Parsed JSON results from the Nikto scan.
    """
    try:
        logger.info(f"Starting Nikto scan for target: {target}")

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Define file paths
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        text_output = os.path.join(output_dir, f"{target}_nikto_{timestamp}.txt")
        json_output = os.path.join(output_dir, f"{target}_nikto_{timestamp}.json")
        html_output = os.path.join(output_dir, f"{target}_nikto_{timestamp}.html")

        # Define Nikto scan arguments
        # Example: Perform a scan and save outputs in multiple formats
        nikto_args = [
            "nikto",
            "-h", target,
            "-output", text_output,
            "-Format", "json",
            "-o", json_output
        ]

        logger.debug(f"Nikto command: {' '.join(nikto_args)}")

        # Execute the Nikto scan for text and JSON outputs
        subprocess.run(nikto_args, check=True)

        # Additionally, generate an HTML report using a simple conversion (optional)
        # Note: Nikto does not support HTML output directly; you may need to convert it.
        # Here, we'll create a basic HTML file with the scan results.

        with open(text_output, 'r') as txt_file:
            scan_results = txt_file.read()

        html_content = f"""
        <html>
        <head><title>Nikto Scan Report for {target}</title></head>
        <body>
            <h1>Nikto Scan Report for {target}</h1>
            <pre>{scan_results}</pre>
        </body>
        </html>
        """

        with open(html_output, 'w') as html_file:
            html_file.write(html_content)

        logger.info(f"Nikto scan completed for {target}. Results saved to {output_dir}")

        # Parse the JSON output for further processing if needed
        with open(json_output, 'r') as f:
            nikto_results = json.load(f)

        return nikto_results

    except subprocess.CalledProcessError as e:
        logger.error(f"Nikto scan failed for {target}: {e}")
        raise
    except FileNotFoundError:
        logger.error("Nikto is not installed or not found in PATH.")
        raise
    except json.JSONDecodeError:
        logger.error(f"Failed to parse Nikto JSON output for {target}.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred during Nikto scan for {target}: {e}")
        raise
