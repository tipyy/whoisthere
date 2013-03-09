#!/usr/bin/python
# by Tonton<onclebobs@gmail.com>

import stat, sys, os, string, commands, time, smtplib, getopt

#some modifiable vars todo: use getopts to set those vars
whitelistFileUri = "~/scripts/whitelist"
mailto="user@host"
MAIL = True
VERBOSE = False
LOOP_ENABLED = False
LOOP_WAIT_TIME = 120

#smtp defintion
src = "user@host"
password = "******"
dest = "user@host"

def send(text):
    mail = "To: " + dest + "\nFrom: " + src + "\nSubject: INTRUDER\n\n" + text
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(src, password)
    smtp.sendmail(src, dest, mail)
    smtp.close()

#getopts
def Usage ():
    print "whoisthere [-v][-p][-h]"
    sys.exit(0)

def mygetopts():
    try:
        optlist, list = getopt.getopt(sys.argv[1:], ':vnhf:l:')
    except getopt.GetoptError:
        Usage()
        sys.exit(1)

    for opt in optlist:
        if opt[0] == '-v':
            VERBOSE = True
        if opt[0] == '-n':
            MAIL = False
        if opt[0] == '-f':
            whitelistFileUri = opt[1]
