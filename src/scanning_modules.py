from target_management import Target, Scan
from abc import ABC, abstractmethod


class Module(ABC):
    def __init__(self, name: str):
        self.name = name
        self.description = ""
        self.enabled: bool = True

    @abstractmethod
    def run(self, target: Target, scan: Scan):
        pass


class PortScan(Module):
    def __init__(self):
        super().__init__("Port Scan")
        self.description = "Scans the target for open ports."
        self.enabled = True

    def run(self, target: Target, scan: Scan):
        target.resolve_host()
        target.scan_ports()
        scan.vulnerabilities.append("Open ports: " + ", ".join(map(str, target.ports)))


class ServiceScanner(Module):
    def __init__(self):
        super().__init__("Service Scanner")
        self.description = "Scans the target for running services."
        self.enabled = True

    def run(self, target: Target, scan: Scan):
        scan.vulnerabilities.append("Running services: " + ", ".join(target.protocols))


class VulnerabilityScanner(Module):
    def __init__(self, name: str):
        super().__init__("Vulnerability Scanner")
        self.name = name
        self.description = "Scans the target for vulnerabilities."
        self.enabled = True

    def run(self, target: Target, scan: Scan):
        scan.vulnerabilities.append("No vulnerabilities found.")


class WebCrawler(Module):
    def __init__(self):
        super().__init__("Web Crawler")
        self.description = "Crawls the target website for links."
        self.enabled = True

    def run(self, target: Target, scan: Scan):
        scan.vulnerabilities.append("Crawled links: " + ", ".join(target.links))


# functions
def tcp_connect_scan(target: Target):
    target.resolve_host()
    target.scan_ports()
    return target.ports

def udp_scan(target: Target):
    target.resolve_host()
    target.scan_ports()
    return target.ports

def identify_services(target: Target):
    return target.protocols
