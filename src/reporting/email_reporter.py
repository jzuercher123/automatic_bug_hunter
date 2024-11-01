import subprocess

# function to send an email
def send_email(subject, body, recipient):
    # use the subprocess module to send an email
    try:
        subprocess.run(['echo', f'{body} | mail -s {subject} {recipient}'], shell=True)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

