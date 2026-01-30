"""Generate beautiful HTML test reports"""
from datetime import datetime
from pathlib import Path


class TestReporter:
    """Generate HTML reports showing test results"""
    
    def __init__(self):
        self.report_dir = Path("reports/html")
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_report(self, test_results):
        """
        Generate HTML report from test results
        
        Args:
            test_results: List of test result dicts
                {
                    'name': 'test_name',
                    'status': 'PASSED' or 'FAILED',
                    'duration': 1.5,
                    'error': 'error message if failed'
                }
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_report_{timestamp}.html"
        filepath = self.report_dir / filename
        
        # Calculate stats
        total = len(test_results)
        passed = sum(1 for t in test_results if t['status'] == 'PASSED')
        failed = sum(1 for t in test_results if t['status'] == 'FAILED')
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        # Generate HTML
        html = self._generate_html(test_results, passed, failed, pass_rate, total)
        
        # Write file
        filepath.write_text(html)
        print(f"\n✅ Report generated: {filepath}")
        return str(filepath)
    
    def _generate_html(self, tests, passed, failed, pass_rate, total):
        """Generate HTML content"""
        
        test_rows = ""
        for test in tests:
            status_color = "green" if test['status'] == 'PASSED' else "red"
            status_icon = "✅" if test['status'] == 'PASSED' else "❌"
            
            error_row = ""
            if test.get('error'):
                error_row = f"""
                <tr style="background-color: #fff0f0;">
                    <td colspan="4" style="padding: 10px; color: red; font-size: 12px;">
                        <strong>Error:</strong> {test['error'][:200]}
                    </td>
                </tr>
                """
            
            test_rows += f"""
            <tr style="border-bottom: 1px solid #e0e0e0;">
                <td style="padding: 10px; color: {status_color}; font-weight: bold;">{status_icon} {test['status']}</td>
                <td style="padding: 10px;">{test['name']}</td>
                <td style="padding: 10px;">{test.get('duration', 0):.2f}s</td>
            </tr>
            {error_row}
            """
        
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-box {{
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }}
        .stat-total {{
            background-color: #e3f2fd;
            border-left: 4px solid #2196F3;
        }}
        .stat-passed {{
            background-color: #e8f5e9;
            border-left: 4px solid #4CAF50;
        }}
        .stat-failed {{
            background-color: #ffebee;
            border-left: 4px solid #f44336;
        }}
        .stat-rate {{
            background-color: #fff3e0;
            border-left: 4px solid #FF9800;
        }}
        .stat-number {{
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-label {{
            font-size: 14px;
            color: #666;
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
            font-weight: bold;
            border-bottom: 2px solid #ddd;
        }}
        td {{
            padding: 10px;
        }}
        .progress {{
            width: 100%;
            height: 30px;
            background-color: #e0e0e0;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}
        .progress-bar {{
            height: 100%;
            background: linear-gradient(90deg, #4CAF50, #45a049);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 14px;
        }}
        .timestamp {{
            color: #999;
            font-size: 12px;
            margin-top: 20px;
            text-align: right;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Test Report</h1>
        
        <div class="stats">
            <div class="stat-box stat-total">
                <div class="stat-label">Total Tests</div>
                <div class="stat-number">{total}</div>
            </div>
            <div class="stat-box stat-passed">
                <div class="stat-label">Passed</div>
                <div class="stat-number">{passed}</div>
            </div>
            <div class="stat-box stat-failed">
                <div class="stat-label">Failed</div>
                <div class="stat-number">{failed}</div>
            </div>
            <div class="stat-box stat-rate">
                <div class="stat-label">Pass Rate</div>
                <div class="stat-number">{pass_rate:.1f}%</div>
            </div>
        </div>
        
        <div class="progress">
            <div class="progress-bar" style="width: {pass_rate}%">
                {pass_rate:.1f}%
            </div>
        </div>
        
        <h2>Test Results</h2>
        <table>
            <thead>
                <tr>
                    <th>Status</th>
                    <th>Test Name</th>
                    <th>Duration</th>
                </tr>
            </thead>
            <tbody>
                {test_rows}
            </tbody>
        </table>
        
        <div class="timestamp">
            Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        </div>
    </div>
</body>
</html>
"""
        return html_content
