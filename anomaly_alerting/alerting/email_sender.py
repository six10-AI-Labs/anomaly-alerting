# alerting/email_sender.py
# Layer 5 — prompt for sender credentials and recipient emails at runtime, then send.

import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Tuple


def validate_email(email: str) -> bool:
    """Basic check that a string looks like an email address."""
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


def prompt_for_email_config() -> Tuple[str, str, List[str]]:
    """
    Prompt the person running the notebook for:
      - Their Gmail address (used as sender)
      - Their Gmail App Password (not their login password)
      - One or more recipient email addresses

    Returns:
        Tuple of (sender_email, app_password, list_of_recipients)

    How to get a Gmail App Password:
        1. Google Account → Security → 2-Step Verification (must be enabled)
        2. Search "App Passwords" → Create one → name it "Six10 Alerts"
        3. Copy the 16-character password shown
    """
    print("\n--- Email Setup ---")

    # Sender email
    while True:
        sender = input("Your Gmail address (will send FROM this): ").strip()
        if validate_email(sender):
            break
        print(f"  '{sender}' doesn't look like a valid email. Try again.")

    # App password
    while True:
        password = input("Your Gmail App Password (16 chars, spaces OK): ").strip()
        if len(password.replace(" ", "")) >= 16:
            break
        print("  App Password should be 16 characters. Try again.")

    # Recipients
    while True:
        raw = input("Recipient email(s) — separate multiple with commas: ").strip()
        recipients = [e.strip() for e in raw.split(",") if e.strip()]
        invalid = [e for e in recipients if not validate_email(e)]
        if recipients and not invalid:
            break
        if invalid:
            print(f"  Invalid address(es): {', '.join(invalid)}. Try again.")
        else:
            print("  Please enter at least one recipient email.")

    print(f"  Sending from: {sender}")
    print(f"  Sending to:   {', '.join(recipients)}")
    return sender, password, recipients


def send_email(recipients: List[str], subject: str, body: str,
               sender_email: str, sender_app_password: str,
               smtp_server: str, smtp_port: int,
               content_type: str = "plain") -> bool:
    """
    Send the alert digest email via Gmail SMTP (TLS).

    Args:
        recipients: List of recipient email addresses.
        subject: Email subject line.
        body: Email body (HTML or plain text).
        sender_email: Gmail address entered at runtime.
        sender_app_password: Gmail App Password entered at runtime.
        smtp_server: SMTP host (from config.py).
        smtp_port: SMTP port (from config.py).
        content_type: "html" or "plain".

    Returns:
        True if sent successfully, False on error.
    """
    try:
        msg = MIMEMultipart()
        msg["From"]    = sender_email
        msg["To"]      = ", ".join(recipients)
        msg["Subject"] = subject
        msg.attach(MIMEText(body, content_type))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_app_password)
            server.sendmail(sender_email, recipients, msg.as_string())

        return True

    except Exception as e:
        print(f"  Email send error: {e}")
        return False


def log_send_result(success: bool, recipients: List[str], run_date: str) -> None:
    """Log whether the email was sent or failed."""
    recipient_str = ", ".join(recipients)
    if success:
        print(f"  [OK]   Alert digest sent → {recipient_str}  ({run_date})")
    else:
        print(f"  [FAIL] Could not send alert digest → {recipient_str}  ({run_date})")
        print("         Check your Gmail address and App Password.")
