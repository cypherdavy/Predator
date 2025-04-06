import json
import os
import jsonschema
from pathlib import Path

TEMPLATE_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "severity": {"enum": ["critical", "high", "medium", "low", "info"]},
        "description": {"type": "string"},
        "target": {"type": "string"},
        "method": {"enum": ["GET", "POST", "PUT", "DELETE", "PATCH"]},
        "headers": {"type": "object"},
        "payload": {"type": "string"},
        "matchers": {
            "type": "object",
            "properties": {
                "status": {"type": "array", "items": {"type": "integer"}},
                "regex": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["status"]
        },
        "poc_regex": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["id", "severity", "target", "method", "matchers"]
}

class TemplateManager:
    def __init__(self, template_path):
        self.template_path = template_path
        self.templates = []
        self._load()

    def _load(self):
        if os.path.isdir(self.template_path):
            self._load_from_directory()
        else:
            self._load_from_file()

    def _load_from_directory(self):
        for root, _, files in os.walk(self.template_path):
            for file in files:
                if file.endswith('.json'):
                    self._process_template(Path(root) / file)

    def _load_from_file(self):
        self._process_template(Path(self.template_path))

    def _process_template(self, path):
        with open(path) as f:
            try:
                template = json.load(f)
                jsonschema.validate(template, TEMPLATE_SCHEMA)
                self.templates.append(template)
            except (json.JSONDecodeError, jsonschema.ValidationError) as e:
                print(f"Invalid template {path}: {str(e)}")
