import os
import platform
import requests
import urllib.request
import urllib, json
cmds = ['ping', 'help', 'sys', 'update', 'about', 'quit']
print("OS: " + platform.system())
print("Directory: " + os.getcwd())
ver = "0.0.3-alpha"
OS = platform.system()
dir = os.getcwd()
updateurl = "https://raw.githubusercontent.com/ccjit/PyTerm/refs/heads/main/main.py"
versionsurl = "https://raw.githubusercontent.com/ccjit/PyTerm/refs/heads/main/versions.json"
defaultdir = dir
def ping(ip):
    if ip == "-h":
        print("ping - usage: ping <ip address> - parameters: -t (checks if IP is reachable), -h (print this message)")
    elif ip == '-t':
        '''
        stream = os.popen(f'ping -c 4 {ip[3:]}')
        output = stream.read()
        if '0 received' in output:
            print('IP unreachable')
        else:
            print('IP reachable')
        '''
        print('Error 00 - deprecated command-parameter combo')
    else:
        stream = os.popen(f'ping -c 4 {ip}')
        output = stream.read()
        print('pinging ' + ip)
        if '0 received' in output:
            print('Error 01 - IP unreachable')
        else:
            print(output)
def checkupdate(param):
    if param == "":
        response = requests.get(versionsurl)
        if response.status_code == 200:
            with urllib.request.urlopen(versionsurl) as file:
                data = json.load(file)
            if data['latest'] == ver:
                print("PyTerm is up to date.")
            else:
                if ver in data['soon']:
                    print("PyTerm is running a beta version, you may encounter bugs or instability.")
                else:
                    print("PyTerm is outdated. Run \"update install\" to install the new update.")
        else:
            print(f"Error {response.status_code}")
    elif param == 'install':
        with urllib.request.urlopen(versionsurl) as file:
            data = json.load(file)
        if data['latest'] == ver:
            updated = True
        else:
            if ver in data['soon']:
                updated = True
            else:
                updated = False
        response = requests.get(updateurl)
        if updated:
            print("PyTerm is already up to date!") 
        else:
            if response.status_code == 200:
                file = urllib.request.urlretrieve(updateurl, "main.py")
                print(file)
            else:
                print(f"Error {response.status_code} when trying to update.")
        
while True:
    prompt = input(dir + "> ")
    args = prompt.split(' ')
    cmd = args[0]
    substring = prompt[len(cmd) + 1:]
    pre = cmd + ": "
    def log(str):
        print(pre + str) 
    if cmd in cmds:
        if cmd == 'ping':
            if len(args) == 1:
                log(pre + "Please specify an IP address or parameter for this command. Do \"ping -h\" to get help on this command.")
            else:
                ping(substring)
        elif cmd == 'help':
            log('PyTerm commands: ' + ", ".join(cmds))
        elif cmd == 'sys':
            log('Running PyTerm v' + ver + " on " + OS)
            log('Running on directory ' + dir)
        elif cmd == "update":
            checkupdate(substring)
        elif cmd == "about":
            log("PyTerm v" + ver + " - Made by ccjt in 2025")
        elif cmd == "quit":
            log("Quitting...")
            exit(0)
    else:
        print("The command " + cmd + " does not exist. Use \"help\" to get a list of commands.")
