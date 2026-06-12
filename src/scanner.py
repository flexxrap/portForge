import socket
import threading
import argparse
from typing import List, Tuple, Optional
import logging

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

    def _grab_banner(self, sock: socket.socket, port: int) -> str:
        """Attempt to grab service banner from an open port."""
        try:
            if port in [80, 8080]:
                sock.send(b"HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(self.target.encode()))
            else:
                sock.send(b"\r\n\r\n")
            banner = sock.recv(1024).decode().strip()
            return banner.split('\n')[0] if banner else 'Unknown'
        except Exception:
            return 'Unknown'

    def scan(self) -> List[Tuple[int, str]]:
        """Perform multi-threaded port scan."""
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

if __name__ == "__main__":
    main()