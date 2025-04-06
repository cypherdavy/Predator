import queue
import threading
import requests
import re
from datetime import datetime

class PredatorScanner:
    def __init__(self, targets, templates, thread_count=50):
        self.target_queue = queue.Queue()
        self.template_queue = queue.Queue()
        self.results = []
        self.lock = threading.Lock()
        self.scan_stats = {
            'total': 0, 
            'vulnerable': 0,
            'critical': 0,
            'high': 0,
            'medium': 0
        }

        self._load_targets(targets)
        self._load_templates(templates)
        self._start_workers(thread_count)

    def _load_targets(self, targets):
        for target in targets:
            self.target_queue.put(target)

    def _load_templates(self, templates):
        for template in templates:
            self.template_queue.put(template)

    def _start_workers(self, thread_count):
        for _ in range(thread_count):
            threading.Thread(target=self._worker, daemon=True).start()

    def _worker(self):
        while True:
            target = self.target_queue.get()
            template = self.template_queue.get()
            
            try:
                response = self._send_request(target, template)
                if self._is_vulnerable(response, template):
                    self._record_finding(target, template, response)
            except Exception:
                pass
            finally:
                self.target_queue.task_done()
                self.template_queue.task_done()

    def _send_request(self, target, template):
        url = template['target'].replace("{{BaseURL}}", target)
        return requests.request(
            template.get('method', 'GET'),
            url,
            headers=template.get('headers', {}),
            data=template.get('payload'),
            timeout=15,
            verify=False
        )

    def _is_vulnerable(self, response, template):
        if response.status_code not in template['matchers'].get('status', []):
            return False
        return any(
            re.search(pattern, response.text, re.IGNORECASE)
            for pattern in template['matchers'].get('regex', [])
        )

    def _record_finding(self, target, template, response):
        with self.lock:
            severity = template.get('severity', 'medium').lower()
            self.results.append({
                'target': target,
                'template_id': template['id'],
                'severity': severity,
                'status': response.status_code,
                'poc': self._extract_poc(response, template),
                'timestamp': datetime.now().isoformat(),
                'description': template.get('description', '')
            })
            self._update_stats(severity)

    def _extract_poc(self, response, template):
        if 'poc_regex' in template:
            match = re.search(template['poc_regex'], response.text)
            return match.group(0) if match else None
        return None

    def _update_stats(self, severity):
        self.scan_stats['total'] += 1
        self.scan_stats['vulnerable'] += 1
        if severity == 'critical':
            self.scan_stats['critical'] += 1
        elif severity == 'high':
            self.scan_stats['high'] += 1
        elif severity == 'medium':
            self.scan_stats['medium'] += 1
