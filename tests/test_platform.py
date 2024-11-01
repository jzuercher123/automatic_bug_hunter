import platform
import subprocess

def main():
    print("Running on:", platform.system())
    print("Release:", platform.release())

    # Example: Run a Kali Linux command
    try:
        result = subprocess.run(['nmap', '--version'], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error running nmap: {e}")

if __name__ == "__main__":
    main()
