import smtplib
import ssl
from email.message import EmailMessage
import mimetypes

def send_email_with_attachment(
    smtp_server,
    port,
    sender_email,
    sender_password,
    recipient_email,
    subject,
    body,
    attachment_path
):
    # Create the email message
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.set_content(body)

    # Determine MIME type and add attachment
    mime_type, _ = mimetypes.guess_type(attachment_path)
    mime_type = mime_type or "application/octet-stream"
    maintype, subtype = mime_type.split("/")

    with open(attachment_path, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype=maintype,
            subtype=subtype,
            filename=attachment_path.split("/")[-1]
        )

    # Connect and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)
        print("Email sent successfully!")

# Example usage:
send_email_with_attachment(
    smtp_server="smtp.gmail.com",
    port=465,
    sender_email="your_email@gmail.com",
    sender_password="your_app_password",
    recipient_email="recipient@example.com",
    subject="Test Email with Attachment",
    body="Please see the attached file.",
    attachment_path="path/to/your/file.pdf"
)
