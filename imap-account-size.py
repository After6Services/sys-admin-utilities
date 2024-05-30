import imaplib

  

# IMAP server details
IMAP_SERVER = 'server.com'
IMAP_PORT = 993

  

# Email account credentials
EMAIL_ADDRESS = 'email_address'
PASSWORD = 'password'

  

# Connect to the IMAP server
imap_server = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

  

# Login to the email account
imap_server.login(EMAIL_ADDRESS, PASSWORD)

  

# Select the mailbox (e.g., 'INBOX')
mailbox = 'INBOX'
imap_server.select(mailbox)

  

# Get all mail IDs
result, data = imap_server.uid('search', None, "ALL")
mail_ids = data[0].split()

  

# Calculate the total size of the mailbox
total_size = 0

for id in mail_ids:
    try:
        result, data = imap_server.uid('fetch', id, '(RFC822.SIZE)')
        total_size += int(data[0].split()[2])
    except imaplib.IMAP4.error as e:
        print(f"IMAP error: {e}")
    except IndexError as e:
        print(f"Index error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

print(f'Total size of the mailbox: {total_size} bytes')

# Logout and close the connection
imap_server.logout()