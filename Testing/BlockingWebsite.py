#Import labraries
import ctypes, sys
import time
from datetime import datetime as dt
#Windows host file path
hostsPath = r"C:\Windows\System32\drivers\etc\hosts"
redirect = "127.0.0.1"
#Add the website you want to block, in this list
websites = ["www.facebook.com"]

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    while True:
        #Durtion during which, website blocker will work
        if dt(dt.now().year,dt.now().month,dt.now().day,9) < dt(dt.now().year,dt.now().month,dt.now().day,18):
            with open(hostsPath,"r+") as file:
                content = file.read()
                for site in websites:
                    if site in content:
                        pass
                    else:
                        file.write(redirect +" " +site+ "\n")
            print("Temporarily Denied")

        else:
            with open(hostsPath, 'r+') as file:
                content = file.readlines()
                file.seek(0)
                for line in content:
                    if not any(site in line for site in websites):
                        file.write(line)
                    file.truncate()
            print("Allow Access")
    time.sleep(5)
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
