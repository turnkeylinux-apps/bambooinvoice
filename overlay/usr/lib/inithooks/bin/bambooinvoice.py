#!/usr/bin/python
"""Set BambooInvoice admin password, email and domain to serve

Option:
    --pass=     unless provided, will ask interactively
    --email=    unless provided, will ask interactively
    --domain=   unless provided, will ask interactively
                DEFAULT=www.example.com
"""

import sys
import getopt
import inithooks_cache
import subprocess
from subprocess import PIPE
from os.path import *

from dialog_wrapper import Dialog
from mysqlconf import MySQL
from executil import system


def usage(s=None):
    if s:
        print >> sys.stderr, "Error:", s
    print >> sys.stderr, "Syntax: %s [options]" % sys.argv[0]
    print >> sys.stderr, __doc__
    sys.exit(1)

DEFAULT_DOMAIN="www.example.com"


def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "h",
                                       ['help', 'pass=', 'email=', 'domain='])
    except getopt.GetoptError, e:
        usage(e)

    email = ""
    domain = ""
    password = ""
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()
        elif opt == '--pass':
            password = val
        elif opt == '--email':
            email = val
        elif opt == '--domain':
            domain = val

    if not password:
        d = Dialog('TurnKey Linux - First boot configuration')
        password = d.get_password(
            "BambooInvoice Password",
            "Enter new password for the 'admin' account.")

    if not email:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        email = d.get_email(
            "BambooInvoice Email",
            "Enter email address for the 'admin' account.",
            "admin@example.com")

    inithooks_cache.write('APP_EMAIL', email)

    if not domain:
        if 'd' not in locals():
            d = Dialog('TurnKey Linux - First boot configuration')

        domain = d.get_input(
            "BambooInvoice Domain",
            "Enter the domain to serve BambooInvoice.",
            DEFAULT_DOMAIN)

    if domain == "DEFAULT":
        domain = DEFAULT_DOMAIN

    inithooks_cache.write('APP_DOMAIN', domain)

    command = ["php", join(dirname(__file__), 'bambooinvoice_pass.php'), password]
    p = subprocess.Popen(command, stdin=PIPE, stdout=PIPE, shell=False)
    stdout, stderr = p.communicate()
    if stderr:
        fatal(stderr)

    cryptpass = stdout.strip()

    m = MySQL()
    m.execute('UPDATE bambooinvoice.clientcontacts SET password=\"%s\" WHERE id=1;' % cryptpass)
    m.execute('UPDATE bambooinvoice.clientcontacts SET email=\"%s\" WHERE id=1;' % email)
    m.execute('UPDATE bambooinvoice.settings SET primary_contact_email=\"%s\" WHERE id=1;' % email)

    conf = "/var/www/bambooinvoice/bamboo_system_files/application/config/config.php"
    system("sed -i \"s|^\$config\['base_url.*|\$config['base_url'] = 'http://%s/';|\" %s" % (domain, conf))

if __name__ == "__main__":
    main()

