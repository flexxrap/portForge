# Port Scanner Project

This directory contains all the source code for the port scanner tool.

## Project Structure

- `src/` - Main source code
  - `scanner.py` - Core scanning logic with multi-threading
  - `reporting.py` - Report generation in various formats
- `requirements.txt` - Python dependencies
- `README.md` - Project documentation

## Features Implemented

1. Multi-threaded port scanning
2. Service detection via banner grabbing
3. Progress visualization with Rich
4. Export to HTML and text reports
5. CLI interface with argparse

## Planned Features

1. PDF report generation
2. Enhanced service detection
3. Improved error handling
4. Unit tests