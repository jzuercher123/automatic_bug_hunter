import subprocess

def run_owasp_zap(target_url, report_path):
    try:
        subprocess.run(['zap-cli', 'start'])
        subprocess.run(['zap-cli', 'spider', target_url])
        subprocess.run(['zap-cli', 'active-scan', target_url])
        alerts = subprocess.run(['zap-cli', 'alerts', '--output', 'json'], capture_output=True, text=True)
        with open(report_path, 'w') as f:
            f.write(alerts.stdout)
    except Exception as e:
        print(f"Error running OWASP ZAP: {e}")
