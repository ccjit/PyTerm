import os
import sys
import platform
import urllib.request
import urllib.error
import urllib, json
import logging as error
from datetime import date
import subprocess
import re
import inspect
cmds = ['ping', 'help', 'sys', 'update', 'about', 'debug', 'restart', 'cd', 'dir', 'read', 'create', 'write', 'append', 'delete', 'mkdir', 'deldir', 'rmdir', 'echo', 'readll', 'clear', 'fetch', 'clone', 'run', 'let', 'unlet', 'var', 'vars', 'import', 'ask', 'exit', 'skip']
cmds.sort()
cmds.append('quit')
errors = {
    "00": "deprecated command-parameter combo",
    "01": "IP unreachable",
    "02": "File not found",
    "02.5": "Directory not found"
}
true = True
false = False
answer = ""
def formatErrorCode(code):
    return f"Error {code} - {errors.get(code)}"
class Vars:
    ver = "0.2.0"
    date = date.today().strftime('%d')
    defaultdir = os.path.dirname(os.path.abspath(__file__))
    installloc = os.path.abspath(__file__)
    filename = os.path.basename(os.path.abspath(__file__))
    on_su = os.geteuid() == 0
    OS = platform.system()
vars = Vars()
vars.date = int(vars.date)
dir = os.getcwd()
ver = vars.ver
OS = vars.OS
defaultdir = vars.defaultdir
installloc = vars.installloc
filename = vars.filename
on_su = vars.on_su
updateurl = "https://ccjt.sad.ovh/api/programs/pyterm"
versionsurl = "https://ccjt.sad.ovh/api/pyterm/versions"
isupdateday = False
print("OS: " + OS)
print("Directory: " + os.getcwd())
print("Default Directory: " + defaultdir)
print("File located at: " + installloc)
print("Filename: " + filename)
print("On SuperUser: " + str(on_su))
class Colors:
    red = '\033[91m'
    green = '\033[92m'
    blue = '\033[94m'
    yellow = '\033[93m'
    reset = '\033[0m'
    bold = '\033[1m'
    under = '\033[4m'
if isupdateday:
    print("Checking for updates...")
    with urllib.request.urlopen(versionsurl) as file:
        data = json.load(file)
    if data['latest'] == ver:
        print("All good! Proceeding to shell.")
    else:
        if ver in data['previous']:
            print("Ding ding! Updates are due.")
            print("Installing updates...")
            response = requests.get(updateurl)
        if response.status_code == 200:
            print("Updating...")
            file = urllib.request.urlretrieve(updateurl, installloc)
            print("Updated!")
            print("Restarting PyTerm...")
            print("Changelog for PyTerm " + data['latest'] + ": " + data['changelog'])
            os.execv(sys.executable, ["python3"] + [installloc])
        else:
            print(f"Error {response.status_code} when trying to update.")
debugging = False
def debug(text: str):
    if debugging and echo:
        line = inspect.stack()[1][2]
        print(f"{line} - [{Colors.yellow}DEBUG{Colors.reset}]: " + str(text))
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
        print(f'{formatErrorCode('00')}')
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
            print(f'{formatErrorCode('01')}')
        else:
            print(output)
def checkupdate(param):
    if param == "" or param == "none":
        try:
            debug("Fetching versions file...")
            debug("If your connection speed is low, this might take a while.")
            with urllib.request.urlopen(versionsurl) as file:
                data = json.load(file)
            debug("Versions file loaded.")
            debug(data)
            debug("Checking for updates...")
            if  ver == data['latest']:
                print(f"PyTerm is {Colors.green}up to date{Colors.reset}.")
            else:
                if ver == data['soon']:
                    print(f"PyTerm is running a {Colors.yellow}beta{Colors.reset} version, you may encounter bugs or instability.")
                else:
                    if ver in data['previous']:
                        print(f"PyTerm is {Colors.red}outdated{Colors.reset}. Run \"update install\" to install the new update.")
                    else: 
                        print(f"You are running an {Colors.yellow}unknown{Colors.reset} version of PyTerm. Run \"update install\" to install the latest version of PyTerm and to revert all changes you made to this file prior to updating.")
        except Exception as e:
            print(f"Something happened while retrieving update data.")
            debug(e)
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

        if updated:
            print("PyTerm is already up to date!") 
        else:
            try:
                print("Updating...")
                debug("Fetching files to add...")
                file = urllib.request.urlretrieve(updateurl, installloc)
                debug(file)
                print("Updated!")
                print("Restarting PyTerm...")
                print("Changelog for PyTerm " + data['latest'] + ": " + data['changelog'])
                os.execv(sys.executable, ["python3"] + [installloc])
            except:
                print("An error occured when updating.")
    elif param == "changelog":
        debug("Fetching versions file...")
        debug("If your connection speed is low, this might take a while.")
        with urllib.request.urlopen(versionsurl) as file:
            debug("File fetched. Loading file...")
            data = json.load(file)
            debug("Loaded.")
        debug(data)
        print("Changelog for PyTerm version " + data['latest'] + ": " + data['changelog'])
    elif param == "latest":
        debug("Fetching versions file...")
        debug("If your connection speed is low, this might take a while.")
        with urllib.request.urlopen(versionsurl) as file:
            debug("File fetched. Loading file...")
            data = json.load(file)
            debug("Loaded.")
        debug(data)
        print("The latest downloadable PyTerm version is v" + data['latest'] + ".")
    elif param == "planned":
        debug("Fetching versions file...")
        debug("If your connection speed is low, this might take a while.")
        with urllib.request.urlopen(versionsurl) as file:
            debug("File fetched. Loading file...")
            data = json.load(file)
            debug("Loaded.")
        debug(data)
        print("---Planned PyTerm features---")
        print(data['planned'])
    elif param == "soon":
        debug("Fetching versions file...")
        debug("If your connection speed is low, this might take a while.")
        with urllib.request.urlopen(versionsurl) as file:
            debug("File fetched. Loading file...")
            data = json.load(file)
            debug("Loaded.")
        debug(data)
        print("The next (planned) PyTerm version is v" + data['soon'] + ".")    
    elif param == "params":
        print("Parameters:")
        print(f"{Colors.blue}none{Colors.reset} - Checks for updates.\n{Colors.blue}install{Colors.reset} - Installs the latest version of PyTerm.\n{Colors.blue}changelog{Colors.reset} - Gives you the changelog for the latest PyTerm version.\n{Colors.blue}latest{Colors.reset} - Tells you what the latest version of PyTerm is.\n{Colors.blue}planned{Colors.reset} - Gives you a list of planned PyTerm features.\n{Colors.blue}soon{Colors.reset} - Tells you the next planned PyTerm version.\n{Colors.blue}params{Colors.reset} - Prints these exact messages.\n")
    else:
        print(f"{Colors.red}{Colors.bold}Unknown parameter{Colors.reset}")
        print(f"Use {Colors.bold}{Colors.blue}update params{Colors.reset} to get a list of parameters.")
def join(elements, n, separator=" "):
    chunks = []
    for i in range(0, len(elements), n):
        chunk = elements[i:i + n]
        chunks.append(separator.join(chunk))
    return "\n".join(chunks)
echo = True
mem = None
skipping = False
imported  = {}
def execute(prompt):
    global skipping
    global mem
    global cmds
    global vars
    global echo
    global OS
    global imported
    global updateurl
    global versionsurl
    global dir
    global debugging
    ver = vars.ver
    defaultdir = vars.defaultdir
    installloc = vars.installloc
    filename = vars.filename
    for var in globals():
        exec("global " + var)
    on_su = vars.on_su
    args = prompt.split(' ')
    for i in range(len(args)):
        match = re.search(r"v:\{(\w+)\}", args[i])
        if match:
            if match.group(1) in globals():
                args[i] = re.sub(r"v:\{(\w+)\}", str(globals()[match.group(1)]).strip('"'), args[i])
    substring = prompt[len(args[0]) + 1:]
    ogprompt = prompt
    prompt = prompt.lower()
    cmd = args[0]
    pre = f"{Colors.blue}{Colors.under}{Colors.bold}" + cmd + f"{Colors.reset} - "
    def log(str):
        if echo:
            print(Colors.reset + pre + str)
    
    if cmd in cmds and not skipping:
        if cmd == 'ping':
            if len(args) == 1:
                log(f"Please specify an IP address or parameter for this command. Do {Colors.blue}{Colors.bold}ping -h{Colors.reset} to get help on this command.")
            else:
                ping(substring)
        elif cmd == 'array':
            if len(args) < 3:
                log("Incorrect Syntax. Usage: 'array <list name> <item>'")
            else:
                try:
                    log(globals(args[1])[int(args[2])])
                except Exception as e:
                    log("Error.")
                    debug(e)
        elif cmd == 'import':
            if len(args) > 1:
                print("this is a test message")
        elif cmd == "help":
            log('PyTerm commands:\n' + join(cmds, 10, ", "))
        elif cmd == 'sys':
            pre2 = ""
            if on_su:
                pre2 = " in the Super User profile"
            log('Running PyTerm v' + ver + " on " + OS + pre2)
            log('Running on directory ' + dir)
        elif cmd == "update":
            checkupdate(substring)
        elif cmd == "about":
            log("PyTerm v" + ver + " - Made by ccjt in 2025")
        elif cmd == "exit":
            return 0
        elif cmd == "quit":
            log("Quitting...")
            exit(0)
        elif cmd == "skip":
            log('The next command will be skipped.')
            skipping = True
        elif cmd == "let":
            if len(args) < 4:
                log("Please specify a variable name and value to set to.")
                log("Syntax: let (variable name: 1 word) = (value, string, number, etc)")
            else:
                try:
                    try:
                        args[3] = float(prompt[len(args[0]) + len(args[1]) + len(args[2]) + 3])
                    except:
                        if args[3] == "true" or args[3] == "false":
                            if args[3] == "true": args[3] = True
                            if args[3] == "false": args[3] = False
                        else:
                            args[3] = '"' + " ".join(args[3:]) + '"'
                    globals()[args[1]] = args[3]
                except Exception as err:
                    debug(err)
                    log("Something happened. Maybe check the syntax?")
        elif cmd == "unlet":
            if len(args) == 1:
                log("Please specify a variable name to remove.")
            else:
                if args[1] in globals():
                    del globals()[args[1]]
                    log("Removed variable.")
                else:
                    log("That variable does not exist.")
        elif cmd == 'ask':
            if len(args) == 1:
                log("Please specify some prompt text. The prompt answer will be stored in the 'answer' variable.")
            else:
                globals()['answer'] = input(substring)
        elif cmd == "vars":
            print("---Variables---")
            print("     ".join(globals()))
        elif cmd == "var":
            if len(args) == 1:
                log("Please specify a variable name to consult.")
            else:
                if args[1] in globals():
                    try:
                        log("[" + str(type(globals()[args[1]])) + "] " + str(globals()[args[1]]))
                    except Exception as ex:
                        debug(ex)
                        log("Something happened when viewing this variable. Use \"debug\" to see the error.")
                else:
                    log(f"That variable {Colors.red}does not{Colors.reset} exist. Maybe you've misspelled it.")
        elif cmd == "restart":
            log("Restarting PyTerm...")
            os.execv(sys.executable, ["python3"] + [installloc])
        elif cmd == "debug":
            if len(args) == 1:
                if debugging:
                    debugging = False
                    log("Debugging is now off.")
                    debug("If you can see this message, it means debugging didn't actually turn off.")
                else:
                    debugging = True
                    log("Debugging is now on.")
            else:
                if args[1] == 'off':
                    debugging = False
                    log("Debugging is now off.")
                    debug("If you can see this message, it means debugging didn't actually turn off.")
                else:
                    debugging = True
                    log("Debugging is now on.")
        elif cmd == "fetch":
            if len(args) == 1:
                log("Please specify a link to a file hosted online to fetch.")
            else:                    
                debug("Fetching file...")
                if args[1].startswith("http://"):
                    log("To fetch, you need a secure protocol connection.")
                    log("In short, fetch doesn't support http:// for security measures.")
                    debug("Failed to fetch file.")
                    return "false"
                else:
                    try:
                        if args[1].replace(' -s', '') == "versions":
                            with urllib.request.urlopen(versionsurl) as data:
                                content = data.read().decode('utf-8')
                                debug("Fetched.")
                                debug("Printing...")
                                globals()['fetched'] = content
                                if not args[len(args) - 1] == "-s":
                                    log("Data:")
                                    log(content)
                                else: 
                                    return content
                        elif args[1].replace(' -s', '') == "pyterm":
                            with urllib.request.urlopen(updateurl) as data:
                                content = data.read().decode('utf-8')
                                debug("Fetched.")
                                debug("Printing...")
                                globals()['fetched'] = content
                                if not args[len(args) - 1] == "-s":
                                    log("Data:")
                                    log(content)
                                else: 
                                    return content
                        else:
                            if substring.replace(' -s', '').startswith("https://"):
                                with urllib.request.urlopen(substring.replace(' -s', '')) as data:
                                    content = data.read().decode('utf-8')
                                    debug("Fetched.")
                                    debug("Printing...")
                                    globals()['fetched'] = content
                                    if not args[len(args) - 1] == "-s":
                                        log("Data:")
                                        log(content)
                                    else: 
                                        return content
                            else:
                                with urllib.request.urlopen("https://" + substring.replace(' -s', '')) as data:
                                    content = data.read().decode('utf-8')
                                    debug("Fetched.")
                                    debug("Printing...")
                                    globals()['fetched'] = content
                                    if not args[len(args) - 1] == "-s":
                                        log("Data:")
                                        log(content)
                                    else: 
                                        return content
                    except Exception as err:
                        debug(f"{Colors.red}Failed to fetch file.{Colors.reset}")
                        debug(err)
                        log(f"There was an {Colors.red}error{Colors.reset} when fetching the file. Maybe check the URL provided?")
        elif cmd == "echo":
            print(' '.join(args[1:]))
        elif cmd == "clear":
            if OS == "Windows":
                os.system('cls')
            else:
                os.system('clear')
        elif cmd == "clone":
            log("Cloning PyTerm...")
            existing = False
            if os.getcwd() == defaultdir:
                log("There is already a copy of PyTerm here!")
                existing = True
            onlyfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
            for file in onlyfiles:
                if file == filename:
                    log("There is already a copy of PyTerm here!")
                    existing = True
            if not existing:
                debug('Reading file...')
                with open(installloc, "r") as file:
                    content = file.read()
                debug(content)
                debug('Writing contents to new file...')
                with open(os.getcwd() + "/" + filename, "w") as f:
                    f.write(content)
        elif cmd == "run":
            if len(args) == 1:
                log("Please specify a PTP (PyTerm Program) file to run.")
            else:
                onlyptp = [f for f in os.listdir(defaultdir) if os.path.isfile(os.path.join(defaultdir, f))]
                def isptp(x):
                    return x.endswith('.ptp')
                onlyptp = filter(isptp, onlyptp)
                onlyptp = list(onlyptp)
                if substring in onlyptp:
                    run_prg(substring)
                elif f"{substring}.ptp" in onlyptp:
                    run_prg(substring + ".ptp")
                else:
                    log(f'{formatErrorCode('02')}')
        elif cmd == "dir":
            if len(args) == 1:
                onlyfiles = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and not f.endswith('.ptp')]
                onlyfolders = [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]
                onlyptp = [f for f in os.listdir(defaultdir) if os.path.isfile(os.path.join(defaultdir, f))]
                def isptp(x):
                    return x.endswith('.ptp')
                onlyptp = filter(isptp, onlyptp)
                onlyptp = list(onlyptp)
                if not len(onlyfiles) == 0:
                    print("~~~Files~~~")
                    print("    ".join(onlyfiles))
                if not len(onlyfolders) == 0:
                    print("~~~Folders~~~")
                    print("    ".join(onlyfolders))
                if not len(onlyptp) == 0:
                    print("~~~Programs~~~")
                    print("    ".join(onlyptp))
                if len(onlyfiles) == 0 and len(onlyfolders) == 0:
                    print("(Empty)")
            else:
                onlyfolders = [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]
                if substring in onlyfolders:
                    onlyfiles = [f for f in os.listdir(substring) if os.path.isfile(os.path.join(dir, f))]
                    onlyfolders = [f for f in os.listdir(substring) if os.path.isdir(os.path.join(dir, f))]
                    if not len(onlyfiles) == 0:
                        print("---Files---")
                        print("    ".join(onlyfiles))
                    if not len(onlyfolders) == 0:
                        print("~~~Folders~~~")
                        print("    ".join(onlyfolders))
                    if len(onlyfiles) == 0 and len(onlyfolders) == 0:
                       print("(Empty)")
                else:
                    log(f'{formatErrorCode('02.5')}')
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
                        os.chdir('..')
                        dir = os.getcwd()
                    else:
                        if substring == "/":
                            os.chdir(os.getcwd() + "/" + substring)
                        else:
                            onlyfolders = [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]
                            targetdir = os.getcwd() + "/" + substring
                            if substring in onlyfolders:
                                os.chdir(targetdir)
                                dir = os.getcwd()
                            else:
                                try:
                                    os.chdir(targetdir)
                                    dir = os.getcwd()
                                except Exception as e:
                                    log(f'{formatErrorCode('02.5')}')
                                    debug(e)
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
                    log(f'{formatErrorCode('02')}')
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
                    log(f'{formatErrorCode('02')}')
        elif cmd == "create":
            if len(args) == 1:
                log("Please specify a file name to make a text file of.")
            else:
                if args[1] == "-f":
                    if os.access(dir, os.W_OK):
                        with open(args[3] + ".txt", "w") as f:
                            f.write(execute("fetch " + args[2] + " -s"))
                    else:
                        log("Cannot create file on a read-only directory.")
                else:
                    if args[1] + ".txt" in os.listdir():
                        log("You can't create a file with an existing file name! Use \"write\" to edit that file!")
                    else:
                        if os.access(dir, os.W_OK):
                            with open(args[1] + ".txt", "w") as f:
                                f.write("")
                        else:
                            log("Cannot create file on a read-only directory.")
        elif cmd == "rename":
            if len(args) < 3:
                log("Please specify a file to rename and what you'll rename it to. Syntax: rename (file name) (file name to rename to)")
            else:
                os.rename(args[1], args[2])
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
                        if substring in onlyfolders:
                            log("Folder already exists")
                        else:
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
                    onlyfolders = [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]
                    if substring in onlyfolders:
                        if os.access(dir, os.W_OK):
                            os.rmdir(substring)
                        else:
                            log("Cannot delete directory on a read-only directory.")
                    else:
                        log(f'{formatErrorCode('02.5')}')
        elif cmd == "write":
            if len(args) < 3:
                log(f"Please specify a file and contents to write to. Usage: {Colors.blue}{Colors.bold}write <file> <contents, can have spaces>{Colors.reset}")
            else:
                if args[1] == os.path.basename(__file__):
                    log("Cannot overwrite self!")
                else:
                    if os.access(dir, os.W_OK):
                        try:
                            with open(args[1], "w") as f:
                                f.write(prompt[len(args[0]) + len(args[1]) + 2:])
                        except:
                            log("Couldn't write to file.")
                    else:
                        log("Cannot write to file on a read-only directory!")
        elif cmd == "append":
            if len(args) < 3:
                log(f"Please specify a file name and contents to append to the desired file. Usage: {Colors.bold}{Colors.blue}append {Colors.yellow}<file> <content, can have spaces>{Colors.reset}")
            else:
                if args[1] == os.path.basename(__file__):
                    log("Cannot append to self!")
                else:
                    if os.access(dir, os.W_OK):
                        try:
                            with open(args[1], "a") as f:
                                f.write(prompt[len(args[0]) + len(args[1]) + 2:])
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
                            log(f'{formatErrorCode('02')}')
                    else:
                        log("Cannot delete file on a read-only directory")
    elif cmd not in cmds and not skipping:
        onlyptp = [f for f in os.listdir(defaultdir) if os.path.isfile(os.path.join(defaultdir, f))]
        def isptp(x):
            return x.endswith('.ptp')
        onlyptp = filter(isptp, onlyptp)
        onlyptp = list(onlyptp)
        for i in range(len(onlyptp)):
            onlyptp[i] = onlyptp[i][:len(onlyptp[i]) - 4]
        if cmd == "cd..":
            os.chdir('..')
            dir = os.getcwd()
        elif cmd == "cd;":
            os.chdir(defaultdir)
            dir = os.getcwd()
        elif cmd == "@echo":
            if len(args) > 1:
                if args[1] == "off":
                    log("Command echo is now off.")
                    echo = False
                elif args[1] == "on":
                    echo = True
                    log("Command echo is now on.")
        elif cmd == "-@echo":
            if len(args) > 1:
                if args[1] == "off":
                    echo = False
                elif args[1] == "on":
                    echo = True
        elif cmd == "":
            print(f"",end="")
        elif cmd in onlyptp:
            run_prg(cmd + ".ptp")
        elif cmd[:4] in onlyptp:
            run_prg(cmd)
        else:
            log(f"The command {Colors.blue}{Colors.bold}{cmd}{Colors.reset} does not exist, or is not a valid PyTerm Program file. Use {Colors.bold}{Colors.blue}help{Colors.reset} to get a list of commands.")
    if cmd != "skip": skipping = False
finishedrunning = True
execs = 0
def run_prg(file):
    global finishedrunning
    global echo
    global execs
    if not finishedrunning:
        execs += 1
    if execs < 21:
        with open(file, "r") as ptp:
            content = ptp.read()
        cmds = content.split('\n')
        finishedrunning = False
        execute('let __filename = ' + file)
        for cmd in cmds:
            if not finishedrunning:
                if cmd == "exit":
                    finishedrunning = true
                else:
                    execute(cmd)
        finishedrunning = True
        if echo == False:
            echo = True
    else:
        execute("echo Program exited because of infinite loop.")
onlyfiles = [f for f in os.listdir(defaultdir) if os.path.isfile(os.path.join(defaultdir, f))]
if 'startup.ptp' in onlyfiles:
    run_prg(defaultdir + '/startup.ptp')
while True:
    if echo:
        prompt = input(dir + "> ")
    else:
        prompt = input("")
    execute(prompt)
