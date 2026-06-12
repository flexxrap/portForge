# Network Port Scanner

CLI tool for scanning network ports with multi-threading, service detection, and reporting capabilities.

## Features

- Multi-threaded port scanning for speed
- Service detection through banner grabbing
- Progress visualization with Rich
- Export reports to HTML and text formats
- Configurable timeout and thread count
- Support for custom port ranges

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Basic scan:
```bash
python src/scanner.py 192.168.1.1
```

Advanced scan with options:
```bash
python src/scanner.py 192.168.1.1 -p 1-65535 -t 200 --timeout 0.5
```

Export to HTML report:
```bash
python src/scanner.py 192.168.1.1 --html report.html
```

## Disclaimer

This tool is intended for authorized security testing and educational purposes only. Users must ensure they have explicit permission before scanning any networks or systems. Unauthorized scanning may violate laws and regulations.