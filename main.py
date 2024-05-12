import os
import sys
import requests
import json
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
    print("Using {}".format(cred_file))
    with open(cred_file) as ifile:
        creds = json.load(ifile)

    print("Pushing: {} : {}".format(creds['host'],extern_ip))
        
    push_url = "https://{0}:{1}@domains.google.com/nic/update?hostname={2}&myip={3}".format(
        creds['user'],
        creds['password'],
        creds['host'],
        extern_ip
    )
    r=requests.get(push_url)
    print(r.text)
