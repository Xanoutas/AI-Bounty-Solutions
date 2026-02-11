import psutil
import logging
from logging.handlers import RotatingFileHandler
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import os

# Configure logging
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')
log_file = 'server_health.log'

handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
handler.setFormatter(log_formatter)

logger = logging.getLogger('server_health_monitor')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Function to send alert email
def send_alert(subject, body):
    sender = 'your_email@example.com'
    recipient = 'admin@example.com'
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_user = 'your_email@example.com'
    smtp_password = 'your_email_password'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender, recipient, msg.as_string())
        logger.info('Alert email sent successfully')
    except Exception as e:
        logger.error(f'Failed to send alert email: {e}')

# Function to check server health
def check_health():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_usage = psutil.virtual_memory().percent

    logger.info(f'CPU Usage: {cpu_usage}%, RAM Usage: {ram_usage}%')

    if cpu_usage > 90:
        logger.warning(f'High CPU usage detected: {cpu_usage}%')
        send_alert('High CPU Usage Alert', f'CPU usage is {cpu_usage}% as of {datetime.now().isoformat()}')

    if ram_usage > 90:
        logger.warning(f'High RAM usage detected: {ram_usage}%')
        send_alert('High RAM Usage Alert', f'RAM usage is {ram_usage}% as of {datetime.now().isoformat()}')

if __name__ == '__main__':
    check_health()


Ensure to replace `'your_email@example.com'`, `'admin@example.com'`, `'smtp.example.com'`, `'smtp_port'`, `'your_email_password'`, and other placeholders with your actual configuration details.