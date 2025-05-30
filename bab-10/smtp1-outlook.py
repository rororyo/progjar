import smtplib

def prompt(prompt):
  return input(prompt).strip()

from_addr = prompt("From: ")
to_addr = prompt("To:").split()
print("Enter message, end with ^D (Unix) or ^Z (Windows):")

msg = ("From: %s\r\nTo: %s\r\n\r\n"
       % (from_addr, ", ".join(to_addr)))

while True:
  try:
    line = input()
  except EOFError:
    break
  if not line:
    break
  msg = msg+line

print("Message length is", len(msg))

server = smtplib.SMTP('smtp.office365.com', 587)
server.set_debuglevel(1)
server.starttls()
server.login('hudan@its.ac.id', 'xxx')
server.sendmail(from_addr=from_addr, to_addrs=to_addr, msg=msg)
server.quit()

# | Email Provider | SMTP Server         | Port | TLS/SSL  |
# | -------------- | ------------------- | ---- | -------- |
# | Gmail          | smtp.gmail.com      | 587  | STARTTLS |
# | Outlook/365    | smtp.office365.com  | 587  | STARTTLS |
# | Yahoo Mail     | smtp.mail.yahoo.com | 587  | STARTTLS |
# | iCloud Mail    | smtp.mail.me.com    | 587  | STARTTLS |
