import smtplib
import ssl
from email.message import EmailMessage

# Example in-memory PDF bytes
pdf_bytes = b"%PDF-1.4\n%Dummy PDF content\n..."

msg = EmailMessage()
msg["Subject"] = "Attachment from memory bytes"
msg["From"] = "you@example.com"
msg["To"] = "recipient@example.com"
msg.set_content("Attached file was generated in memory.")

# Attach from memory bytes
msg.add_attachment(
    pdf_bytes,
    maintype="application",
    subtype="pdf",
    filename="in_memory.pdf"
)

# Send email
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
    server.login("you@example.com", "your_app_password")
    server.send_message(msg)
