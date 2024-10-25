#!/usr/bin/env python3
import platform
import subprocess
import sys
import os
import logging
from shutil import which

# Configure logging
logging.basicConfig(
    filename='logs/setup_dependencies.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()

def check_root():
    """Check if the script is run as root."""
    if os.geteuid() != 0:
        logger.error("This script must be run as root. Please run with sudo.")
        sys.exit("Error: Script requires root privileges. Please run with sudo.")

def detect_os():
    """Detect the operating system and return a standardized name."""
    os_system = platform.system()
    os_name = ""
    if os_system == "Linux":
        distro = platform.linux_distribution()[0].lower()
        if 'ubuntu' in distro or 'debian' in distro:
            os_name = 'debian'
        elif 'centos' in distro or 'fedora' in distro or 'red hat' in distro:
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
        else:
            pkg_manager = 'yum'
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
        if not is_command_available('brew'):
            logger.info("Homebrew not found. Installing Homebrew...")
            subprocess.run(['/bin/bash', '-c',
                            "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"],
                           check=True)
            # Add Homebrew to PATH
            os.environ['PATH'] += os.pathsep + '/usr/local/bin'
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
        'nmap',
        'nikto',
        'mutt',
        'default-jdk',      # For OWASP ZAP
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
        'java',             # For OWASP ZAP
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
            logger.info("Installing OWASP ZAP via apt repository...")
            # Add OWASP ZAP repository and install
            # Note: OWASP ZAP might not have official repos; alternatively, download and install manually
            zap_download_url = "https://github.com/zaproxy/zaproxy/releases/download/v2.13.0/ZAP_2.13.0_Linux.tar.gz"
            zap_install_dir = "/opt/zaproxy"
            os.makedirs(zap_install_dir, exist_ok=True)
            subprocess.run(['wget', '-O', f"{zap_install_dir}/ZAP.tar.gz", zap_download_url], check=True)
            subprocess.run(['tar', '-xzf', f"{zap_install_dir}/ZAP.tar.gz", '-C', zap_install_dir], check=True)
            logger.info("OWASP ZAP installed successfully.")
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
        print(f"Warning: The following commands are missing: {', '.join(missing_commands)}. Please install them manually if needed.")
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
