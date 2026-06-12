"""Main entry point for port scanner CLI."""

import argparse
import sys
import os
from typing import List
from .scanner import PortScanner
from .reporting import ReportGenerator


def parse_ports(port_arg: str) -> List[int]:
    """Parse port range string into list of integers."""
    ports = []
    for part in port_arg.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))
    return ports


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Network Port Scanner')
    parser.add_argument('target', help='Target IP address')
    parser.add_argument('-p', '--ports', default='1-1000',
                        help='Port range (e.g. 1-1000 or 22,80,443)')
    parser.add_argument('-t', '--timeout', type=float, default=1.0,
                        help='Connection timeout in seconds')
    parser.add_argument('-T', '--threads', type=int, default=100,
                        help='Number of threads')
    parser.add_argument('--html', help='Export report to HTML file')
    parser.add_argument('--pdf', help='Export report to PDF file')
    
    args = parser.parse_args()
    
    try:
        ports = parse_ports(args.ports)
        scanner = PortScanner(timeout=args.timeout, threads=args.threads)
        results = scanner.scan(args.target, ports)
        
        if results:
            print(f"\nOpen ports on {args.target}:")
            for ip, port, banner in results:
                if banner:
                    print(f"  {port}: {banner.split()[0] if banner.split() else 'Unknown'}")
                else:
                    print(f"  {port}: Unknown")
        else:
            print(f"No open ports found on {args.target}")
            
        # Export reports if requested
        if args.html or args.pdf:
            # Change to script directory to resolve templates path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            template_dir = os.path.join(script_dir, "templates")
            reporter = ReportGenerator(template_dir)
            
            if args.html:
                reporter.export_html(args.target, results, args.html)
                print(f"\nHTML report saved to {args.html}")
                
            if args.pdf:
                try:
                    reporter.export_pdf(args.target, results, args.pdf)
                    print(f"PDF report saved to {args.pdf}")
                except Exception as e:
                    print(f"Failed to generate PDF report: {e}")
            
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()