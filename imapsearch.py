#!/usr/bin/env python3
import getpass, imaplib
import email
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search IMAP')
    parser.add_argument('hostname', nargs=1, help='Hostname of the IMAP server')
    parser.add_argument('-l', '--login', default=getpass.getuser(), help='Login name for IMAP server')
    parser.add_argument('-f', '--folder', default='INBOX', help='folder to search in')
    parser.add_argument('-m', '--msgid', required=True, help='Message id to search for')
    args = parser.parse_args()

    M = imaplib.IMAP4_SSL(args.hostname[0])
    M.login(args.login, getpass.getpass())
    ret = M.select(args.folder, readonly=True)
    typ, data = M.search(None, '(HEADER Message-id %s)' % args.msgid)
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                print(part.get_payload())
    M.close()
    M.logout()
