import os
import sys
import platform
import requests
import urllib.request
import urllib, json
cmds = ['ping', 'help', 'sys', 'update', 'about', 'debug']
cmds.sort()
cmds.append('quit')
print("OS: " + platform.system())
print("Directory: " + os.getcwd())
ver = "0.0.4.8-alpha"
OS = platform.system()
dir = os.getcwd()
updateurl = "https://raw.githubusercontent.com/ccjit/PyTerm/refs/heads/main/main.py"
versionsurl = "https://raw.githubusercontent.com/ccjit/PyTerm/refs/heads/main/versions.json"
defaultdir = dir
print("Default directory: " + defaultdir)
debugging = False
def debug(str: str):
    if debugging:
        print(str)
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
        if OS == "Linux":
            stream = os.popen(f'ping -c 4 {ip}')
        elif OS == "Windows":
            stream = os.popen(f'ping /n 4 {ip}')
        elif OS == "Darwin":
            stream = os.popen(f'ping -c 4 {ip}')
        elif OS == "FreeBSD":
            stream = os.popen(f'ping -c 4 {ip}')
        debug("Pinging " + ip + " with 4 packets...")
        stream = os.popen(f'ping -c 4 {ip}')
        debug("Pinged. Reading output.")
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
            debug("Fetching versions file...")
            debug("If your connection speed is low, this might take a while.")
            with urllib.request.urlopen(versionsurl) as file:
                data = json.load(file)
            debug("Versions file loaded.")
            debug(data)
            debug("Checking for updates...")
            if data['latest'] == ver:
                print("PyTerm is up to date.")
            else:
                if ver == data['soon']:
                    print("PyTerm is running a beta version, you may encounter bugs or instability.")
                else:
                    print("PyTerm is outdated. Run \"update install\" to install the new update.")
        else:
            print(f"Error {response.status_code}")
    elif param == 'install':
        debug("Fetching versions file...")
        debug("If your connection speed is low, this might take a while.")
        with urllib.request.urlopen(versionsurl) as file:
            data = json.load(file)
        debug("Versions file loaded.")
        debug(data)
        debug("Checking if PyTerm is already up to date...")
            
        if data['latest'] == ver:
            updated = True
        else:
            if ver == data['soon']:
                updated = True
            else:
                updated = False
        response = requests.get(updateurl)
        if updated:
            print("PyTerm is already up to date!") 
        else:
            if response.status_code == 200:
                print("Updating...")
                debug("Fetching files to add...")
                file = urllib.request.urlretrieve(updateurl, defaultdir + "?main.py")
                debug(file)
                print("Updated!")
                print("Restarting PyTerm...")
                os.execv(sys.executable, ["python3"] + [defaultdir + "/main.py"])
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
        elif cmd == "debug":
            if debugging:
                debugging = False
                log("Debugging is now off.")
                debug(pre + "If you can see this message, it means debugging didn't turn off.")
            else:
                debugging = True
                log("Debugging is now on.")
    else:
        print("The command " + cmd + " does not exist. Use \"help\" to get a list of commands.")
