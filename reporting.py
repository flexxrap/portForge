"""Reporting module for port scanner."""

import os
from typing import List, Tuple, Optional
from datetime import datetime
import pdfkit


class ReportGenerator:
    """Generate scan reports in various formats."""

    def __init__(self, template_dir: str = "templates"):
        self.template_dir = template_dir

    def export_html(self, target: str, results: List[Tuple[str, int, Optional[str]]], 
                   output_file: str) -> None:
        """Export scan results to HTML report."""
        # Simple template rendering without external dependencies
        html_template = self._load_template("report.html")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Replace template variables
        html_content = html_template.replace("{{target}}", target)
        html_content = html_content.replace("{{timestamp}}", timestamp)
        
        # Generate table rows
        if results:
            rows = ""
            for _, port, banner in results:
                rows += f"<tr><td>{port}</td><td class='banner'>{banner or 'No banner'}</td></tr>\n"
            # Replace the loop section with generated rows
            html_content = html_content.replace(
                "{% for _, port, banner in results %}\n            <tr>\n                <td>{{port}}</td>\n                <td class='banner'>{% if banner %}{{banner}}{% else %}No banner{% endif %}</td>\n            </tr>\n            {% endfor %}",
                rows.rstrip()
            )
        else:
            html_content = html_content.replace(
                "{% if results %}\n    <table>\n        <thead>\n            <tr>\n                <th>Port</th>\n                <th>Banner</th>\n            </tr>\n        </thead>\n        <tbody>\n            {% for _, port, banner in results %}\n            <tr>\n                <td>{{port}}</td>\n                <td class='banner'>{% if banner %}{{banner}}{% else %}No banner{% endif %}</td>\n            </tr>\n            {% endfor %}\n        </tbody>\n    </table>\n    {% else %}\n    <p>No open ports found.</p>\n    {% endif %}",
                "<p>No open ports found.</p>"
            )
        
        with open(output_file, "w") as f:
            f.write(html_content)

    def export_pdf(self, target: str, results: List[Tuple[str, int, Optional[str]]], 
                  output_file: str) -> None:
        """Export scan results to PDF report."""
        # Generate HTML first
        temp_html = f"/tmp/report_{target.replace('.', '_')}.html"
        self.export_html(target, results, temp_html)
        
        # Convert to PDF using pdfkit
        try:
            pdfkit.from_file(temp_html, output_file)
        finally:
            # Clean up temporary file
            if os.path.exists(temp_html):
                os.remove(temp_html)

    def _load_template(self, template_name: str) -> str:
        """Load HTML template from file."""
        template_path = os.path.join(self.template_dir, template_name)
        with open(template_path, "r") as f:
            return f.read()