import subprocess
import logging
import json
import os
from datetime import datetime

logger = logging.getLogger(__name__)

def run_nmap_scan(target, output_dir):
    """
    Executes an Nmap scan on the specified target and saves the results.

    Args:
        target (str): The domain or IP address to scan.
        output_dir (str): The directory where scan results will be stored.

    Returns:
        dict: Parsed JSON results from the Nmap scan.
    """
    try:
        logger.info(f"Starting Nmap scan for target: {target}")

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Define file paths
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        xml_output = os.path.join(output_dir, f"{target}_nmap_{timestamp}.xml")
        json_output = os.path.join(output_dir, f"{target}_nmap_{timestamp}.json")

        # Define Nmap scan arguments
        # Example: Perform a comprehensive scan with OS detection, version detection, script scanning, and traceroute
        nmap_args = [
            "nmap",
            "-sV",                 # Service/version detection
            "-O",                  # OS detection
            "-A",                  # Aggressive scan options
            "-oX", xml_output,     # Output in XML format
            "-oJ", json_output,    # Output in JSON format
            target
        ]

        logger.debug(f"Nmap command: {' '.join(nmap_args)}")

        # Execute the Nmap scan
        subprocess.run(nmap_args, check=True)

        logger.info(f"Nmap scan completed for {target}. Results saved to {output_dir}")

        # Parse the JSON output for further processing if needed
        with open(json_output, 'r') as f:
            nmap_results = json.load(f)

        return nmap_results

    except subprocess.CalledProcessError as e:
        logger.error(f"Nmap scan failed for {target}: {e}")
        raise
    except FileNotFoundError:
        logger.error("Nmap is not installed or not found in PATH.")
        raise
    except json.JSONDecodeError:
        logger.error(f"Failed to parse Nmap JSON output for {target}.")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred during Nmap scan for {target}: {e}")
        raise
