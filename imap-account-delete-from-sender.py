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

# From email address pattern to delete
FROM_EMAIL = sys.argv[5]

# Pattern to match the sender's email address
sender_pattern = re.compile(FROM_EMAIL)

# Minimum age of emails to delete (in days)
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

# Get all mail IDs for messages older than AGE days
result, data = imap_server.uid('search', None, "BEFORE", date_threshold.strftime("%d-%b-%Y"))
mail_ids = data[0].split()

# Set email_deleted_count to 0
email_deleted_count = 0

# Delete all emails from the senders matching the email address pattern
for id in mail_ids:
    # Fetch the email headers
    result, data = imap_server.uid('fetch', id, '(BODY[HEADER.FIELDS (FROM DATE SUBJECT)])')
    raw_email = data[0][1].decode('utf-8', errors='ignore')

    # Parse the email headers to get the sender's email address
    email_message = email.message_from_string(raw_email)
    from_address = email.utils.parseaddr(email_message['From'])[1]

    # Parse the email headers to get the date
    date_str = email_message.get('Date')

    # Get email subject
    subject = email_message.get('Subject')

    # If the sender's email address matches the pattern, mark the email for deletion
    if sender_pattern.match(from_address):
        print(f"Deleting email: {subject} from: {from_address} with date: {date_str}")

        try:
            imap_server.uid('store', id, '+FLAGS', '\\Deleted')
            email_deleted_count += 1
        except imaplib.IMAP4.error as e:
            print(f"IMAP error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}") 

    else:
        print(f"Skipping email: {subject} from: {from_address} with date: {date_str}")

# Expunge the deleted emails
try:
    imap_server.expunge()
    print(f"Expunged {email_deleted_count} deleted emails.")
except imaplib.IMAP4.error as e:
    print(f"IMAP error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

# Logout and close the connection
imap_server.logout()
