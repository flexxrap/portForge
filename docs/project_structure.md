# Network Port Scanner

This directory contains all the source code for the port scanner tool.

## Project Structure

- `src/` - Main source code
  - `scanner.py` - Core scanning logic with multi-threading
  - `reporting.py` - Report generation in various formats
- `tests/` - Unit tests
- `docs/` - Documentation
- `requirements.txt` - Python dependencies
- `setup.py` - Package setup
- `setup.cfg` - Configuration for linting and testing
- `README.md` - Project documentation

## Features Implemented

1. Multi-threaded port scanning
2. Service detection via banner grabbing
3. Progress visualization with Rich
4. Export to HTML, PDF, and text reports
5. CLI interface with argparse
6. Package installation support

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

## Disclaimer

This tool is intended for authorized security testing and educational purposes only. Users must ensure they have explicit permission before scanning any networks or systems. Unauthorized scanning may violate laws and regulations.