import os
import sys
import platform
import requests
import urllib.request
import urllib, json
cmds = ['ping', 'help', 'sys', 'update', 'about', 'debug', 'restart', 'cd', 'dir', 'read', 'create', 'write', 'append', 'delete', 'mkdir', 'deldir', 'rmdir', 'echo', '@echo', 'readll', 'clear', 'fetch']
cmds.sort()
cmds.append('quit')
ver = "0.1.1-alpha"
OS = platform.system()
dir = os.getcwd()
defaultdir = dir
installloc = __file__
print("OS: " + OS)
print("Directory: " + os.getcwd())
print("Default Directory: " + defaultdir)
print("File located at: " + installloc)
updateurl = "https://raw.githubusercontent.com/ccjit/PyTerm/refs/heads/main/main.py"
versionsurl = "https://raw.githubusercontent.com/ccjit/PyTerm/refs/heads/main/versions.json"
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
        if OS == "Windows":
            stream = os.popen(f'ping /n 4 {ip}')
        else:
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
            if  ver == data['latest']:
                print("PyTerm is up to date.")
            else:
                if ver == data['soon']:
                    print("PyTerm is running a beta version, you may encounter bugs or instability.")
                else:
                    if ver in data['previous']:
                        print("PyTerm is outdated. Run \"update install\" to install the new update.")
                    else: 
                        print("You are running an unknown version of PyTerm. Run \"update install\" to install the latest version of PyTerm and to revert all changes you made to this file prior to updating.")
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
            
        if ver == data['latest']:
            updated = True
        else:
            if ver == data['soon']:
                updated = True
            else:
                if ver in data['previous']:
                    updated = False
                else: 
                    updated = False

        response = requests.get(updateurl)
        if updated:
            print("PyTerm is already up to date!") 
        else:
            if response.status_code == 200:
                print("Updating...")
                debug("Fetching files to add...")
                file = urllib.request.urlretrieve(updateurl, installloc)
                debug(file)
                print("Updated!")
                print("Restarting PyTerm...")
                print("Changelog for PyTerm " + data['latest'] + ": " + data['changelog'])
                os.execv(sys.executable, ["python3"] + [installloc])
            else:
                print(f"Error {response.status_code} when trying to update.")
    elif param == "changelog":
        debug("Fetching versions file...")
        debug("If your connection speed is low, this might take a while.")
        with urllib.request.urlopen(versionsurl) as file:
            debug("File fetched. Loading file...")
            data = json.load(file)
            debug("Loaded.")
        debug(file)
        print("Changelog for PyTerm version " + data['latest'] + ": " + data['changelog'])
    else:
        print("Unknown parameter")
echo = True  
while True:
    if echo:
        prompt = input(dir + "> ")
    else:
        prompt = input("")
    args = prompt.split(' ')
    cmd = args[0]
    substring = prompt[len(cmd) + 1:]
    pre = cmd + " - "
    def log(str):
        if echo:
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
        elif cmd == "restart":
            log("Restarting PyTerm...")
            os.execv(sys.executable, ["python3"] + [installloc])
        elif cmd == "debug":
            if debugging:
                debugging = False
                log("Debugging is now off.")
                debug(pre + "If you can see this message, it means debugging didn't turn off.")
            else:
                debugging = True
                log("Debugging is now on.")
        elif cmd == "fetch":
            if len(args) == 1:
                log("Please specify a link to a file hosted online to fetch.")
            else:
                debug("Fetching file...")
                if substring.startswith("http://"):
                    log("To fetch, you need a secure protocol connection.")
                    print("In short, fetch doesn't support http:// for security measures.")
                else:
                    try:
                        if substring.startswith("https://"):
                            with urllib.request.urlopen(substring) as data:
                                debug("Fetched.")
                                debug("Printing...")
                                log("Data:")
                                print(data.read())
                        else:
                            with urllib.request.urlopen("https://" + substring) as data:
                                debug("Fetched.")
                                debug("Printing...")
                                log("Data:")
                                print(data.read())
                    except:
                        log("There was an error when fetching the file. Maybe check the URL provided?")
        elif cmd == "echo":
            print(substring)
        elif cmd == "clear":
            if OS == "Windows":
                os.system('cls')
            else:
                os.system('clear')
        elif cmd == "dir":
          onlyfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
          onlyfolders = [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]
          if not len(onlyfiles) == 0:
              print("---Files---")
              print("    ".join(onlyfiles))
          if not len(onlyfolders) == 0:
              print("~~~Folders~~~")
              print("    ".join(onlyfolders))
          if len(onlyfiles) == 0 and len(onlyfolders) == 0:
              print("(Empty)")
        elif cmd == "cd":
            if len(args) == 1:
                log("Please specify a directory to go to.")
            else:
                if substring == ";":
                    debug("Going to default directory...")
                    os.chdir(defaultdir)
                    dir = os.getcwd()
                else:
                    if substring == "..":
                        debug("Going down one folder...")
                        os.chdir('..')
                        dir = os.getcwd()
                    else:
                        onlyfolders = [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]
                        if substring in onlyfolders:
                            os.chdir(os.getcwd() + "/" + substring)
                            dir = os.getcwd()
                        else:
                            log("Error 02.5 - Directory not found")
        elif cmd == "read":
            if len(args) == 1:
                log("Please specify a text file to read.")
            else:
                onlyfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
                if substring in onlyfiles:
                    if substring.endswith(".txt"):
                        with open(substring, "r") as file:
                            content = file.read()
                        print(content)
                    else:
                        log("File must be a .txt file!")
                else:
                    log("Error 02 - File not found")
        elif cmd == "readll":
            if len(args) == 1:
                log("Please specify a file to read.")
            else:
                onlyfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
                if substring in onlyfiles:
                    try: 
                        with open(substring, "r") as file:
                            content = file.read()
                        print(content)
                    except:
                        log("Cannot read this file.")
                else:
                    log("Error 02 - File not found")
        elif cmd == "create":
            if len(args) == 1:
                log("Please specify a file name to make a text file of.")
            else:
                if args[1] + ".txt" in os.listdir():
                    log("You can't create a file with an existing file name! Use \"write\" to edit that file!")
                else:
                    if os.access(dir, os.W_OK):
                        with open(args[1] + ".txt", "w") as f:
                            f.write("")
                    else:
                        log("Cannot create file on a read-only directory.")
        elif cmd == "mkdir":
            if len(args) == 1:
                log("Please specify a folder name to create.")
            else:
                invalid = [".", "/", "?", "\\", ";", ":"]
                def callback(char):
                    return char in substring
                if any(callback(char) for char in invalid):
                    log("Folder name contains invalid characters!")
                else:
                    if os.access(dir, os.W_OK):
                        os.mkdir(substring)
                    else:
                        log("Cannot create directory on a read-only directory.")
        elif cmd == "deldir" or cmd == "rmdir":
            if len(args) == 1:
                log('Please specify a directory to delete.')
            else:
                if substring in installloc:
                    log("Cannot delete directory that hosts self!")
                else:
                  if os.access(dir, os.W_OK):
                      os.rmdir(substring)
                  else:
                      log("Cannot delete directory on a read-only directory.")
                      
        elif cmd == "write":
            if len(args) < 3:
                log("Please specify a file and contents to write to. Usage: \"write <file> '<contents>'\" (single quotes are required)")
            else:
                if prompt.count("'") < 2:
                    log("The syntax of the command is invalid.")
                else:
                    if args[1] == os.path.basename(__file__):
                        log("Cannot overwrite self!")
                    else:
                        if os.access(dir, os.W_OK):
                            try:
                                with open(args[1], "w") as f:
                                    f.write(prompt.split("'")[1])
                            except:
                                log("Couldn't write to file.")
                        else:
                            log("Cannot write to file on a read-only directory!")
        elif cmd == "append":
            if len(args) < 3:
                log("Please specify a file name and contents to append to the desired file. Usage: \"append <file> '<contents>'\" (single quotes are required)")
            else:
                if prompt.count("'") < 2:
                    log("The syntax of the command is invalid.")
                else:
                    if args[1] == os.path.basename(__file__):
                        log("Cannot append to self!")
                    else:
                        if os.access(dir, os.W_OK):
                            try:
                                with open(args[1], "a") as f:
                                    f.write(prompt.split("'")[1])
                            except:
                                log("Couldn't append to file.")
                        else:
                            log("Cannot append text to file on a directory that is read-only!")
        elif cmd == "delete":
            if len(args) == 1:
                log("Please specify a file to delete.")
            else:
                if args[1] == os.path.basename(__file__):
                    log("Cannot self destruct!")
                else:
                    if os.access(dir, os.W_OK):
                        onlyfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
                        if substring in onlyfiles:
                            os.remove(args[1])
                        else:
                            log("Error 02 - File not found")
                    else:
                        log("Cannot delete file on a read-only directory")
    else:
      if cmd == "cd..":
          os.chdir('..')
          dir = os.getcwd()
      else:
          if cmd == "@echo":
              if echo:
                  print("@echo - Command echo is now off.")
                  echo = False
                  print("(run \"@echo\" again to turn on command echo)")
              else:
                  echo = True
                  print("@echo - Command echo is now on.")
          else:
              print("The command " + cmd + " does not exist. Use \"help\" to get a list of commands.")
