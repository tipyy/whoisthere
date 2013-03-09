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
if opt[0] == '-h':
            Usage()
        if opt[0] == '-l':
            LOOP_ENABLED = True
            LOOP_WAIT_TIME = opt[1]

#let's go !
try:
    mygetopts()
    print time.strftime("%d/%m/%Y %H:%M") 
    #getting the whitelist from file
    whitelist = []
    whitelistFile = open(whitelistFileUri, "r")
    for line in whitelistFile:
        if line[0] != "#":
            whitelist.append(string.split(line.strip('\n'), " "))
    whitelistFile.close()

    #run a 'nmap' command and assign results to a variable
    #commandString = "nmap -T4 -sP 192.168.0.* | grep -v ^$ | grep -v Nmap | grep -v " + me
    commandString = "nmap -T4 -sP 192.168.0.* | grep -v ^$ | grep -v Nmap"
    commandOutput = commands.getoutput(commandString)
    findResults = string.split(commandOutput, "\n")

    #getting hosts list with mac addresses
    hosts = []
    for result in findResults:
        splittedResult = string.split(result, " ")
        if result[0:4] == "Host":
            host = []
            host.append(splittedResult[1]) 
        elif result[0:12] == "MAC Address:":      
            host.append(splittedResult[2]) 
            hosts.append(host)

    #display
    print "=================================================================="
    for daHost in hosts:
        print "Machine : " + daHost[0] + " Adresse MAC : " + daHost[1]
        finded = False
        whitelistName = ""
        for w in whitelist:
            if daHost[1].upper() in w:
finded = True
                whitelistName = w[1]
        if finded:
            print "ok c'est " + whitelistName
        else:
            print "un intrus"
            print "payes ton scan sur " + daHost[0]
            commandString = "nmap -A " + daHost[0]
            commandOutput = commands.getoutput(commandString)
            print commandOutput
            if MAIL:
                print "On envoi le mail avec le resultat du scan"
                send(commandOutput)
        print "=================================================================="
except Exception as e:
    print "On a eu un petit soucis"
    print e
