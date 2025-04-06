# Getting Started with Predator

## Installation
```
git clone https://github.com/yourusername/predator.git
cd predator
./scripts/install.sh
```

## Basic Usage
Scan single target:
```
predator -t http://example.com -T ~/.predator/templates
```

Scan multiple targets:
```
predator -t http://site1.com http://site2.com -T ./custom-templates -o json
```

## Updating Templates
```
predator --update
```

## Output Formats
Supported formats: JSON, CSV, HTML
```

