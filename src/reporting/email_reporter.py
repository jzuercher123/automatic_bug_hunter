import subprocess

def send_email(report_paths, recipient_email):
    try:
        attachments = ' '.join(report_paths)
        subject = "Automated Pentest Report"
        body = "Please find the attached pentest reports."
        subprocess.run(['mutt', '-s', subject, '-a'] + report_paths + ['--', recipient_email], input=body.encode())
    except Exception as e:
        print(f"Error sending email: {e}")
