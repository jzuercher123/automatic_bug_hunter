#!/usr/bin/env bash

# run_all.sh
# This script sets up the environment and runs the automated pentesting application.

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
SRC_DIR="$PROJECT_DIR/src"
LOGS_DIR="$PROJECT_DIR/logs"
VENV_DIR="$PROJECT_DIR/venv"

# Create logs directory if it doesn't exist
mkdir -p "$LOGS_DIR"

# Log file
LOG_FILE="$LOGS_DIR/run_all.log"

# Start logging
exec > >(tee -a "$LOG_FILE") 2>&1

echo_info "Starting the automated pentesting application."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo_error "Python3 could not be found. Please install Python3 before running this script."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null
then
    echo_error "pip3 could not be found. Please install pip3 before running this script."
    exit 1
fi

# Optional: Set up a Python virtual environment
if [ ! -d "$VENV_DIR" ]; then
    echo_info "Creating a Python virtual environment."
    python3 -m venv "$VENV_DIR"
    echo_info "Virtual environment created at $VENV_DIR."
else
    echo_info "Python virtual environment already exists at $VENV_DIR."
fi

# Activate the virtual environment
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
    echo_info "Activated the Python virtual environment."
else
    echo_error "Activation script not found at $VENV_DIR/bin/activate."
    echo_error "Recreating the virtual environment."
    rm -rf "$VENV_DIR"
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    echo_info "Recreated and activated the Python virtual environment."
fi

# Upgrade pip
echo_info "Upgrading pip."
pip install --upgrade pip

# Check if requirements.txt exists
if [ ! -f "$PROJECT_DIR/requirements.txt" ]; then
    echo_error "requirements.txt not found at $PROJECT_DIR/requirements.txt."
    deactivate
    exit 1
fi

# Install Python dependencies
echo_info "Installing Python dependencies from requirements.txt."
pip install -r "$PROJECT_DIR/requirements.txt"

# Verify that required Python packages are installed
REQUIRED_PYTHON_PACKAGES=("markdown") # Add other packages as needed
MISSING_PACKAGES=()

for pkg in "${REQUIRED_PYTHON_PACKAGES[@]}"; do
    pip show "$pkg" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        MISSING_PACKAGES+=("$pkg")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -ne 0 ]; then
    echo_info "Installing missing Python packages: ${MISSING_PACKAGES[@]}"
    pip install "${MISSING_PACKAGES[@]}"
else
    echo_info "All required Python packages are already installed."
fi

# Ensure the main application exists
MAIN_APP="$SRC_DIR/main.py"
if [ ! -f "$MAIN_APP" ]; then
    echo_error "Main application script not found at $MAIN_APP."
    deactivate
    exit 1
fi

# Run the main application
echo_info "Executing the main application: $MAIN_APP."
python3 "$MAIN_APP"

# Deactivate the virtual environment after execution
deactivate
echo_info "Deactivated the Python virtual environment."

echo_info "Automated pentesting application has completed execution."
