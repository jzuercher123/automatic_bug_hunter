import json
from typing import Optional


class Configuration:
    def __init__(self):
        self.max_threads = 10
        self.timeout = 5  # seconds
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        self.proxies: Optional[dict[str, str]] = None
        self.verify_ssl = True

    def load_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.max_threads = data.get('max_threads', self.max_threads)
            self.timeout = data.get('timeout', self.timeout)
            self.user_agent = data.get('user_agent', self.user_agent)
            self.proxies = data.get('proxies', self.proxies)
            self.verify_ssl = data.get('verify_ssl', self.verify_ssl)

    def save_to_file(self, file_path: str):
        data = {
            'max_threads': self.max_threads,
            'timeout': self.timeout,
            'user_agent': self.user_agent,
            'proxies': self.proxies,
            'verify_ssl': self.verify_ssl
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
