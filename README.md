# Automated Pentesting Application

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Usage](#usage)
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

