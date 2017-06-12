import subprocess as sp
import os
import time
from winreg import *
from tkinter import *
from tkinter.ttk import *

class WindowsPloneInstaller:

    def __init__(self):
        try:
            self.base_path = sys._MEIPASS  # PyInstaller creates a temp folder and stores path in _MEIPASS environment variable
        except Exception:
            self.base_path = os.path.abspath(".")

        self.plone_key = r'SOFTWARE\PloneInstaller' #our Windows registry key under HKEY_CURRENT_USER
        self.run_once_key = r'Software\Microsoft\Windows\CurrentVersion\RunOnce'

        self.installer_path = os.path.realpath(__file__).split(".")[0]+".exe"
        self.log_file = os.path.dirname(self.installer_path) + "\install.log"

        self.required_build = 15063

        try: #Grab installation state from registry if it exists
            k = OpenKey(HKEY_CURRENT_USER, self.plone_key, 0, KEY_ALL_ACCESS)
            self.install_status = QueryValueEx(k, "install_status")[0]

        except: #Otherwise create it with ititial "begin" value
            k = CreateKey(HKEY_CURRENT_USER, self.plone_key)
            self.install_status = "begin"
            SetValueEx(k, "install_status", 1, REG_SZ, self.install_status)

        SetValueEx(k, "base_path", 1,REG_SZ, self.base_path) #This ensures powershell and bash can find this path.
        SetValueEx(k, "installer_path", 1, REG_SZ, os.path.dirname(self.installer_path))
        CloseKey(k)

        self.last_status = self.install_status
        self.init_GUI()

    def killapp(self, event):
        sys.exit(0)

    def init_GUI(self):
        self.gui = Tk()
        self.gui.title("Windows Plone Installer")
        window_width = 500
        window_height = 275
        self.fr1 = Frame(self.gui, width=window_width, height=window_height)
        self.fr1.pack(side="top")

        self.log_text = Text(self.fr1, borderwidth=3, relief="sunken",spacing1=1, height=8, width=50, bg="black", fg="white")
        self.log_text.config(font=("consolas", 12), undo=True, wrap='word')
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

        scrollb = Scrollbar(self.fr1, command=self.log_text.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.log_text['yscrollcommand'] = scrollb.set

        self.log("Initializing installer.")
        self.log("Welcome to Plone Installer for Windows.")

        if self.install_status == "wsl_enabled":
            self.log("Picking up where we left off. Installing Linux Subsystem...")
            self.run_PS("installWSL.ps1") #Install Ubuntu on Windows
            self.wait_for_status_change(5000) # Not sure how long this takes

            if self.install_status == "wsl_installed":
                self.install_on_wsl()

            else:
                self.catch()

        elif self.install_status == "begin":
            self.run_PS("getWinInfo.ps1")
            self.wait_for_status_change(10)

            if self.install_status == "got_win_info":
                k = OpenKey(HKEY_CURRENT_USER, self.plone_key)
                
                env_build = int(str(QueryValueEx(k, "win_version")).split('.')[2].split("'")[0]) #this feels 'rigged.' Moved it to PowerShell because it's much more reliable, however.

                if env_build >= self.required_build:
                    self.install_type = IntVar(value=1)
                    Checkbutton(self.fr1, text="Install using Ubuntu for Windows (recommended)", variable=self.install_type).grid(row=1,sticky="NW")
                else:
                    self.install_type = IntVar(value=0)
                    self.log("You do not have a new enough version of Windows to install with Ubuntu for Windows.\n Please install Creator's Update or newer to use Ubuntu.\nOr press OK to install using standard buildout.")

        #else:
            # This shouldn't really happen.
            # Is another instance of the installer already running? Should we start installion over?

        self.okaybutton = Button(self.fr1, text="Okay")
        self.okaybutton.grid(row=2, sticky="WE")
        self.okaybutton.bind("<Button>", self.init_install)

        cancelbutton = Button(self.fr1, text="Cancel")
        cancelbutton.grid(row=3, sticky="WE")
        cancelbutton.bind("<Button>", self.killapp)
        self.fin = ''

        ws = self.gui.winfo_screenwidth()
        hs = self.gui.winfo_screenheight()
        x = (ws/2) - (window_width/2)
        y = (hs/2) - (window_height/2)
        self.gui.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

        self.gui.mainloop()
        
    def init_install(self, event):

        self.okaybutton.configure(state="disabled")

        if self.install_type.get(): #if this is true, this machine has proper version for WSL route
            self.log('Checking for Linux Subsystem')
            SetValueEx(HKEY_CURRENT_USER, self.run_once_key, 0, REG_SZ, self.installer_path) #Set Win Registry to load our installer after the next restart
            self.run_PS("enableWSL.ps1") #Make sure WSL is enabled and check if it is already installed
            self.wait_for_status_change(15)

            if self.install_status == "wsl_enabled":
                self.log('Linux Subsystem enabled. Must restart to install it!')

            elif self.install_status == "wsl_installed":
                self.log('Linux Subsystem already installed, installing Plone')
                self.install_on_wsl()

            else:
                catch()

        else: #either this machine isn't high enough version,or user has selected standard buildout route manually.
            self.log('Installing Chocolatey package manager')
            self.run_PS("installChoco.ps1") #Chocolatey will allow us to grab dependencies.
            self.wait_for_status_change(90)

            if self.install_status == "choco_installed":
                self.log('Chocolatey Installed')
                self.log('Installing Plone Dependencies using Chocolatey')
                self.run_PS("installPloneBuildout.ps1")  #Run the regular Plone buildout script for users who are not using Ubuntu/Bash

                self.wait_for_status_change(300)

                if self.install_status == "dependencies_installed":
                    self.log("Dependencies installed.")
                    self.log("Preparing virtualenv and gathering Plone buildout from GitHub.")
                    self.wait_for_status_change(500)

                    if self.install_status == "starting_buildout":
                        self.log("Running buildout, this may take a while...")

                        self.wait_for_status_change(5000) #Not sure how long this takes

                        if self.install_status == "complete":
                            log("Plone installed successfully!")
                            self.clean_up()
                        else:
                            self.catch()
                    else:
                        self.catch()
                else:
                    self.catch()
            else:
                self.catch()

    def install_on_wsl(self):
        self.run_PS("installPlone.ps1") #Install Plone on the new instance of WSL
        self.wait_for_status_change(150) # Not sure how long this takes

        if self.install_status == "complete":
            log("Plone installed successfully on Linux subsystem!")
            self.clean_up()
        else:
            catch()

    def run_PS(self, script_name):
        script_path = self.base_path+"\\PS\\"+script_name
        self.log("Calling " + script_name + " in Microsoft PowerShell, please accept any prompts.")
        #sp.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", ". " + script_path, "-ExecutionPolicy", "Unrestricted", "-windowstyle", "hidden;"]) #these -options aren't actually working.
        sp.run(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", ". " + script_path, "-ExecutionPolicy", "Unrestricted", "-windowstyle", "hidden"])

    def wait_for_status_change(self, timeout): #add a timeout here in case, for example, powershell crashes before updating status
        k = OpenKey(HKEY_CURRENT_USER, self.plone_key, 0, KEY_ALL_ACCESS)
        count = 0
        while self.install_status == self.last_status:
            time.sleep(2) #to prevent this from overkill
            self.install_status = QueryValueEx(k, "install_status")[0]
            count += 1
            if count == timeout:
                self.install_status = "timed_out"
                break
        self.last_status = self.install_status
        CloseKey(k)
        return

    def catch(self):
        if self.install_status == "timed_out":
                print("Installer process timed out!")

    def log(self, message):
        with open(self.log_file, "a") as log:
            log.write(message+"\n")
        self.log_text.config(state="normal")
        self.log_text.insert(END, "> " + message + '\n')
        self.log_text.config(state="disabled")
        self.log_text.see(END)

    def clean_up(self):
        k = OpenKey(HKEY_CURRENT_USER, self.plone_key, 0, KEY_ALL_ACCESS)
        DeleteKey(k, "install_status")
        DeleteKey(k, "base_path")
        DeleteKey(k, "installer_path")
        DeleteKey(k, "win_version")
        CloseKey(k)
        DeleteKey(HKEY_CURRENT_USER, self.plone_key)

if __name__ == "__main__":
    try:
        app = WindowsPloneInstaller()
    except KeyboardInterrupt:
        raise SystemExit("Aborted by user request.")