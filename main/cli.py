import argparse
import json
import sys
from .reporter import ReportGenerator

class PredatorCLI:
    def __init__(self):
        self.parser = self._create_parser()
        self.args = self.parser.parse_args()
        self._validate_args()

    def _create_parser(self):
        parser = argparse.ArgumentParser(
            description='Predator - Advanced Vulnerability Scanner',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        
        parser.add_argument(
            '-t', '--targets',
            nargs='+',
            required=True,
            help='List of targets to scan'
        )
        
        parser.add_argument(
            '-T', '--templates',
            required=True,
            help='Path to template directory or file'
        )
        
        parser.add_argument(
            '-o', '--output',
            choices=['json', 'csv', 'html', 'all'],
            help='Output format for results'
        )
        
        parser.add_argument(
            '--threads',
            type=int,
            default=50,
            help='Number of concurrent threads'
        )
        
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update templates before scanning'
        )
        
        return parser

    def _validate_args(self):
        if self.args.update:
            self._update_templates()
        
        try:
            self.templates = self._load_templates()
        except FileNotFoundError:
            sys.exit("Error: Template path not found")

    def _load_templates(self):
        # Implement template loading logic
        pass

    def _update_templates(self):
        # Implement template update logic
        print("Updating templates...")

    def run(self):
        from .scanner import PredatorScanner
        scanner = PredatorScanner(self.args.targets, self.templates, self.args.threads)
        
        if self.args.output:
            ReportGenerator(scanner.results).generate(self.args.output)
