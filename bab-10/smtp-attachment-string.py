import smtplib
import ssl
from email.message import EmailMessage

csv_content = "name,age\nAlice,30\nBob,25"

msg = EmailMessage()
msg["Subject"] = "Attachment from string"
msg["From"] = "you@example.com"
msg["To"] = "recipient@example.com"
msg.set_content("Attached CSV was created from a string.")

# Attach from string
msg.add_attachment(
    csv_content,
    maintype="text",
    subtype="csv",
    filename="report.csv"
)

# Send email
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
    server.login("you@example.com", "your_app_password")
    server.send_message(msg)
