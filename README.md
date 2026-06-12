# Port Scanner

A Python-based network port scanning tool with multi-threading, service detection, and reporting capabilities.

## Features

- Multi-threaded port scanning for speed
- Service detection through banner grabbing
- Progress visualization with Rich
- Export reports to HTML, PDF, and text formats
- Configurable timeout and thread count
- Support for custom port ranges

## Installation

```bash
pip install -r requirements.txt
```

Or for development:
```bash
pip install -e .
```

## Usage

Basic scan:
```bash
port-scanner target_host
```

Advanced scan with options:
```bash
port-scanner target_host -p 1-65535 -t 200 --timeout 0.5
```

Export to HTML report:
```bash
port-scanner target_host --html report.html
```

Export to PDF report:
```bash
port-scanner target_host --pdf report.pdf
```

## Development

### Linting
```bash
flake8 src/
```

### Type Checking
```bash
mypy src/
```

### Testing
```bash
pytest tests/
```

## Disclaimer

This tool is intended for authorized security testing and educational purposes only. Users must ensure they have explicit permission before scanning any networks or systems. Unauthorized scanning may violate laws and regulations.