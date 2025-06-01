import smtplib
import base64
from getpass import getpass

# Prompting for credentials and recipient
from_addr = input("From: ").strip()
to_addr = input("To: ").strip()
password = getpass("Password: ")

# Read and encode the file
filename = "example.pdf"
with open(filename, "rb") as f:
    file_data = f.read()
    encoded_file = base64.b64encode(file_data).decode()

# Construct MIME message manually
boundary = "BOUNDARY123"

msg = f"""From: {from_addr}
To: {to_addr}
Subject: Manual MIME Email with Attachment
MIME-Version: 1.0
Content-Type: multipart/mixed; boundary={boundary}

--{boundary}
Content-Type: text/plain

This is the email body text.

--{boundary}
Content-Type: application/pdf; name="{filename}"
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename="{filename}"

{encoded_file}
--{boundary}--
"""

# Connect and send
server = smtplib.SMTP("smtp.office365.com", 587)
server.starttls()
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg)
server.quit()
