import socket
import threading
import argparse
from typing import List, Tuple, Optional, Dict, Any
import logging
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from .reporting import ReportExporter
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PortScanner:
    def __init__(self, target: str, port_range: Tuple[int, int], threads: int = 100, timeout: float = 1.0):
        self.target = target
        self.start_port, self.end_port = port_range
        self.threads = threads
        self.timeout = timeout
        self.open_ports: List[Tuple[int, str]] = []
        self.progress: Optional[Progress] = None
        self.task_id: Optional[TaskID] = None
        self.scan_results: Dict[str, Any] = {
            'target': target,
            'port_range': port_range,
            'threads': threads,
            'timeout': timeout,
            'open_ports': [],
            'scan_duration': 0
        }
        self.console = Console()

    def scan_port(self, port: int) -> None:
        """Scan a single port and perform banner grabbing if open."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    service = self._grab_banner(sock, port)
                    self.open_ports.append((port, service))
                    logger.info(f"Port {port} is open ({service})")
        except socket.gaierror:
            logger.error(f"Hostname {self.target} could not be resolved")
            raise
        except socket.error:
            logger.error(f"Couldn't connect to server {self.target}")
            raise
        except Exception as e:
            logger.debug(f"Error scanning port {port}: {e}")
        finally:
            # Update progress bar
            if self.progress and self.task_id:
                self.progress.update(self.task_id, advance=1)

    def _grab_banner(self, sock: socket.socket, port: int) -> str:
        """Attempt to grab service banner from an open port."""
        try:
            # Send appropriate handshake for different services
            if port in [80, 8080, 8000]:
                sock.send(b"HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(self.target.encode()))
            elif port in [21]:
                # FTP - wait for banner
                pass
            elif port in [22]:
                # SSH - wait for banner
                pass
            elif port in [25, 465, 587]:
                # SMTP - send EHLO
                sock.send(b"EHLO scanner\r\n")
            elif port in [110, 995]:
                # POP3 - wait for banner
                pass
            elif port in [143, 993]:
                # IMAP - send CAPABILITY
                sock.send(b"CAPABILITY\r\n")
            else:
                sock.send(b"\r\n\r\n")
            
            banner = sock.recv(1024).decode(errors='ignore').strip()
            # Clean up the banner for better readability
            if '\n' in banner:
                banner = banner.split('\n')[0]
            if '\r' in banner:
                banner = banner.split('\r')[0]
                
            # If we get an empty banner, try to identify service by port
            if not banner:
                service_map = {
                    21: 'FTP',
                    22: 'SSH',
                    23: 'Telnet',
                    25: 'SMTP',
                    53: 'DNS',
                    80: 'HTTP',
                    110: 'POP3',
                    143: 'IMAP',
                    443: 'HTTPS',
                    465: 'SMTPS',
                    587: 'SMTP',
                    993: 'IMAPS',
                    995: 'POP3S',
                    3306: 'MySQL',
                    5432: 'PostgreSQL',
                    6379: 'Redis',
                    27017: 'MongoDB'
                }
                return service_map.get(port, 'Unknown')
                
            return banner if banner else 'Unknown'
        except Exception:
            # Fallback service identification by port number
            service_map = {
                21: 'FTP',
                22: 'SSH',
                23: 'Telnet',
                25: 'SMTP',
                53: 'DNS',
                80: 'HTTP',
                110: 'POP3',
                143: 'IMAP',
                443: 'HTTPS',
                465: 'SMTPS',
                587: 'SMTP',
                993: 'IMAPS',
                995: 'POP3S',
                3306: 'MySQL',
                5432: 'PostgreSQL',
                6379: 'Redis',
                27017: 'MongoDB'
            }
            return service_map.get(port, 'Unknown')

    def scan(self) -> List[Tuple[int, str]]:
        """Perform multi-threaded port scan with error handling."""
        import time
        start_time = time.time()
        
        try:
            # Initialize progress bar
            self.progress = Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            )
            
            with self.progress:
                total_ports = self.end_port - self.start_port + 1
                self.task_id = self.progress.add_task(
                    f"[cyan]Scanning {self.target}...", 
                    total=total_ports
                )
                
                threads_list = []
                for port in range(self.start_port, self.end_port + 1):
                    thread = threading.Thread(target=self.scan_port, args=(port,))
                    threads_list.append(thread)
                    thread.start()
                    
                    # Control thread count
                    if len(threads_list) >= self.threads:
                        for t in threads_list:
                            t.join(timeout=5)  # Add timeout for stuck threads
                        threads_list = []
                
                # Wait for remaining threads with timeout
                for thread in threads_list:
                    thread.join(timeout=5)
            
            # Update scan results
            self.scan_results['open_ports'] = self.open_ports
            self.scan_results['scan_duration'] = time.time() - start_time
            
            return self.open_ports
            
        except KeyboardInterrupt:
            logger.info("Scan interrupted by user")
            raise
        except Exception as e:
            logger.error(f"Scan failed: {e}")
            raise

    def print_colored_results(self) -> None:
        """Print scan results with colored output using Rich."""
        table = Table(title=f"Port Scan Results for {self.scan_results['target']}")
        table.add_column("Port", style="cyan", no_wrap=True)
        table.add_column("Service", style="magenta")
        table.add_column("Status", style="green")
        
        for port, service in self.open_ports:
            table.add_row(str(port), service, "Open")
        
        self.console.print(table)
        self.console.print(f"[bold green]Scan completed in {self.scan_results['scan_duration']:.2f} seconds[/bold green]")
        self.console.print(f"[bold blue]Found {len(self.open_ports)} open ports[/bold blue]")

    def save_results(self, filename: str) -> None:
        """Save scan results to a JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.scan_results, f, indent=2)
        logger.info(f"Results saved to {filename}")

    def load_results(self, filename: str) -> None:
        """Load scan results from a JSON file."""
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Results file {filename} not found")
            
        with open(filename, 'r') as f:
            self.scan_results = json.load(f)
        self.open_ports = [tuple(port) for port in self.scan_results['open_ports']]
        logger.info(f"Results loaded from {filename}")

def main():
    parser = argparse.ArgumentParser(description="Network Port Scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", default="1-1000", help="Port range (e.g., 1-1000 or 80)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout in seconds")
    parser.add_argument("--html", help="Export to HTML report")
    parser.add_argument("--pdf", help="Export to PDF report")
    parser.add_argument("--text", help="Export to text report")
    parser.add_argument("--save", help="Save results to JSON file")
    parser.add_argument("--load", help="Load results from JSON file")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")
    
    args = parser.parse_args()
    
    # Handle loading results
    if args.load:
        scanner = PortScanner("", (0, 0))  # Dummy scanner for loading
        try:
            scanner.load_results(args.load)
            open_ports = scanner.open_ports
            target = scanner.scan_results['target']
        except FileNotFoundError as e:
            logger.error(e)
            return
    else:
        # Parse port range
        if '-' in args.ports:
            start, end = map(int, args.ports.split('-'))
        else:
            start = end = int(args.ports)
        
        scanner = PortScanner(args.target, (start, end), args.threads, args.timeout)
        target = args.target
        
        try:
            logger.info(f"Scanning {target} ports {start}-{end} with {args.threads} threads")
            open_ports = scanner.scan()
        except (socket.gaierror, socket.error) as e:
            logger.error(f"Scan failed: {e}")
            return
        except KeyboardInterrupt:
            logger.info("Scan interrupted by user")
            return
    
    # Print results
    if not args.no_color:
        scanner.print_colored_results()
    else:
        print(f"\nScan Results for {target}:")
        print(f"Open Ports ({len(open_ports)} found):")
        for port, service in open_ports:
            print(f"  {port}/tcp    {service}")
    
    # Save results if requested
    if args.save:
        scanner.save_results(args.save)
    
    # Export reports if requested
    if args.html:
        ReportExporter.export_to_html(target, open_ports, args.html)
    
    if args.pdf:
        ReportExporter.export_to_pdf(target, open_ports, args.pdf)
    
    if args.text:
        ReportExporter.export_to_text(target, open_ports, args.text)

if __name__ == "__main__":
    main()