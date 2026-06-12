# Port Scanner API Documentation

## Classes

### PortScanner

Main class for performing port scans.

#### Constructor
```python
PortScanner(target: str, port_range: Tuple[int, int], threads: int = 100, timeout: float = 1.0)
```

Parameters:
- `target` (str): Target IP address or hostname
- `port_range` (Tuple[int, int]): Range of ports to scan (start, end)
- `threads` (int): Number of threads to use for scanning (default: 100)
- `timeout` (float): Connection timeout in seconds (default: 1.0)

#### Methods

##### scan()
```python
scan() -> List[Tuple[int, str]]
```
Perform multi-threaded port scan.

Returns:
- List of tuples containing (port_number, service_name) for open ports

##### scan_port(port)
```python
scan_port(port: int) -> None
```
Scan a single port and perform banner grabbing if open.

Parameters:
- `port` (int): Port number to scan

##### print_colored_results()
```python
print_colored_results() -> None
```
Print scan results with colored output using Rich.

##### save_results(filename)
```python
save_results(filename: str) -> None
```
Save scan results to a JSON file.

Parameters:
- `filename` (str): Path to save the results file

##### load_results(filename)
```python
load_results(filename: str) -> None
```
Load scan results from a JSON file.

Parameters:
- `filename` (str): Path to the results file to load

### ReportExporter

Class for exporting scan results to various formats.

#### Methods

##### export_to_html()
```python
export_to_html(target: str, open_ports: List[Tuple[int, str]], filename: str = "scan_report.html") -> str
```
Export scan results to HTML report.

Parameters:
- `target` (str): Target host that was scanned
- `open_ports` (List[Tuple[int, str]]): List of open ports and services
- `filename` (str): Output filename (default: "scan_report.html")

Returns:
- HTML content as string

##### export_to_pdf()
```python
export_to_pdf(target: str, open_ports: List[Tuple[int, str]], filename: str = "scan_report.pdf") -> None
```
Export scan results to PDF report.

Parameters:
- `target` (str): Target host that was scanned
- `open_ports` (List[Tuple[int, str]]): List of open ports and services
- `filename` (str): Output filename (default: "scan_report.pdf")

##### export_to_text()
```python
export_to_text(target: str, open_ports: List[Tuple[int, str]], filename: str = "scan_report.txt") -> None
```
Export scan results to text report.

Parameters:
- `target` (str): Target host that was scanned
- `open_ports` (List[Tuple[int, str]]): List of open ports and services
- `filename` (str): Output filename (default: "scan_report.txt")

## Command Line Interface

The port scanner can be used from the command line:

```bash
port-scanner target_host [-p PORTS] [-t THREADS] [--timeout TIMEOUT] [--html HTML] [--pdf PDF] [--text TEXT] [--save SAVE] [--load LOAD] [--no-color]
```

### Arguments

- `target_host`: Target IP address or hostname
- `-p, --ports`: Port range (e.g., 1-1000 or 80) (default: 1-1000)
- `-t, --threads`: Number of threads (default: 100)
- `--timeout`: Connection timeout in seconds (default: 1.0)
- `--html`: Export to HTML report
- `--pdf`: Export to PDF report
- `--text`: Export to text report
- `--save`: Save results to JSON file
- `--load`: Load results from JSON file
- `--no-color`: Disable colored output