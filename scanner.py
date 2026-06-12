"""Port scanner implementation with threading support."""

import socket
import threading
from typing import List, Tuple, Optional
from rich.progress import Progress, TaskID


class PortScanner:
    """Threaded port scanner with banner grabbing capability."""

    def __init__(self, timeout: float = 1.0, threads: int = 100):
        self.timeout = timeout
        self.threads = threads
        self.open_ports: List[Tuple[str, int, Optional[str]]] = []

    def scan_port(self, ip: str, port: int, progress: Optional[Progress] = None, 
                  task_id: Optional[TaskID] = None) -> None:
        """Scan a single port and grab banner if open."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    banner = self._grab_banner(ip, port)
                    self.open_ports.append((ip, port, banner))
        except Exception:
            pass
        finally:
            if progress and task_id:
                progress.update(task_id, advance=1)

    def _grab_banner(self, ip: str, port: int) -> Optional[str]:
        """Grab service banner from open port."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                sock.connect((ip, port))
                sock.send(b'HEAD / HTTP/1.0\r\n\r\n')
                return sock.recv(1024).decode('utf-8', errors='ignore').strip()
        except Exception:
            return None

    def scan(self, ip: str, ports: List[int]) -> List[Tuple[str, int, Optional[str]]]:
        """Scan multiple ports on target IP with progress bar."""
        self.open_ports = []
        threads_list = []
        
        with Progress() as progress:
            task_id = progress.add_task(f"[green]Scanning {ip}...", total=len(ports))
            
            for port in ports:
                while len(threads_list) >= self.threads:
                    for t in threads_list[:]:
                        if not t.is_alive():
                            t.join()
                            threads_list.remove(t)
                    threading.Event().wait(0.01)
                    
                thread = threading.Thread(
                    target=self.scan_port, 
                    args=(ip, port, progress, task_id)
                )
                thread.start()
                threads_list.append(thread)
            
            for thread in threads_list:
                thread.join()
                
        return self.open_ports