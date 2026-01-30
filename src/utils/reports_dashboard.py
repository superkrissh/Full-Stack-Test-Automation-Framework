"""Create a dashboard to view all test reports"""
from pathlib import Path
from datetime import datetime


class ReportsDashboard:
    """Generate a dashboard showing all available reports"""
    
    def __init__(self):
        self.report_dir = Path("reports/html")
        self.dashboard_path = Path("reports/dashboard.html")
    
    def generate_dashboard(self):
        """Generate dashboard HTML"""
        # Find all report files
        reports = sorted(self.report_dir.glob("test_report_*.html"), reverse=True)
        
        report_links = ""
        if reports:
            for report in reports:
                # Parse timestamp from filename
                timestamp = report.stem.replace("test_report_", "")
                formatted_time = self._format_timestamp(timestamp)
                
                report_links += f"""
                <tr>
                    <td style="padding: 12px;">
                        <a href="html/{report.name}" style="color: #2196F3; text-decoration: none; font-weight: bold;">
                            {formatted_time}
                        </a>
                    </td>
                    <td style="padding: 12px;">
                        <a href="html/{report.name}" style="background-color: #2196F3; color: white; padding: 8px 16px; border-radius: 4px; text-decoration: none;">
                            View Report →
                        </a>
                    </td>
                </tr>
                """
        else:
            report_links = """
            <tr>
                <td colspan="2" style="padding: 20px; text-align: center; color: #999;">
                    No reports generated yet. Run tests to generate reports.
                </td>
            </tr>
            """
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test Reports Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }}
        .subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 24px;
            font-weight: bold;
        }}
        .stat-label {{
            font-size: 12px;
            opacity: 0.8;
            margin-top: 5px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th {{
            background-color: #f5f5f5;
            padding: 12px;
            text-align: left;
            font-weight: 600;
            color: #333;
            border-bottom: 2px solid #ddd;
        }}
        tr {{
            border-bottom: 1px solid #eee;
        }}
        tr:hover {{
            background-color: #f9f9f9;
        }}
        .info {{
            background-color: #e3f2fd;
            border-left: 4px solid #2196F3;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
            font-size: 14px;
            color: #1565c0;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #999;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Test Reports Dashboard</h1>
        <div class="subtitle">View and track all test execution reports</div>
        
        <div class="info">
            ℹ️ Reports are automatically generated after each test run. Click on any report below to view detailed results.
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(reports)}</div>
                <div class="stat-label">Total Reports</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">Latest</div>
                <div class="stat-label">Always Available</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">HTML</div>
                <div class="stat-label">Report Format</div>
            </div>
        </div>
        
        <h2>Available Reports</h2>
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {report_links}
            </tbody>
        </table>
        
        <div class="footer">
            Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 
            Reports stored in: <code>reports/html/</code>
        </div>
    </div>
</body>
</html>
"""
        
        self.dashboard_path.write_text(html)
        print(f"✅ Dashboard generated: {self.dashboard_path}")
        return str(self.dashboard_path)
    
    def _format_timestamp(self, timestamp_str):
        """Format timestamp string to readable format"""
        try:
            dt = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
            return dt.strftime("%B %d, %Y at %H:%M:%S")
        except:
            return timestamp_str
