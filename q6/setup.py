# this gonna end up on r/programmerhorror

# imports
import os, sys, datetime, shutil

def get_timestamp():
    return datetime.datetime.now().strftime("%d %b %Y %H:%M:%S")

def parse_flag(flag: str):
    if not flag.startswith("-"):
        sys.stderr.write("Invalid flag: Flag must start with -")
        exit(1)
    else:
        kwargs = set(["i", "v", "l"])

        if flag.find("v") != -1 and flag.find("i") != -1:
            sys.stderr.write("Invalid flag: Choose verify or install process not both")
            exit(1)
            
        if flag.count("v") > 1 or flag.count("i") > 1 or flag.count("l") > 1:
            sys.stderr.write("Invalid flag: Each character must be unique")
            exit(1)

        if flag[1:] == "l":
            sys.stderr.write("Invalid flag: Log can only run with install or verify")
            exit(1)

        if len(set(flag[1:]).difference(kwargs)) != 0:
            sys.stderr.write("Invalid flag: Character must be combination of 'v' or 'i' and 'l'")
            exit(1)

        return str(flag[1:])
    
def compare_files(file1, file2) -> bool:
    f1 = open(file1, "r")
    f2 = open(file2, "r")

    line1 = f1.readline()
    line2 = f2.readline()

    while line1:
        while line2:
            if line1 != line2:
                return False

            line2 = f2.readline()
        line1 = f1.readline()
    
    return True

def logging(logs: list) -> None:
    '''
    Logging function uses a list of strings to write previous output into a
    log file.
    Parameters:
        logs: list, output from verification/installation in the form of list of 
                    strings to write to logging file.
    '''
    current_date = datetime.datetime.now().strftime("%Y-%b-%d")
    current_time = datetime.datetime.now().strftime("%H_%M_%S")

    if not os.path.exists(f"/home/logs/{current_date}"):
        os.mkdir(f"/home/logs/{current_date}")

    with open(f"/home/logs/{current_date}/{current_time}.txt", "w+") as f:
        i = 0
        while i < len(logs):
            f.write(f"{logs[i]}\n")
            i += 1

def verification(master: str, timestamp: str, log_enabled: int) -> list:
    '''
    Verification makes sure all files and directories listed in the config file
    are present and match the contents of the master files. 
    Parameters:
        master:    str,  a string representing the absolute path to the master directory.
        timestamp: str,  a string representing the time to insert into the output.
    Returns:
        output:    list, a list of strings generated from the verification process.
    '''
    log_strings = []
    dirs = []
    files = []
    filenames = []
    master_files = []

    config_path = master + "config.txt"

    log_strings.append(f"{timestamp} Start verification process.")

    with open(config_path, "r") as f:
        line = f.readline().rstrip()
        while line:
            if line.startswith("/") and line.endswith("/"):
                path = str(line)
                dirs.append(os.path.abspath(path))
            if line.startswith("./"):
                files.append(os.path.abspath(path + line[2:]))
                filenames.append(line[2:])
            
            line = f.readline().rstrip()

    contents = tuple(os.walk(os.path.abspath(master)))
    i = 0
    while i < len(contents):
        j = 0
        while j < len(contents[i][2]):
            fp = os.path.abspath(f"{contents[i][0]}/{contents[i][2][j]}")
            master_files.append(fp)
            if log_enabled == 1:
                log_strings.append(f"Found: {fp}")
            j += 1
        i += 1

    log_strings.append(f"{timestamp} Extracting paths in configuration file.")
    log_strings.append(f"Total directories to check: {len(dirs)}")

    log_strings.append(f"{timestamp} Checking if directories exists.")

    i = 0
    while i < len(dirs):
        if os.path.exists(os.path.abspath(dirs[i])):
            log_strings.append(f"{os.path.abspath(dirs[i])} is found!")
        else:
            log_strings.append(f"{os.path.abspath(dirs[i])} NOT found!")
            log_strings.append(f"\nAbnormalities detected...")
            return log_strings
        i += 1

    log_strings.append(f"{timestamp} Extracting files in configuration file.")
    i = 0
    while i < len(files):
        log_strings.append(f"Files to check: {files[i]}")
        i += 1
    log_strings.append(f"Total files to check: {len(files)}")

    log_strings.append(f"{timestamp} Checking if files exists.")

    i = 0
    while i < len(files):
        if os.path.exists(os.path.abspath(files[i])):
            log_strings.append(f"{os.path.abspath(files[i])} found!")
        else:
            log_strings.append(f"{os.path.abspath(files[i])} NOT found!")
            log_strings.append(f"\nAbnormalities detected...")
            return log_strings
        i += 1

    log_strings.append(f"{timestamp} Check contents with master copy.")
    i = 0
    while i < len(filenames):
        j = 0
        k = 0
        while j < len(master_files):
            if master_files[j].find(filenames[i]) != -1:
                src_path = master_files[j]
            j += 1

        while k < len(files):
            if files[k].find(filenames[i]) != -1:
                dest_path = files[k]
            k += 1

        if compare_files(src_path, dest_path):
            log_strings.append(f"{dest_path} is the same as {src_path}: True")
        else:
            log_strings.append(f"{dest_path} is the same as {src_path}: False")
            log_strings.append(f"\nAbnormalities detected...")
            return log_strings

        i += 1

        log_strings.append(f"\n{timestamp} Verification complete.")
    
    return log_strings


def installation(master: str, timestamp: str, log_enabled: int) -> list:
    '''
    Installation copies all required master files into the addresses listed by
    the config file.
    Parameters:
        master:    str,  a string representing the absolute path to the master directory.
        timestamp: str,  a string representing the time to insert into the output.
    Returns:
        output:    list, a list of strings generated from the installation process.
    '''
    config_path = master + "config.txt"
    path = ""
    files = []
    filenames = []
    dirs = []
    log_strings = []
    master_files = []

    log_strings.append(f"{timestamp} Start installation process.")

    with open(config_path, "r") as f:
        line = f.readline().rstrip()
        while line:
            if line.startswith("/") and line.endswith("/"):
                path = str(line)
                dirs.append(os.path.abspath(path))
            if line.startswith("./"):
                files.append(os.path.abspath(path + line[2:]))
                filenames.append(line[2:])
            
            line = f.readline().rstrip()

    log_strings.append(f"{timestamp} Extracting paths in configuration file.")
    if log_enabled == 1:
        log_strings.append(f"Total directories to create: {len(dirs)}")

    log_strings.append(f"{timestamp} Create new directories.")

    i = 0
    while i < len(dirs):
        if not os.path.exists(os.path.abspath(dirs[i])):
            os.makedirs(os.path.abspath(dirs[i]))
            if log_enabled == 1:
                log_strings.append(f"{os.path.abspath(dirs[i])} is created successfully.")
        else:
            if log_enabled == 1:
                log_strings.append(f"{os.path.abspath(dirs[i])} exists. Skip directory creation.")
        i += 1

    log_strings.append(f"{timestamp} Extracting paths of all files in {master}.")
    contents = tuple(os.walk(os.path.abspath(master)))
    i = 0
    while i < len(contents):
        j = 0
        while j < len(contents[i][2]):
            fp = os.path.abspath(f"{contents[i][0]}/{contents[i][2][j]}")
            master_files.append(fp)
            if log_enabled == 1:
                log_strings.append(f"Found: {fp}")
            j += 1
        i += 1

    log_strings.append(f"{timestamp} Create new files.")
    i = 0
    while i < len(files):
        if log_enabled == 1:
            log_strings.append(f"Creating file: {files[i]}")
        f = open(files[i], "w+")
        f.close()
        i += 1

    log_strings.append(f"{timestamp} Copying files.")
    i = 0
    while i < len(filenames):
        j = 0
        k = 0
        while j < len(master_files):
            if master_files[j].find(filenames[i]) != -1:
                src_path = master_files[j]
            j += 1

        while k < len(files):
            if files[k].find(filenames[i]) != -1:
                dest_path = files[k]
            k += 1

        try:
            shutil.copyfile(src_path, dest_path)
        except FileNotFoundError:
            return log_strings

        if log_enabled == 1:
            log_strings.append(f"Locating: {filenames[i]}")
            log_strings.append(f"Original path: {os.path.abspath(src_path)}")
            log_strings.append(f"Destination path: {os.path.abspath(dest_path)}")
        i += 1

    log_strings.append(f"\n{timestamp} Installation complete.")

    return log_strings


def main(master: str, flag: str, timestamp: str):
    '''
    Ideally, all your print statements would be in this function. However, this is
    not a requirement.
    Parameters:
        master:    str, a string representing the absolute path to the master directory.
        flag:      str, a string representing the specified flags, if no flag is given
                        through the command line, flags will be an empty string.
        timestamp: str, a string representing the time to insert into the output.
                    in the format: DD MMM YYYY HH:MM:DD , ex: 10 Apr 2023 12:44:17
    '''
    log_enabled = 0

    if flag == "":
        log_enabled = 1
    else:
        if flag.find("l") != -1:
            log_enabled = 1

    if flag.find("i") != -1 or flag == "":
        log = installation(master, timestamp, log_enabled)
        print(*log, sep = "\n")
        if log_enabled == 1:
            logging(log)
        return
    
    if flag.find("v") != -1:
        log = verification(master, timestamp, log_enabled)
        print(*log, sep = "\n")
        if log_enabled == 1:
            logging(log)
        return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Insufficient arguments")
        exit(1)
    
    if not sys.argv[1].startswith("/") or not sys.argv[1].endswith("/"):
        sys.stderr.write("Invalid master path")
        exit(1)
    
    master = str(sys.argv[1])

    if len(sys.argv) == 2:
        flag = ""
    else:
        flag = parse_flag(sys.argv[2])

    timestamp = get_timestamp()

    # you will need to pass in some arguments here
    # we will leave this empty for you to handle the implementation
    main(master, flag, timestamp)