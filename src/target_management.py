import socket
from urllib.parse import urlparse
import nmap
from datetime import datetime
from typing import Optional
from vulnerability_detection import Vulnerability

class Target:
    def __init__(self, url):
        self.url = url
        self.parsed_url = urlparse(self.url)
        self.ip_address = None
        self.hosts = []
        self.ports = []
        self.protocols = []

    def resolve_host(self):
        self.ip_address = socket.gethostbyname(self.parsed_url.netloc)
        self.hosts = socket.gethostbyaddr(self.ip_address)
        self.ports = [80, 443]
        self.protocols = ["http", "https"]

    def scan_ports(self):
        scanner = nmap.PortScanner()
        scanner.scan(self.ip_address, arguments="-p 80,443")
        self.ports = [int(port) for port in scanner[self.ip_address]['tcp'].keys()]


class Scan:
    def __init__(self, target: Target, scan_type: str):
        self.scan_id = None
        self.target = target
        self.scan_type = scan_type
        self.start_time = datetime.now()
        self.end_time = Optional[datetime]
        self.status = ""
        self.vulnerabilities = list[Vulnerability]
        self.payloads_used = list[Payload]
        self.configuration =

    def start_scan(self):
        self.status = "In Progress"

    def complete_scan(self):
        self.end_time = datetime.now()
        self.status = "Completed"

