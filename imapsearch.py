#!/usr/bin/python
import getpass, imaplib

import sys

login="eugeni.dodonov"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Usage: %s <folder> <message-id>" % sys.argv[0]
        sys.exit(1)

    print "Using login %s" % login
    passwd = getpass.getpass()
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    M.login(login, passwd)
    ret = M.select(sys.argv[1])
    typ, data = M.search(None, '(HEADER Message-id %s)' % sys.argv[2])
    for num in data[0].split():
        typ, data = M.fetch(num, '(RFC822)')
        print data[0][1]
    M.close()
    M.logout()
