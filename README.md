# sys-admin-utilities

Utilities for Managing Servers from After6 Services LLC.

# Requirements

* Python 3
* UNIX-like environment, such as MacOS or Linux

# Usage

## imap-account-size.py

### Configuration

Since The script is not written to take commandline parameters at the present time, you must make changes directly to the source code of the script.

### Execution

On most Unix-like systems, invoke the script using:

python3 imap-account-size.py


## imap-account-delete-from-sender.py

This script connects to an IMAP email account, deletes all emails from senders matching an email address pattern, and expunges the deleted emails.

## Configuration

imap-account-delete-from-sender.py takes command line parameters, so pass the configuration on the command line as follows:

* IMAP_SERVER (such as mail.server.com.)
* IMAP_PORT (possibly 993, check your mail server configuration.)
* EMAIL_ADDRESS (for the IMAP account being modified.)
* PASSWORD (for the IMAP account being modified.)
* FROM_EMAIL (from email address *pattern* to delete, i.e. "notification*?@leagueathletics.com$", without the quotes.)
* AGE (minimum age of emails to delete, in days).

### Execution

On most Unix-like systems, invoke the script using:

python3 imap-account-delete-from-sender.py mail.server.com 993 email@server.com password notification*?@leagueathletics.com$ 365

# Support

Although After6 Services LLC has developed these scripts, After6 only provides support for them as part of a technical support agreement that references these scripts by name.

# License

This scripts are licensed under The MIT License, http://www.opensource.org/licenses/mit-license.php.  See LICENSE.md for the exact license.

# Authorship

sys-admin-utiliies was originally written by Dave Aiello.  sys-admin-utilities is maintained by Dave Aiello.

# Copyright

Copyright &copy; 2024, After6 Services LLC.  All Rights Reserved.

Trademarks, product names, company names, or logos used in connection with this repository are the property of their respective owners and references do not imply any endorsement, sponsorship, or affiliation with After6 Services LLC unless otherwise specified.
