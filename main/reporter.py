import json
import csv
from html import escape
from datetime import datetime

class ReportGenerator:
    def __init__(self, results):
        self.results = results
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def generate(self, format):
        if format == 'json':
            self._generate_json()
        elif format == 'csv':
            self._generate_csv()
        elif format == 'html':
            self._generate_html()
        elif format == 'all':
            self._generate_json()
            self._generate_csv()
            self._generate_html()

    def _generate_json(self):
        filename = f"predator_report_{self.timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)

    def _generate_csv(self):
        filename = f"predator_report_{self.timestamp}.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
            writer.writeheader()
            writer.writerows(self.results)

    def _generate_html(self):
        filename = f"predator_report_{self.timestamp}.html"
        with open(filename, 'w') as f:
            f.write("<html><body>")
            f.write("<h1>Predator Scan Report</h1>")
            f.write("<table border='1'>")
            f.write("<tr><th>Target</th><th>Severity</th><th>PoC</th></tr>")
            
            for result in self.results:
                f.write(f"<tr>"
                        f"<td>{escape(result['target'])}</td>"
                        f"<td>{result['severity'].capitalize()}</td>"
                        f"<td>{escape(str(result['poc']))}</td>"
                        f"</tr>")
            
            f.write("</table></body></html>")
