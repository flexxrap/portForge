import socket
import threading
import argparse
from typing import List, Tuple, Optional
import logging
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskID
from .reporting import ReportExporter

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
        """Perform multi-threaded port scan."""
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
                        t.join()
                    threads_list = []
            
            # Wait for remaining threads
            for thread in threads_list:
                thread.join()
        
        return self.open_ports

def main():
    parser = argparse.ArgumentParser(description="Network Port Scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", default="1-1000", help="Port range (e.g., 1-1000 or 80)")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout in seconds")
    parser.add_argument("--html", help="Export to HTML report")
    parser.add_argument("--pdf", help="Export to PDF report")
    parser.add_argument("--text", help="Export to text report")
    
    args = parser.parse_args()
    
    # Parse port range
    if '-' in args.ports:
        start, end = map(int, args.ports.split('-'))
    else:
        start = end = int(args.ports)
    
    scanner = PortScanner(args.target, (start, end), args.threads, args.timeout)
    logger.info(f"Scanning {args.target} ports {start}-{end} with {args.threads} threads")
    
    open_ports = scanner.scan()
    
    print("\nOpen Ports:")
    for port, service in open_ports:
        print(f"  {port}/tcp    {service}")
    
    # Export reports if requested
    if args.html:
        ReportExporter.export_to_html(args.target, open_ports, args.html)
    
    if args.pdf:
        ReportExporter.export_to_pdf(args.target, open_ports, args.pdf)
    
    if args.text:
        ReportExporter.export_to_text(args.target, open_ports, args.text)

if __name__ == "__main__":
    main()