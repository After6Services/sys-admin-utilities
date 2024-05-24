# Description: This script connects to an IMAP email account, deletes all emails from senders matching an email address pattern, and expunges the deleted emails.

import imaplib
import sys
import email
import re

# Read parameters from the command line
# IMAP server details
IMAP_SERVER = sys.argv[1]
IMAP_PORT = int(sys.argv[2])

# Email account credentials
EMAIL_ADDRESS = sys.argv[3]
PASSWORD = sys.argv[4]

# From email address to delete
FROM_EMAIL = sys.argv[5]

# Age of emails to delete (in days)
AGE = int(sys.argv[6])

# Calculate date threshold
from datetime import datetime, timedelta
date_threshold = datetime.now() - timedelta(days=AGE)

# Connect to the IMAP server
imap_server = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

# Login to the email account
imap_server.login(EMAIL_ADDRESS, PASSWORD)

# Select the mailbox (e.g., 'INBOX')
mailbox = 'INBOX'
imap_server.select(mailbox)

# Get all email IDs for emails from senders matching an email address pattern in FROM_EMAIL.
result, data = imap_server.uid('search', None, f'(FROM "{FROM_EMAIL}")')
mail_ids = data[0].split()

# Delete all emails from the senders matching the email address pattern
for id in mail_ids:

    # If the date of this email is older than AGE days, delete it
    result, data = imap_server.uid('fetch', id, '(RFC822)')
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)
    date_str = email_message['Date']
    date = email.utils.parsedate(date_str)
    if date is None:
        print(f"Could not parse date: {date_str}")
        continue
    if (date[0], date[1], date[2]) > (date_threshold.year, date_threshold.month, date_threshold.day):
        print(f"Skipping email with date: {date_str}")
    else:
        try:
            imap_server.uid('store', id, '+FLAGS', '\\Deleted')
        except imaplib.IMAP4.error as e:
            print(f"IMAP error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
            
        print(f"Deleting email: {email_message.get('Subject')} with date: {date_str}")

# Expunge the deleted emails
imap_server.expunge()

# Logout and close the connection
imap_server.logout()
