#!/usr/bin/env python3

import platform
import subprocess
import sys
import os
import logging
from shutil import which
import requests
from packaging import version

# Import the 'distro' package for Linux distribution detection
try:
    import distro
except ImportError:
    print("The 'distro' package is not installed. Installing now...")
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'distro'], check=True)
    import distro

# Configure logging
LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'setup_dependencies.log'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()


def check_root():
    """Check if the script is running with root privileges."""
    try:
        # os.geteuid() is available on Unix/Linux/macOS
        if os.geteuid() != 0:
            logger.error("This script requires root privileges. Please run as root.")
            sys.exit("Error: This script requires root privileges. Please run as root.")
    except AttributeError:
        # os.geteuid() is not available on Windows
        logger.warning("Root privilege check is not applicable on this operating system.")
        # Optionally, implement Windows admin check here if needed


def detect_os():
    """Detect the operating system and return a standardized name."""
    os_system = platform.system()
    os_name = ""
    if os_system == "Linux":
        distro_id = distro.id().lower()
        logger.info(f"Detected Linux distribution ID: {distro_id}")
        if 'ubuntu' in distro_id or 'debian' in distro_id or 'kali' in distro_id:
            os_name = 'debian'
        elif 'centos' in distro_id or 'fedora' in distro_id or 'redhat' in distro_id:
            os_name = 'redhat'
        else:
            os_name = 'unknown'
    elif os_system == "Darwin":
        os_name = 'macos'
    else:
        os_name = 'unknown'
    logger.info(f"Detected OS: {os_name}")
    return os_name


def detect_architecture():
    """Detect the system architecture."""
    arch = platform.machine().lower()
    logger.info(f"Detected architecture: {arch}")
    return arch


def is_command_available(command):
    """Check if a command is available on the system."""
    return which(command) is not None


def install_packages_debian(packages):
    """Install packages using apt for Debian-based systems."""
    try:
        logger.info("Updating package list...")
        subprocess.run(['apt-get', 'update'], check=True)
        logger.info(f"Installing packages: {' '.join(packages)}")
        subprocess.run(['apt-get', 'install', '-y'] + packages, check=True)
        logger.info("Packages installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install packages on Debian-based system: {e}")
        sys.exit(f"Error: Failed to install packages on Debian-based system: {e}")


def install_packages_redhat(packages):
    """Install packages using yum or dnf for RedHat-based systems."""
    try:
        # Check if dnf is available, else use yum
        if is_command_available('dnf'):
            pkg_manager = 'dnf'
        elif is_command_available('yum'):
            pkg_manager = 'yum'
        else:
            logger.error("Neither 'dnf' nor 'yum' package managers are available.")
            sys.exit("Error: Neither 'dnf' nor 'yum' package managers are available.")
        logger.info("Updating package list...")
        subprocess.run([pkg_manager, 'makecache'], check=True)
        logger.info(f"Installing packages: {' '.join(packages)}")
        subprocess.run([pkg_manager, 'install', '-y'] + packages, check=True)
        logger.info("Packages installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install packages on RedHat-based system: {e}")
        sys.exit(f"Error: Failed to install packages on RedHat-based system: {e}")


def install_packages_macos(packages):
    """Install packages using brew for macOS."""
    try:
        # Determine Homebrew installation path based on architecture
        arch = detect_architecture()
        if 'arm' in arch:
            brew_path = '/opt/homebrew/bin'
        else:
            brew_path = '/usr/local/bin'

        if not is_command_available('brew'):
            logger.info("Homebrew not found. Installing Homebrew...")
            subprocess.run(['/bin/bash', '-c',
                            "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"],
                           check=True)
            # Add Homebrew to PATH
            os.environ['PATH'] += os.pathsep + brew_path
            logger.info("Homebrew installed successfully.")
        else:
            logger.info("Homebrew is already installed.")

        logger.info(f"Installing packages: {' '.join(packages)}")
        subprocess.run(['brew', 'install'] + packages, check=True)
        logger.info("Packages installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install packages on macOS: {e}")
        sys.exit(f"Error: Failed to install packages on macOS: {e}")


def install_system_dependencies(os_name):
    """Install system dependencies based on the detected OS."""
    # Define the required packages for each OS
    packages_debian = [
        'python3-venv',
        'nmap',
        'nikto',
        'mutt',
        'default-jdk',  # For OWASP ZAP
        'wget',
        'curl',
        'unzip'
    ]
    packages_redhat = [
        'nmap',
        'nikto',
        'mutt',
        'java-11-openjdk',  # For OWASP ZAP
        'wget',
        'curl',
        'unzip'
    ]
    packages_macos = [
        'nmap',
        'nikto',
        'mutt',
        'java',  # For OWASP ZAP
        'wget',
        'curl',
        'unzip'
    ]

    if os_name == 'debian':
        install_packages_debian(packages_debian)
    elif os_name == 'redhat':
        install_packages_redhat(packages_redhat)
    elif os_name == 'macos':
        install_packages_macos(packages_macos)
    else:
        logger.error("Unsupported operating system.")
        sys.exit("Error: Unsupported operating system.")


def install_owasp_zap(os_name):
    """Install OWASP ZAP based on the OS."""
    try:
        if os_name in ['debian', 'redhat']:
            logger.info("Installing OWASP ZAP manually...")
            # Dynamically get the latest version


            response = requests.get("https://api.github.com/repos/zaproxy/zaproxy/releases/latest")
            if response.status_code == 200:
                latest_release = response.json()
                tag_name = latest_release['tag_name']
                download_url = ""
                for asset in latest_release['assets']:
                    if 'Linux' in asset['name'] and asset['name'].endswith('.tar.gz'):
                        download_url = asset['browser_download_url']
                        break
                if not download_url:
                    logger.error("OWASP ZAP tar.gz asset not found.")
                    sys.exit("Error: OWASP ZAP tar.gz asset not found.")

                zap_install_dir = "/opt/zaproxy"
                os.makedirs(zap_install_dir, exist_ok=True)
                logger.info(f"Downloading OWASP ZAP from {download_url}")
                subprocess.run(['wget', '-O', f"{zap_install_dir}/ZAP.tar.gz", download_url], check=True)
                subprocess.run(['tar', '-xzf', f"{zap_install_dir}/ZAP.tar.gz", '-C', zap_install_dir], check=True)

                # Create a symbolic link to zap.sh for easy access
                zap_sh_path = os.path.join(zap_install_dir, 'zap.sh')
                symlink_path = '/usr/local/bin/zap.sh'
                if not os.path.exists(symlink_path):
                    subprocess.run(['ln', '-s', zap_sh_path, symlink_path], check=True)
                logger.info("OWASP ZAP installed successfully.")
            else:
                logger.error(f"Failed to fetch OWASP ZAP releases: {response.status_code}")
                sys.exit(f"Error: Failed to fetch OWASP ZAP releases: {response.status_code}")
        elif os_name == 'macos':
            logger.info("Installing OWASP ZAP via Homebrew...")
            subprocess.run(['brew', 'install', '--cask', 'owasp-zap'], check=True)
            logger.info("OWASP ZAP installed successfully.")
        else:
            logger.error("Unsupported OS for OWASP ZAP installation.")
            sys.exit("Error: Unsupported OS for OWASP ZAP installation.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install OWASP ZAP: {e}")
        sys.exit(f"Error: Failed to install OWASP ZAP: {e}")
    except Exception as e:
        logger.error(f"An error occurred while installing OWASP ZAP: {e}")
        sys.exit(f"Error: An error occurred while installing OWASP ZAP: {e}")


def install_python_dependencies():
    """Install Python dependencies using pip."""
    try:
        logger.info("Installing Python dependencies from requirements.txt...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'], check=True)
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        logger.info("Python dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install Python dependencies: {e}")
        sys.exit(f"Error: Failed to install Python dependencies: {e}")


def verify_installations():
    """Verify that all required commands are available."""
    required_commands = ['nmap', 'nikto', 'mutt', 'java', 'zap.sh']
    missing_commands = []
    for cmd in required_commands:
        if not is_command_available(cmd):
            missing_commands.append(cmd)
    if missing_commands:
        logger.warning(f"The following commands are missing: {', '.join(missing_commands)}")
        print(
            f"Warning: The following commands are missing: {', '.join(missing_commands)}. Please install them manually if needed.")
    else:
        logger.info("All required commands are available.")


def main():
    logger.info("Starting dependency installation process.")
    check_root()
    os_name = detect_os()
    arch = detect_architecture()

    if os_name == 'unknown':
        logger.error("Unsupported or unrecognized operating system.")
        sys.exit("Error: Unsupported or unrecognized operating system.")

    install_system_dependencies(os_name)
    install_owasp_zap(os_name)
    install_python_dependencies()
    verify_installations()
    logger.info("Dependency installation process completed successfully.")
    print("All dependencies have been installed successfully.")


if __name__ == "__main__":
    main()
