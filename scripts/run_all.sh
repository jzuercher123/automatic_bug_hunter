#!/bin/bash

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
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"
echo_info "Activated the Python virtual environment."

# Upgrade pip
echo_info "Upgrading pip."
pip install --upgrade pip

# Install Python dependencies
echo_info "Installing Python dependencies from requirements.txt."
pip install -r "$PROJECT_DIR/requirements.txt"

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
