#!/bin/bash

# update_tools.sh
# This script updates system packages and pentesting tools to their latest versions.

# Exit immediately if a command exits with a non-zero status
set -e

# Function to display messages
function echo_info() {
    echo -e "\e[32m[INFO]\e[0m $1"
}

function echo_error() {
    echo -e "\e[31m[ERROR]\e[0m $1"
}

# Define project directories
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOGS_DIR="$PROJECT_DIR/logs"
VENV_DIR="$PROJECT_DIR/venv"

# Create logs directory if it doesn't exist
mkdir -p "$LOGS_DIR"

# Log file
LOG_FILE="$LOGS_DIR/update_tools.log"

# Start logging
exec > >(tee -a "$LOG_FILE") 2>&1

echo_info "Starting the tools update process."

# Check if the script is run as root
if [ "$EUID" -ne 0 ]
then
    echo_error "This script must be run as root. Please run with sudo."
    exit 1
fi

# Detect Operating System
OS_NAME=$(uname)
if [[ "$OS_NAME" == "Linux" ]]; then
    # Further distinguish between Debian-based and RedHat-based
    if [ -f /etc/debian_version ]; then
        DISTRO="debian"
    elif [ -f /etc/redhat-release ]; then
        DISTRO="redhat"
    else
        echo_error "Unsupported Linux distribution."
        exit 1
    fi
elif [[ "$OS_NAME" == "Darwin" ]]; then
    DISTRO="macos"
else
    echo_error "Unsupported operating system: $OS_NAME."
    exit 1
fi

echo_info "Detected OS: $DISTRO."

# Update system packages
if [[ "$DISTRO" == "debian" ]]; then
    echo_info "Updating package list for Debian-based system."
    apt-get update -y
    echo_info "Upgrading packages for Debian-based system."
    apt-get upgrade -y
elif [[ "$DISTRO" == "redhat" ]]; then
    echo_info "Updating package list for RedHat-based system."
    if command -v dnf &> /dev/null; then
        dnf makecache -y
        echo_info "Upgrading packages using dnf for RedHat-based system."
        dnf upgrade -y
    else
        yum makecache -y
        echo_info "Upgrading packages using yum for RedHat-based system."
        yum upgrade -y
    fi
elif [[ "$DISTRO" == "macos" ]]; then
    echo_info "Updating Homebrew."
    brew update
    echo_info "Upgrading Homebrew packages."
    brew upgrade
fi

# Update specific pentesting tools
echo_info "Updating pentesting tools."

# Update Nmap
if command -v nmap &> /dev/null; then
    echo_info "Updating Nmap."
    if [[ "$DISTRO" == "debian" ]]; then
        apt-get install --only-upgrade -y nmap
    elif [[ "$DISTRO" == "redhat" ]]; then
        if command -v dnf &> /dev/null; then
            dnf upgrade -y nmap
        else
            yum update -y nmap
        fi
    elif [[ "$DISTRO" == "macos" ]]; then
        brew upgrade nmap
    fi
else
    echo_info "Nmap is not installed. Installing Nmap."
    if [[ "$DISTRO" == "debian" ]]; then
        apt-get install -y nmap
    elif [[ "$DISTRO" == "redhat" ]]; then
        if command -v dnf &> /dev/null; then
            dnf install -y nmap
        else
            yum install -y nmap
        fi
    elif [[ "$DISTRO" == "macos" ]]; then
        brew install nmap
    fi
fi

# Update Nikto
if command -v nikto &> /dev/null; then
    echo_info "Updating Nikto."
    # Nikto is often updated via Git; assuming it's installed via package manager
    if [[ "$DISTRO" == "debian" ]]; then
        apt-get install --only-upgrade -y nikto
    elif [[ "$DISTRO" == "redhat" ]]; then
        if command -v dnf &> /dev/null; then
            dnf upgrade -y nikto
        else
            yum update -y nikto
        fi
    elif [[ "$DISTRO" == "macos" ]]; then
        brew upgrade nikto
    fi
else
    echo_info "Nikto is not installed. Installing Nikto."
    if [[ "$DISTRO" == "debian" ]]; then
        apt-get install -y nikto
    elif [[ "$DISTRO" == "redhat" ]]; then
        if command -v dnf &> /dev/null; then
            dnf install -y nikto
        else
            yum install -y nikto
        fi
    elif [[ "$DISTRO" == "macos" ]]; then
        brew install nikto
    fi
fi

# Update Mutt
if command -v mutt &> /dev/null; then
    echo_info "Updating Mutt."
    if [[ "$DISTRO" == "debian" ]]; then
        apt-get install --only-upgrade -y mutt
    elif [[ "$DISTRO" == "redhat" ]]; then
        if command -v dnf &> /dev/null; then
            dnf upgrade -y mutt
        else
            yum update -y mutt
        fi
    elif [[ "$DISTRO" == "macos" ]]; then
        brew upgrade mutt
    fi
else
    echo_info "Mutt is not installed. Installing Mutt."
    if [[ "$DISTRO" == "debian" ]]; then
        apt-get install -y mutt
    elif [[ "$DISTRO" == "redhat" ]]; then
        if command -v dnf &> /dev/null; then
            dnf install -y mutt
        else
            yum install -y mutt
        fi
    elif [[ "$DISTRO" == "macos" ]]; then
        brew install mutt
    fi
fi

# Update Java (required for OWASP ZAP)
if command -v java &> /dev/null; then
    echo_info "Updating Java."
    if [[ "$DISTRO" == "debian" ]]; then
        apt-get install --only-upgrade -y default-jdk
    elif [[ "$DISTRO" == "redhat" ]]; then
        if command -v dnf &> /dev/null; then
            dnf upgrade -y java-11-openjdk
        else
            yum update -y java-11-openjdk
        fi
    elif [[ "$DISTRO" == "macos" ]]; then
        brew upgrade java
    fi
else
    echo_info "Java is not installed. Installing Java."
    if [[ "$DISTRO" == "debian" ]]; then
        apt-get install -y default-jdk
    elif [[ "$DISTRO" == "redhat" ]]; then
        if command -v dnf &> /dev/null; then
            dnf install -y java-11-openjdk
        else
            yum install -y java-11-openjdk
        fi
    elif [[ "$DISTRO" == "macos" ]]; then
        brew install java
    fi
fi

# Update OWASP ZAP
echo_info "Updating OWASP ZAP."
if [[ "$DISTRO" == "debian" || "$DISTRO" == "redhat" ]]; then
    # Assuming OWASP ZAP is installed in /opt/zaproxy
    ZAP_DIR="/opt/zaproxy"
    if [ -d "$ZAP_DIR" ]; then
        echo_info "Updating OWASP ZAP in $ZAP_DIR."
        cd "$ZAP_DIR"
        # Fetch the latest release
        LATEST_ZAP_URL=$(curl -s https://api.github.com/repos/zaproxy/zaproxy/releases/latest | grep browser_download_url | grep tar.gz | cut -d '"' -f 4)
        echo_info "Downloading the latest OWASP ZAP from $LATEST_ZAP_URL."
        wget -q "$LATEST_ZAP_URL" -O ZAP_latest.tar.gz
        echo_info "Extracting the latest OWASP ZAP."
        tar -xzf ZAP_latest.tar.gz --strip-components=1
        rm ZAP_latest.tar.gz
        echo_info "OWASP ZAP updated successfully."
    else
        echo_error "OWASP ZAP directory not found at $ZAP_DIR. Please install OWASP ZAP first."
    fi
elif [[ "$DISTRO" == "macos" ]]; then
    echo_info "Updating OWASP ZAP via Homebrew."
    brew reinstall --cask owasp-zap
    echo_info "OWASP ZAP updated successfully."
fi

# Upgrade Python dependencies
echo_info "Upgrading Python dependencies."
# Activate virtual environment if it exists
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    echo_info "Activated the Python virtual environment."
    pip install --upgrade pip
    pip install --upgrade -r "$PROJECT_DIR/requirements.txt"
    deactivate
    echo_info "Deactivated the Python virtual environment."
else
    echo_info "Python virtual environment not found. Skipping Python dependencies upgrade."
fi

# Restart services or perform additional steps if necessary
# Example: Restarting the main application (optional)
# echo_info "Restarting the main application."
# ./run_all.sh &

echo_info "Tools update process completed successfully."
