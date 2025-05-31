import smtplib
import ssl
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Attachment from file path"
msg["From"] = "you@example.com"
msg["To"] = "recipient@example.com"
msg.set_content("Please find the attached file from path.")

# Attach file from path
with open("example.pdf", "rb") as f:
    msg.add_attachment(
        f.read(),
        maintype="application",
        subtype="pdf",
        filename="example.pdf"
    )

# Send email
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
    server.login("you@example.com", "your_app_password")
    server.send_message(msg)
