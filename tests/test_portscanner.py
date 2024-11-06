from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from urllib.parse import urlparse
import socket
import threading
import nmap
from datetime import datetime
from src.scanning_modules import Module
from src.target_management import Target, Scan
from src.vulnerability_detection import Vulnerability


@dataclass
class PortScanner(Module):
    name: str = "PortScanner"
    description: str = "Scans for open TCP ports on the target."
    enabled: bool = True
    target: Target = field(default=None)
    port_range: Tuple[int, int] = (1, 1024)
    open_ports: List[int] = field(default_factory=list)
    scan: Scan = field(default=None)

    def run(self, target: Target, scan: Scan) -> None:
        self.target = target
        self.port_range = (1, 1024)  # Example port range
        threads = []
        for port in range(self.port_range[0], self.port_range[1] + 1):
            thread = threading.Thread(target=self.scan_port, args=(port,))
            threads.append(thread)
            thread.start()
            if len(threads) >= scan.configuration.max_threads:
                for t in threads:
                    t.join()
                threads = []
        # Join any remaining threads
        for t in threads:
            t.join()
        scan.end_time = datetime.now()
        scan.status = "Completed"

    def scan_port(self, port: int) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((self.target.ip_address, port))
            if result == 0:
                self.open_ports.append(port)
                Scan.vulnerabilities.append(Vulnerability(
                    vuln_id=len(scan.vulnerabilities) + 1,
                    name="Open Port",
                    description=f"Port {port} is open.",
                    severity="Low",
                    affected_component=f"Port {port}",
                    evidence=f"Port {port} on {self.target.ip_address} is open.",
                    scan=scan
                ))
