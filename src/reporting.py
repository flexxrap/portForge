import argparse
from typing import List, Tuple
import webbrowser
import os
from datetime import datetime
from weasyprint import HTML

class ReportExporter:
    @staticmethod
    def export_to_html(target: str, open_ports: List[Tuple[int, str]], filename: str = "scan_report.html") -> None:
        """Export scan results to HTML report."""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Port Scan Report - {target}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
        h1 {{ color: #333; }}
        .timestamp {{ color: #666; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>Port Scan Report</h1>
    <p class="timestamp">Scan performed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Target:</strong> {target}</p>
    
    <table>
        <tr>
            <th>Port</th>
            <th>Service</th>
        </tr>
"""
        
        for port, service in open_ports:
            html_content += f"        <tr>\n            <td>{port}/tcp</td>\n            <td>{service}</td>\n        </tr>\n"
        
        html_content += """
    </table>
</body>
</html>
"""
        
        with open(filename, 'w') as f:
            f.write(html_content)
        
        print(f"HTML report saved to {filename}")
        return html_content
    
    @staticmethod
    def export_to_pdf(target: str, open_ports: List[Tuple[int, str]], filename: str = "scan_report.pdf") -> None:
        """Export scan results to PDF report."""
        html_content = ReportExporter.export_to_html(target, open_ports, "temp_report.html")
        HTML(string=html_content).write_pdf(filename)
        os.remove("temp_report.html")  # Clean up temporary file
        print(f"PDF report saved to {filename}")
        
    @staticmethod
    def export_to_text(target: str, open_ports: List[Tuple[int, str]], filename: str = "scan_report.txt") -> None:
        """Export scan results to text report."""
        with open(filename, 'w') as f:
            f.write(f"Port Scan Report for {target}\n")
            f.write(f"Scan performed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 50 + "\n\n")
            
            f.write("Open Ports:\n")
            for port, service in open_ports:
                f.write(f"  {port}/tcp    {service}\n")
        
        print(f"Text report saved to {filename}")