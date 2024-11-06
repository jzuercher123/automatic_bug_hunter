"""
+------------+        +---------+        +---------------+
|   Target   |<-------|  Scan   |<-------| Vulnerability |
+------------+        +---------+        +---------------+
      ^                    ^                     ^
      |                    |                     |
+------------+        +---------+        +---------------+
| Credential |        | Payload |        |    Report     |
+------------+        +---------+        +---------------+
"""


from dataclasses import dataclass, field
from typing import List, Optional
from urllib.parse import urlparse
from datetime import datetime

@dataclass
class Target:
    url: str
    parsed_url: urlparse = field(init=False)
    ip_address: Optional[str] = None
    hosts: List[str] = field(default_factory=list)
    ports: List[int] = field(default_factory=list)
    protocols: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.parsed_url = urlparse(self.url)


@dataclass
class Scan:
    target: Target
    scan_type: str  # e.g., "XSS", "SQL Injection"
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str = "In Progress"
    vulnerabilities: List['Vulnerability'] = field(default_factory=list)
    payloads_used: List['Payload'] = field(default_factory=list)

    def complete_scan(self):
        self.end_time = datetime.now()
        self.status = "Completed"


@dataclass
class Vulnerability:
    vuln_id: int
    name: str
    description: str
    severity: str  # e.g., "Low", "Medium", "High", "Critical"
    affected_component: str
    evidence: str
    remediation: Optional[str] = None
    scan: Optional[Scan] = None


@dataclass
class Payload:
    payload_id: int
    content: str
    encoding: Optional[str] = None  # e.g., URL-encoded, Base64
    description: Optional[str] = None
    scan: Optional[Scan] = None


@dataclass
class Form:
    form_id: int
    action: str
    method: str  # GET or POST
    inputs: List['InputField']
    page_url: str

@dataclass
class InputField:
    name: str
    type: str  # text, password, hidden, etc.
    value: Optional[str] = None


@dataclass
class Endpoint:
    endpoint_id: int
    url: str
    method: str  # GET, POST, PUT, DELETE, etc.
    parameters: List[str]
    headers: dict = field(default_factory=dict)
    response_code: Optional[int] = None
    response_body: Optional[str] = None


from typing import Optional

@dataclass
class Report:
    report_id: int
    scan: Scan
    generated_on: datetime
    format: str  # e.g., HTML, PDF, JSON
    content: Optional[str] = None  # Path to the report file or raw content

    def generate_report_content(self):
        # Implementation to generate report content
        pass


@dataclass
class Credential:
    credential_id: int
    username: str
    password: str
    auth_type: str  # e.g., Basic, Token, OAuth
    target: Optional[Target] = None


@dataclass
class Configuration:
    max_threads: int = 10
    timeout: int = 5  # seconds
    user_agent: str = "PenTestTool/1.0"
    proxies: Optional[dict] = None
    verify_ssl: bool = True


@dataclass
class LogEntry:
    timestamp: datetime
    level: str  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    message: str
    context: Optional[dict] = None

@dataclass
class Logger:
    logs: List[LogEntry] = field(default_factory=list)

    def log(self, level: str, message: str, context: Optional[dict] = None):
        entry = LogEntry(timestamp=datetime.now(), level=level, message=message, context=context)
        self.logs.append(entry)
        # Optionally, print or write to a file
