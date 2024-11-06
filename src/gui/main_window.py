import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QTabWidget, QFileDialog,
    QMessageBox, QListWidget, QListWidgetItem, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal

from src.domain_selection import fetch_scoped_domains
from src.scanning.nmap_scan import run_nmap_scan
from src.scanning.nikto_scan import run_nikto_scan
from src.utils.logger import safe_run

import logging

# Set up logger
logger = safe_run('GUI', 'logs/pentest_gui.log', logging.DEBUG)


class ScanThread(QThread):
    progress = Signal(str)
    finished = Signal(dict)

    def __init__(self, domain, scan_types):
        super().__init__()
        self.domain = domain
        self.scan_types = scan_types

    def run(self):
        results = {}
        try:
            if 'Nmap' in self.scan_types:
                self.progress.emit('Starting Nmap scan...')
                nmap_result = run_nmap_scan(self.domain, f'reports/nmap/{self.domain}/')
                results['nmap'] = nmap_result
                self.progress.emit('Nmap scan completed.')

            if 'Nikto' in self.scan_types:
                self.progress.emit('Starting Nikto scan...')
                nikto_result = run_nikto_scan(self.domain, f'reports/nikto/{self.domain}/')
                results['nikto'] = nikto_result
                self.progress.emit('Nikto scan completed.')

            # Add other scans here

            self.finished.emit(results)
        except Exception as e:
            logger.error(f"ScanThread encountered an error: {e}")
            self.finished.emit(results)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Automated Pentesting Application")
        self.setGeometry(100, 100, 800, 600)

        # Main widget and layout
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout()

        # Tabs
        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        # Domain Selection Tab
        self.domain_tab = QWidget()
        self.domain_layout = QVBoxLayout()

        self.domain_input_layout = QHBoxLayout()
        self.domain_label = QLabel("Domain:")
        self.domain_input = QLineEdit()
        self.add_domain_button = QPushButton("Add Domain")
        self.add_domain_button.clicked.connect(self.add_domain)

        self.domain_input_layout.addWidget(self.domain_label)
        self.domain_input_layout.addWidget(self.domain_input)
        self.domain_input_layout.addWidget(self.add_domain_button)

        self.domain_layout.addLayout(self.domain_input_layout)

        self.domain_list = QListWidget()
        self.domain_layout.addWidget(self.domain_list)

        self.fetch_domains_button = QPushButton("Fetch In-Scope Domains")
        self.fetch_domains_button.clicked.connect(self.fetch_in_scope_domains)
        self.domain_layout.addWidget(self.fetch_domains_button)

        self.domain_tab.setLayout(self.domain_layout)
        self.tabs.addTab(self.domain_tab, "Domain Selection")

        # Scan Controls Tab
        self.scan_tab = QWidget()
        self.scan_layout = QVBoxLayout()

        self.scan_types_layout = QHBoxLayout()
        self.nmap_checkbox = QPushButton("Nmap", checkable=True)
        self.nikto_checkbox = QPushButton("Nikto", checkable=True)
        self.zap_checkbox = QPushButton("OWASP ZAP", checkable=True)

        self.scan_types_layout.addWidget(self.nmap_checkbox)
        self.scan_types_layout.addWidget(self.nikto_checkbox)
        self.scan_types_layout.addWidget(self.zap_checkbox)

        self.scan_layout.addLayout(self.scan_types_layout)

        self.start_scan_button = QPushButton("Start Scan")
        self.start_scan_button.clicked.connect(self.start_scan)
        self.scan_layout.addWidget(self.start_scan_button)

        self.progress_bar = QProgressBar()
        self.scan_layout.addWidget(self.progress_bar)

        self.scan_tab.setLayout(self.scan_layout)
        self.tabs.addTab(self.scan_tab, "Scan Controls")

        # Reports Tab
        self.report_tab = QWidget()
        self.report_layout = QVBoxLayout()

        self.view_report_button = QPushButton("View Latest Report")
        self.view_report_button.clicked.connect(self.view_report)
        self.report_layout.addWidget(self.view_report_button)

        self.report_display = QTextEdit()
        self.report_display.setReadOnly(True)
        self.report_layout.addWidget(self.report_display)

        self.export_report_button = QPushButton("Export Report")
        self.export_report_button.clicked.connect(self.export_report)
        self.report_layout.addWidget(self.export_report_button)

        self.report_tab.setLayout(self.report_layout)
        self.tabs.addTab(self.report_tab, "Reports")

        # Logs Tab
        self.logs_tab = QWidget()
        self.logs_layout = QVBoxLayout()

        self.view_logs_button = QPushButton("View Logs")
        self.view_logs_button.clicked.connect(self.view_logs)
        self.logs_layout.addWidget(self.view_logs_button)

        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.logs_layout.addWidget(self.log_display)

        self.logs_tab.setLayout(self.logs_layout)
        self.tabs.addTab(self.logs_tab, "Logs")

        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

    def add_domain(self):
        domain = self.domain_input.text().strip()
        if domain:
            item = QListWidgetItem(domain)
            self.domain_list.addItem(item)
            self.domain_input.clear()
            logger.info(f"Added domain: {domain}")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid domain.")

    def fetch_in_scope_domains(self):
        try:
            domains = self.domain_selector.fetch_in_scope_domains()
            self.domain_list.clear()
            for domain in domains:
                item = QListWidgetItem(domain)
                self.domain_list.addItem(item)
            logger.info("Fetched and displayed in-scope domains.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to fetch in-scope domains: {e}")
            logger.error(f"Failed to fetch in-scope domains: {e}")

    def start_scan(self):
        selected_items = self.domain_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Selection Error", "Please select at least one domain to scan.")
            return

        scan_types = []
        if self.nmap_checkbox.isChecked():
            scan_types.append('Nmap')
        if self.nikto_checkbox.isChecked():
            scan_types.append('Nikto')
        if self.zap_checkbox.isChecked():
            scan_types.append('OWASP ZAP')

        if not scan_types:
            QMessageBox.warning(self, "Selection Error", "Please select at least one scan type.")
            return

        domains = [item.text() for item in selected_items]

        self.progress_bar.setValue(0)
        self.scan_thread = ScanThread(domain=domains[0], scan_types=scan_types)  # Modify to handle multiple domains
        self.scan_thread.progress.connect(self.update_progress)
        self.scan_thread.finished.connect(self.scan_finished)
        self.scan_thread.start()

    def update_progress(self, message):
        self.progress_bar.setFormat(message)
        logger.info(message)

    def scan_finished(self, results):
        self.progress_bar.setValue(100)
        QMessageBox.information(self, "Scan Completed", "The scan has been completed successfully.")
        logger.info("Scan process finished.")


    def view_report(self):
        report_path, _ = QFileDialog.getOpenFileName(self, "Open Report", "reports/",
                                                     "HTML Files (*.html);;Markdown Files (*.md);;JSON Files (*.json)")
        if report_path:
            try:
                with open(report_path, 'r') as file:
                    content = file.read()
                self.report_display.setPlainText(content)
                logger.info(f"Opened report: {report_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open report: {e}")
                logger.error(f"Failed to open report: {e}")

    def export_report(self):
        report_path, _ = QFileDialog.getSaveFileName(self, "Export Report", "",
                                                     "HTML Files (*.html);;Markdown Files (*.md);;JSON Files (*.json)")
        if report_path:
            try:
                with open(report_path, 'w') as file:
                    file.write(self.report_display.toPlainText())
                QMessageBox.information(self, "Export Successful", f"Report exported to {report_path}")
                logger.info(f"Exported report to: {report_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export report: {e}")
                logger.error(f"Failed to export report: {e}")

    def view_logs(self):
        log_path, _ = QFileDialog.getOpenFileName(self, "Open Log", "logs/", "Log Files (*.log);;All Files (*)")
        if log_path:
            try:
                with open(log_path, 'r') as file:
                    content = file.read()
                self.log_display.setPlainText(content)
                logger.info(f"Opened log file: {log_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open log file: {e}")
                logger.error(f"Failed to open log file: {e}")


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
