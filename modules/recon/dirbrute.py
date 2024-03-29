import subprocess
import os
import ssl
import socket

wordlist_path = os.path.join(os.path.dirname(__file__), '../wordlists/DIR')


# This function checks whether the domain or subdomain has SSL enabled or not 
def has_ssl(domain):
    try:
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(socket.socket(), server_hostname=domain)
        s.connect((domain, 443))
        return True
    except:
        return False
    



def godir(target,mode):
    directories = []
    
    if(mode == 1):
        wordlist = os.path.join(wordlist_path,"small.txt")
    else:
        wordlist = os.path.join(wordlist_path,"medium.txt")

    if has_ssl(target):
        target = "https://"+target
    else:
        target = "http://"+target

    # Above snippet checks if the url must be appended with http or https
    gobuster_process = subprocess.Popen(
        ['gobuster', 'dir', '-u', target, '-w', wordlist],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output, error = gobuster_process.communicate()
    if gobuster_process.returncode != 0:
        print(f"Error running Gobuster: {error}")
        return directories
    for line in output.decode().split('\n'):
        if line.startswith('\r/'):
            directory = line.split(' ')[0]
            directories.append(directory.replace("\r",""))
    print(f"[+] Gobuster found {len(directories)} directories!!")
    return directories


print(godir("unipune.ac.in",1))