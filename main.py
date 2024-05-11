import os
import sys
import requests
from typing import TextIO


def get_cred_file():
    """Gets the cred file
    Command Line First
    Then $IP_CRED_FILE
    Finally $USER/.ip_cred_file
    """
    # Argv
    if len(sys.argv) > 1:  # Provided argv
        cred_file = sys.argv[1]
        if os.path.isfile(cred_file):
            print("Using Command Line")
            return cred_file

    # ENV Set Variable File
    print("No Command Line File Given")

    cred_file = os.getenv('IP_CRED_FILE', None)
    if cred_file != None:
        if os.path.isfile(cred_file):
            print("Using $IP_CRED_FILE")
            return cred_file

    print("Unable to find IP_CRED_FILE")
    cred_file = os.path.join(os.path.expanduser('~'), '.ip_cred_file')
    if os.path.isfile(cred_file):
        print("Using User .ip_cred_file")
        return cred_file

    return None

if __name__ == '__main__':
    print("Starting")
    cred_file = get_cred_file()
    
    extern_ip = requests.get('https://ident.me').text
    
    ifile: TextIO
    with open(cred_file, 'r') as ifile:
        host = ifile.readline()
        user = ifile.readline()
        password = ifile.readline()
        
    push_url = "https://{0}:{1}@domains.google.com/nic/update?hostname={2}&myip={3}".format(
        user,
        password,
        host,
        extern_ip
    )

