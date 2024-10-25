# Automated Pentesting Application

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Installation on Debian-Based Systems (e.g., Ubuntu, Debian)](#installation-on-debian-based-systems-e-g-ubuntu-debian)
  - [Installation on RedHat-Based Systems (e.g., CentOS, Fedora, RHEL)](#installation-on-redhat-based-systems-e-g-centos-fedora-rhel)
  - [Installation on macOS](#installation-on-macos)
  - [Using Docker (Optional)](#using-docker-optional)
  - [Post-Installation](#post-installation)
- [Usage](#usage)
  - [Starting the Application](#starting-the-application)
  - [Running Scans Manually](#running-scans-manually)
  - [Scheduling Automated Scans](#scheduling-automated-scans)
  - [Viewing Reports](#viewing-reports)
  - [Updating Tools](#updating-tools)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

The **Automated Pentesting Application** is a comprehensive tool designed for ethical bug bounty hunting and penetration testing. It automates every step of domain and web application pentesting, ensuring thorough vulnerability assessments with minimal manual intervention. The application is cloud-based, runs scheduled scans on eligible domains from HackerOne programs, and generates detailed reports in multiple formats.

## Features

- **Cloud-Based Execution**: Runs seamlessly on cloud servers, ensuring high availability and scalability.
- **Automated Scheduling**: Executes pentesting scripts four times a day on randomly selected in-scope domains from HackerOne programs that offer bounties.
- **Comprehensive Reporting**: Generates detailed reports in Markdown, JSON, and HTML formats.
- **OWASP Top 10 Scanning**: Identifies vulnerabilities based on the OWASP Top 10 security risks.
- **Email Notifications**: Automatically emails reports to specified recipients using `mutt`.
- **Auto-Updating**: Keeps all pentesting tools and dependencies up-to-date automatically.
- **Robust Error Handling**: Handles errors gracefully with comprehensive logging for debugging and analysis.
- **Optimized Performance**: Utilizes multithreading to perform scans efficiently and reduce execution time.

## Technologies Used

- **Programming Language**: Python 3
- **Pentesting Tools**:
  - [Nmap](https://nmap.org/)
  - [Nikto](https://cirt.net/Nikto2)
  - [OWASP ZAP](https://www.zaproxy.org/)
  - [Mutt](http://www.mutt.org/)
- **Libraries & Frameworks**:
  - [Requests](https://docs.python-requests.org/)
  - [Jinja2](https://jinja.palletsprojects.com/)
  - [PyYAML](https://pyyaml.org/)
  - [Schedule](https://schedule.readthedocs.io/)
- **Others**:
  - [Git](https://git-scm.com/)
  - [Docker](https://www.docker.com/) (Optional for containerization)

## Directory Structure

```
pentest_automation/
├── config/
│   ├── config.yaml
│   └── logging.conf
├── reports/
│   ├── markdown/
│   ├── json/
│   └── html/
├── scripts/
│   ├── run_all.sh
│   ├── update_tools.sh
│   └── setup_dependencies.py
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── domain_selection.py
│   ├── scanning/
│   │   ├── __init__.py
│   │   ├── nmap_scan.py
│   │   └── nikto_scan.py
│   ├── reporting/
│   │   ├── __init__.py
│   │   ├── report_generator.py
│   │   └── email_reporter.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py
│   │   ├── error_handler.py
│   │   └── updater.py
│   └── scheduler.py
├── logs/
│   ├── pentest_automation.log
│   ├── run_all.log
│   └── update_tools.log
├── tools/
│   ├── owasp_zap/
│   ├── nmap/
│   └── nikto/
├── tests/
│   ├── __init__.py
│   ├── test_domain_selection.py
│   ├── test_scanning.py
│   ├── test_reporting.py
│   └── test_utils.py
├── .gitignore
├── requirements.txt
├── README.md
├── INSTALL.md
├── USAGE.md
└── Dockerfile
```

## Installation

### Prerequisites

Before proceeding with the installation, ensure that your system meets the following requirements:

- **Operating System**: Debian-based, RedHat-based, or macOS.
- **Python 3.x**: Installed on the system.
- **Internet Connectivity**: Required to download and install packages.
- **Sudo Privileges**: Necessary for installing system packages.
- **Git**: To clone the repository (optional but recommended).

### Installation on Debian-Based Systems (e.g., Ubuntu, Debian)

1. **Update System Packages**

   Open a terminal and run:

   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   ```

2. **Install Git (If Not Already Installed)**

   ```bash
   sudo apt-get install -y git
   ```

3. **Clone the Repository**

   Navigate to your desired directory and clone the project:

   ```bash
   git clone https://github.com/jzuercher123/automatic_bug_hunter.git
   cd pentest_automation
   ```

4. **Run the Dependency Setup Script**

   Execute the `setup_dependencies.py` script to install system and Python dependencies:

   ```bash
   sudo python3 scripts/setup_dependencies.py
   ```

5. **Install Additional Dependencies (If Needed)**

   If you encounter any missing dependencies during setup, refer to the [Troubleshooting](#troubleshooting) section.

### Installation on RedHat-Based Systems (e.g., CentOS, Fedora, RHEL)

1. **Update System Packages**

   Open a terminal and run:

   ```bash
   sudo yum update -y
   ```

   *For systems using `dnf` (e.g., Fedora), replace `yum` with `dnf`.*

2. **Install Git (If Not Already Installed)**

   ```bash
   sudo yum install -y git
   ```

3. **Clone the Repository**

   Navigate to your desired directory and clone the project:

   ```bash
   git clone https://github.com/yourusername/pentest_automation.git
   cd pentest_automation
   ```

4. **Run the Dependency Setup Script**

   Execute the `setup_dependencies.py` script to install system and Python dependencies:

   ```bash
   sudo python3 scripts/setup_dependencies.py
   ```

5. **Install Additional Dependencies (If Needed)**

   If you encounter any missing dependencies during setup, refer to the [Troubleshooting](#troubleshooting) section.

### Installation on macOS

1. **Install Homebrew (If Not Already Installed)**

   Homebrew is a package manager for macOS. Install it by running:

   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Update Homebrew**

   ```bash
   brew update
   ```

3. **Install Git (If Not Already Installed)**

   ```bash
   brew install git
   ```

4. **Clone the Repository**

   Navigate to your desired directory and clone the project:

   ```bash
   git clone https://github.com/yourusername/pentest_automation.git
   cd pentest_automation
   ```

5. **Run the Dependency Setup Script**

   Execute the `setup_dependencies.py` script to install system and Python dependencies:

   ```bash
   sudo python3 scripts/setup_dependencies.py
   ```

   *Note: macOS may prompt you for your password when using `sudo`.*

6. **Install Additional Dependencies (If Needed)**

   If you encounter any missing dependencies during setup, refer to the [Troubleshooting](#troubleshooting) section.

### Using Docker (Optional)

If you prefer containerization for consistent environments across different systems, follow these steps:

1. **Install Docker**

   - **macOS**: Install Docker Desktop from [here](https://www.docker.com/products/docker-desktop).
   - **Debian-Based Systems**:

     ```bash
     sudo apt-get update
     sudo apt-get install -y docker.io
     sudo systemctl start docker
     sudo systemctl enable docker
     ```

   - **RedHat-Based Systems**:

     ```bash
     sudo yum install -y docker
     sudo systemctl start docker
     sudo systemctl enable docker
     ```

2. **Build the Docker Image**

   Navigate to the project's root directory and build the Docker image:

   ```bash
   docker build -t pentest_automation .
   ```

3. **Run the Docker Container**

   ```bash
   docker run -d --name pentest_automation pentest_automation
   ```

   *Note: Ensure that necessary ports are exposed and volumes are mounted if required.*

## Post-Installation

After completing the installation steps, perform the following:

1. **Configure the Application**:

   - Edit the `config/config.yaml` file to include your HackerOne API token, email credentials, and other configurations.

2. **Verify Installations**:

   - Ensure all dependencies are installed by running:

     ```bash
     ./scripts/run_all.sh
     ```

   - Check the `logs/` directory for logs to confirm successful execution.

3. **Set Up Scheduling**:

   - Use `cron` or the built-in scheduler to run the application four times a day.

   - Example `cron` entry (runs at midnight, 6 AM, 12 PM, and 6 PM):

     ```bash
     0 0,6,12,18 * * * /path/to/pentest_automation/scripts/run_all.sh
     ```

## Usage

### Starting the Application

Use the provided shell scripts to execute your automated pentesting application. There are two primary scripts:

1. **Run the Application**: Executes the pentesting cycle once.
2. **Update Tools**: Updates system packages and pentesting tools to their latest versions.

#### 1. Running the Application

Use the `run_all.sh` script to execute the pentesting application:

```bash
./scripts/run_all.sh
```

**What It Does**:

- Sets up and activates a Python virtual environment.
- Installs or updates Python dependencies.
- Executes the main application (`src/main.py`), which performs the following:
  - Fetches eligible domains from HackerOne.
  - Runs vulnerability scans (Nmap, Nikto, OWASP ZAP) on selected domains.
  - Generates comprehensive reports in Markdown, JSON, and HTML formats.
  - Emails the reports to specified recipients.

**Logs**:

- Execution logs are stored in `logs/run_all.log`.
- Detailed information and any errors during the run can be reviewed here.

#### 2. Updating Tools

Regularly update the application's dependencies and tools using the `update_tools.sh` script:

```bash
sudo ./scripts/update_tools.sh
```

**What It Does**:

- Updates system packages using the appropriate package manager.
- Updates or installs pentesting tools like Nmap, Nikto, Mutt, Java, and OWASP ZAP.
- Upgrades Python dependencies within the virtual environment.
- Logs the update process in `logs/update_tools.log`.

### Running Scans Manually

If you prefer to run specific scans manually without executing the entire application, you can directly invoke the scanning modules.

#### 1. Nmap Scan

```bash
# Activate the virtual environment
source venv/bin/activate

# Run the Nmap scan script
python3 src/scanning/nmap_scan.py --target example.com --output_dir reports/nmap/example.com/
```

**Parameters**:

- `--target`: The domain or IP address to scan.
- `--output_dir`: Directory to store the scan results.

#### 2. Nikto Scan

```bash
# Activate the virtual environment
source venv/bin/activate

# Run the Nikto scan script
python3 src/scanning/nikto_scan.py --target example.com --output_dir reports/nikto/example.com/
```

**Parameters**:

- `--target`: The domain or IP address to scan.
- `--output_dir`: Directory to store the scan results.

#### 3. OWASP ZAP Scan

OWASP ZAP is integrated within the main application. However, you can manually initiate it as follows:

```bash
# Activate the virtual environment
source venv/bin/activate

# Run the OWASP ZAP scan
python3 src/scanning/owasp_zap.py --target example.com --output_dir reports/zap/example.com/
```

**Parameters**:

- `--target`: The domain or IP address to scan.
- `--output_dir`: Directory to store the scan results.

*Note: Ensure that OWASP ZAP is installed and accessible.*

### Scheduling Automated Scans

To automate the execution of pentesting cycles, schedule the `run_all.sh` script to run at desired intervals using `cron` or other scheduling tools.

#### Using Cron

1. **Open the Crontab Editor**:

   ```bash
   crontab -e
   ```

2. **Add Cron Entries**:

   For example, to run the application four times a day at specific times:

   ```cron
   # Run at 00:15, 06:45, 12:30, and 18:00 every day
   15 0 * * * /path/to/pentest_automation/scripts/run_all.sh
   45 6 * * * /path/to/pentest_automation/scripts/run_all.sh
   30 12 * * * /path/to/pentest_automation/scripts/run_all.sh
   0 18 * * * /path/to/pentest_automation/scripts/run_all.sh
   ```

   *Adjust the times (`minute hour`) as per your preference.*

3. **Save and Exit**:

   - In `vim`, press `Esc`, type `:wq`, and press `Enter`.
   - In `nano`, press `Ctrl + O` to save and `Ctrl + X` to exit.

#### Using Systemd Timer (For Systems with Systemd)

1. **Create a Service File**: `/etc/systemd/system/pentest_automation.service`

   ```ini
   [Unit]
   Description=Automated Pentesting Application

   [Service]
   Type=oneshot
   ExecStart=/path/to/pentest_automation/scripts/run_all.sh
   ```

2. **Create a Timer File**: `/etc/systemd/system/pentest_automation.timer`

   ```ini
   [Unit]
   Description=Run Automated Pentesting Application Every 6 Hours

   [Timer]
   OnCalendar=*-*-* 00,06,12,18:00:00
   Persistent=true

   [Install]
   WantedBy=timers.target
   ```

3. **Enable and Start the Timer**:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable pentest_automation.timer
   sudo systemctl start pentest_automation.timer
   ```

4. **Check Timer Status**:

   ```bash
   systemctl list-timers --all
   ```

*Refer to [Systemd Timers](https://www.freedesktop.org/software/systemd/man/systemd.timer.html) for more configurations.*

### Viewing Reports

After scans are completed, reports are generated in the `reports/` directory in three formats:

- **Markdown**: `reports/markdown/example.com.md`
- **JSON**: `reports/json/example.com.json`
- **HTML**: `reports/html/example.com.html`

#### Accessing Reports

1. **Markdown Reports**:

   Use any Markdown viewer or text editor to view the `.md` files.

   ```bash
   cat reports/markdown/example.com.md
   ```

2. **JSON Reports**:

   Use tools like `jq` or any JSON viewer to parse and analyze.

   ```bash
   jq . reports/json/example.com.json
   ```

3. **HTML Reports**:

   Open the `.html` files in a web browser for a formatted view.

   ```bash
   open reports/html/example.com.html   # macOS
   xdg-open reports/html/example.com.html # Linux
   ```

#### Email Reports

The application automatically emails the generated reports to the specified recipient(s) using `mutt`. Ensure that email configurations in `config/config.yaml` are correctly set.

### Updating Tools

Regularly update system packages and pentesting tools to ensure optimal performance and security.

#### Using the Update Script

Execute the `update_tools.sh` script to update all dependencies and tools:

```bash
sudo ./scripts/update_tools.sh
```

**What It Does**:

- Updates system packages using the appropriate package manager.
- Updates or installs pentesting tools like Nmap, Nikto, Mutt, Java, and OWASP ZAP.
- Upgrades Python dependencies within the virtual environment.
- Logs the update process in `logs/update_tools.log`.

#### Manual Updates

If you prefer manual updates, refer to the [Installation](#installation) section for instructions on updating individual components.

## Logging

The application maintains detailed logs for monitoring and troubleshooting purposes.

- **Main Log**: `logs/pentest_automation.log`
- **Run Logs**: `logs/run_all.log`
- **Update Logs**: `logs/update_tools.log`

### Viewing Logs

Use `cat`, `less`, or any text editor to view log files.

```bash
cat logs/run_all.log
```

*For real-time monitoring:*

```bash
tail -f logs/run_all.log
```

## Troubleshooting

If you encounter issues while using the application, consider the following steps:

- **Check Logs**: Review the relevant log files in the `logs/` directory for error messages and debugging information.
- **Verify Configurations**:
  - Ensure that `config/config.yaml` is correctly set with valid API tokens and email credentials.
  - Confirm that the virtual environment is activated when running scans.
- **Dependency Issues**:
  - Run the `update_tools.sh` script to ensure all tools and dependencies are up-to-date.
  - Reinstall any missing packages as indicated in the logs.
- **Permission Problems**:
  - Ensure that scripts have executable permissions.
  - Run scripts with `sudo` if necessary.
- **Email Sending Failures**:
  - Verify SMTP settings and credentials in `config/config.yaml`.
  - Check network connectivity and firewall settings that might block SMTP ports.
- **Scan Failures**:
  - Ensure that target domains are in scope and that you have authorization to perform scans.
  - Check network connectivity and DNS resolution for target domains.

For further assistance, refer to the [Contact](#contact) section below or open an issue in the repository.

## Contributing

Contributions are welcome! Please follow these steps to contribute to the project:

1. **Fork the Repository**

   Click the "Fork" button at the top-right corner of the repository page to create a personal copy.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/yourusername/pentest_automation.git
   cd pentest_automation
   ```

3. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

4. **Make Your Changes**

   Implement your feature or bug fix.

5. **Commit Your Changes**

   ```bash
   git commit -m "Add feature: YourFeatureName"
   ```

6. **Push to Your Fork**

   ```bash
   git push origin feature/YourFeatureName
   ```

7. **Open a Pull Request**

   Navigate to the original repository and click on "Compare & pull request" to submit your changes.

### Code of Conduct

Please adhere to the [Code of Conduct](CODE_OF_CONDUCT.md) when contributing to this project.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or support, please contact [your.email@example.com](mailto:your.email@example.com).

---

**Note**: Always operate within legal and ethical boundaries. Obtain necessary permissions before performing any scans or penetration testing activities.