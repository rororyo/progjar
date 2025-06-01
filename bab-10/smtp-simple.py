# Purpose: The most basic example.

# What it does: Sends an email using the standard smtplib.SMTP() connection.

# No authentication, no encryption.
# 🔧 Common Elements Across All Scripts:
# Message Template: All messages follow a similar format (To, From, Subject, Body).

# Command Line Arguments: All expect this structure:

# bash
# Copy
# Edit
# python3 script.py smtp.server.com from@example.com to@example.com

import sys, smtplib

message_template = """To: {}
From: {}
Subject: Test Message from simple.py

Hello,

This is a test message sent to you from the simple.py program
in Foundations of Python Network Programming.
"""

def main():
    if len(sys.argv) < 4:
        name = sys.argv[0]
        print("usage: {} server fromaddr toaddr [toaddr...]".format(name))
        sys.exit(2)

    server, fromaddr, toaddrs = sys.argv[1], sys.argv[2], sys.argv[3:]
    message = message_template.format(', '.join(toaddrs), fromaddr)

    connection = smtplib.SMTP(server)
    connection.sendmail(fromaddr, toaddrs, message)
    connection.quit()

    s = '' if len(toaddrs) == 1 else 's'
    print("Message sent to {} recipient{}".format(len(toaddrs), s))

if __name__ == '__main__':
    main()