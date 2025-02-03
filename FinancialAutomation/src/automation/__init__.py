# src/automation/__init__.py
from .report_generator import ReportGenerator

# src/automation/report_generator.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any
import json
from datetime import datetime

class ReportGenerator:
    def __init__(self, data: pd.DataFrame, analysis_results: Dict[str, Any]):
        self.data = data
        self.analysis_results = analysis_results
        self.report_date = datetime.now().strftime('%Y-%m-%d')
        
    def generate_report(self, output_path: str):
        """Generate comprehensive financial report with visualizations."""
        # Create visualizations
        self._create_visualizations()
        
        # Generate report content
        report_content = self._generate_report_content()
        
        # Save report
        self._save_report(report_content, output_path)
    
    def _create_visualizations(self):
        """Create financial visualizations."""
        # Revenue and Profit Trends
        plt.figure(figsize=(12, 6))
        monthly_data = self.data.set_index('date').resample('M').sum()
        plt.plot(monthly_data.index, monthly_data['revenue'], label='Revenue')
        plt.plot(monthly_data.index, monthly_data['profit'], label='Profit')
        plt.title('Monthly Revenue and Profit Trends')
        plt.xlabel('Date')
        plt.ylabel('Amount ($)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('reports/trends.png')
        plt.close()
        
        # Category Performance
        plt.figure(figsize=(10, 6))
        category_data = self.data.groupby('category')['profit'].sum()
        sns.barplot(x=category_data.index, y=category_data.values)
        plt.title('Profit by Category')
        plt.xlabel('Category')
        plt.ylabel('Total Profit ($)')
        plt.tight_layout()
        plt.savefig('reports/category_performance.png')
        plt.close()
    
    def _generate_report_content(self) -> str:
        """Generate the report content in Markdown format."""
        summary_metrics = self.analysis_results['summary_metrics']
        
        report = f"""# Financial Analysis Report
Generated on: {self.report_date}

## Summary Metrics
- Total Revenue: ${summary_metrics['total_revenue']:,.2f}
- Total Profit: ${summary_metrics['total_profit']:,.2f}
- Average Profit Margin: {summary_metrics['average_profit_margin']:.2f}%
- Revenue Growth: {summary_metrics['revenue_growth']}%

## Trend Analysis
- Revenue Trend: {self.analysis_results['trend_analysis']['revenue_trend']}
- Profit Trend: {self.analysis_results['trend_analysis']['profit_trend']}

## Category Performance
"""
        
        # Add category performance details
        for category, metrics in self.analysis_results['category_analysis'].items():
            report += f"\n### {category}\n"
            report += f"- Revenue: ${metrics['revenue']:,.2f}\n"
            report += f"- Profit: ${metrics['profit']:,.2f}\n"
            report += f"- Average Profit Margin: {metrics['profit_margin']:.2f}%\n"
        
        return report
    
    def _save_report(self, content: str, output_path: str):
        """Save the report to file."""
        with open(output_path, 'w') as f:
            f.write(content)

# src/automation/email_automation.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

class EmailAutomation:
    def __init__(self, smtp_server: str, smtp_port: int):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_report(self, sender: str, recipient: str, subject: str, 
                   report_path: str, password: str):
        """Send financial report via email."""
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient
        msg['Subject'] = subject
        
        # Add body
        body = "Please find attached the latest financial analysis report."
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach report
        with open(report_path, 'rb') as f:
            report_attachment = MIMEApplication(f.read(), _subtype='txt')
            report_attachment.add_header('Content-Disposition', 'attachment', 
                                      filename=os.path.basename(report_path))
            msg.attach(report_attachment)
        
        # Send email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(sender, password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False