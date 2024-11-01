import subprocess

def update_tools():
    try:
        subprocess.run(['sudo', 'apt-get', 'update'])
        subprocess.run(['sudo', 'apt-get', 'upgrade', '-y'])
        subprocess.run(['zap-cli', 'update'])
        # Add other tool update commands as needed
    except Exception as e:
        print(f"Error updating tools: {e}")
