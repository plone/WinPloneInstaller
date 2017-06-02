import subprocess as sp
import os
# import win32api
# import platform
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

        self.ploneKey = r'SOFTWARE\Plone' #our Windows registry key under HKEY_CURRENT_USER

        try: #Grab installation state from registry if it exists
            k = OpenKey(HKEY_CURRENT_USER, self.ploneKey)
            self.install_status = QueryValueEx(k, "install_status")[0]

        except: #Otherwise create it with ititial "begin" value
            k = CreateKey(HKEY_CURRENT_USER, self.ploneKey)
            self.install_status = "begin"
            SetValueEx(k, "install_status", 0, REG_SZ, self.install_status)

        SetValueEx(k, "base_path", 0,REG_SZ, self.base_path) #This ensures powershell and bash can find this path.

        self.lastStatus = self.install_status
        self.initGUI()

    def killapp(self, event):
        sys.exit(0)

    def initGUI(self):
        self.root = Tk()
        self.root.title("Windows Plone Installer")
        self.fr1 = Frame(self.root, width=300, height=100)
        self.fr1.pack(side="top")

        self.fr2 = Frame(self.root, width=300, height=300,
                    borderwidth=2, relief="ridge")
        self.fr2.pack(ipadx=10, ipady=10)
        self.fr4 = Frame(self.root, width=300, height=100)
        self.fr4.pack(side="bottom", pady=10)

        self.statusText = StringVar()
        self.statusText.set('Welcome to Plone Installer for Windows.')
        statusLabel = Label(self.fr2, textvariable=self.statusText)
        statusLabel.grid(sticky="NW")

        if self.install_status == "wsl_enabled":
            statusText.set('Picking up where we left off. Installing Linux Subsystem...')
            self.runPS("./PS/installWSL.ps1") #Install Ubuntu on Windows

        elif self.install_status == "begin":
            requiredBuildNumber = 15063
            self.runPS("./PS/getWinInfo.ps1")
            self.waitForStatusChange()

            if self.install_status == "got_win_info":
                k = OpenKey(HKEY_CURRENT_USER, self.ploneKey)
                
                envWinBuildNumber = int(str(QueryValueEx(k, "win_version")).split('.')[2])

                if envWinBuildNumber >= requiredBuildNumber:
                    self.install_type = IntVar(value=1)
                    checkbox = Checkbutton(self.fr2, text="Install using Ubuntu for Windows (recommended)", variable=self.install_type)
                    checkbox.grid(sticky="NW")
                else:
                    self.install_type = IntVar(value=0)
                    self.statusText.set("You do not have a new enough version of Windows to install with Ubuntu for Windows.\n Please install Creator's Update or newer to use Ubuntu.\nOr press OK to install using standard buildout.")

        #else:
            # This shouldn't really happen.
            # Is another instance of the installer already running? Should we start installion over?

        okaybutton = Button(self.fr4, text="Okay   ")
        okaybutton.bind("<Button>", self.initInstall)
        okaybutton.pack(side="left")

        cancelbutton = Button(self.fr4, text="Cancel")
        cancelbutton.bind("<Button>", self.killapp)
        cancelbutton.pack(side="right")
        self.fin = ''

        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (400/2)
        y = (hs/2) - (250/2)
        self.root.geometry('%dx%d+%d+%d' % (400, 250, x, y))

        self.root.mainloop()
        
    def initInstall(self, event):

        if self.install_type.get(): #if this is true, this machine has proper version for WSL route
            self.statusText.set('Checking for Linux Subsystem')
            self.runPS("./PS/enableWSL.ps1") #Make sure WSL is enabled and check if it is already installed
            runOnceKey = r'Software\Microsoft\Windows\CurrentVersion\RunOnce'
            installerPath = os.path.realpath(__file__).split(".")[0]+".exe"
            SetValue(HKEY_CURRENT_USER, runOnceKey, REG_SZ,installerPath) #Set Win Registry to load our installer after the next restart
            self.waitForStatusChange()

            if self.install_status == "wsl_enabled":
                self.statusText.set('Linux Subsystem enabled. Must restart to install it...')
                # self.performRestart()

            elif self.install_status == "wsl_installed":
                self.statusText.set('Linux Subsystem already installed, installing Plone')
                self.runPS("./PS/installPlone.ps1") #User already had WSL installed, Install Plone on existing subsystem.

            #else: problem occured

        else: #either this machine isn't high enough version,or user has selected standard buildout route manually.
            self.statusText.set('Installing Chocolatey package manager')
            self.runPS("./PS/installChoco.ps1") #Chocolatey will allow us to grab dependencies.
            self.waitForStatusChange()

            if self.install_status == "choco_installed":
                self.statusText.set('Chocolatey Installed...')
                self.runPS("./PS/installPloneBuildout.ps1")  #Run the regular Plone buildout script for users who are not using Ubuntu/Bash

                self.waitForStatusChange()

            #else: problem occured

    def runPS(self, scriptName):
        scriptPath = self.base_path + scriptName
        sp.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", ". "+scriptPath+" -ExecutionPolicy Unrestricted -windowstyle hidden;"])

    def waitForStatusChange(self): #add a timeout here in case, for example, powershell crashes before updating status
        k = OpenKey(HKEY_CURRENT_USER, self.ploneKey)
        while self.install_status == self.lastStatus:
            time.sleep(2) #to prevent this from overkill
            self.install_status = QueryValueEx(k, "install_status")[0]
        self.lastStatus = self.install_status
        return

    # def performRestart(self):
        # runOnceKey = r'Software\Microsoft\Windows\CurrentVersion\RunOnce'
        # installerPath = os.path.realpath(__file__).split(".")[0]+".exe"
        # SetValue(HKEY_CURRENT_USER, runOnceKey, REG_SZ,installerPath) #Set Win Registry to load our installer after the next restart

        # win32api.InitiateSystemShutdown()

if __name__ == "__main__":
    try:
        app = WindowsPloneInstaller()
    except KeyboardInterrupt:
        raise SystemExit("Aborted by user request.")