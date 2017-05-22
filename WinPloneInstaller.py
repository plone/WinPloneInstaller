import subprocess as sp
import os
import win32api
from winreg import *

try:
    from tkinter import *
    from tkinter.ttk import *
except ImportError:
    from Tkinter import *
    from ttk import *

class WindowsPloneInstaller:

    def __init__(self):
        try:
            self.base_path = sys._MEIPASS  # PyInstaller creates a temp folder and stores path in _MEIPASS environment variable
        except Exception:
            self.base_path = os.path.abspath(".")

        #self.powershell_windowstyle = "normal"

        self.ploneKey = r'SOFTWARE\Plone' #our Windows registry key under HKEY_CURRENT_USER

        try: #Grab installation state from registry if it exists
            k = OpenKey(HKEY_CURRENT_USER, self.ploneKey)
            self.installStatus = QueryValueEx(k, "install_status")[0]

        except: #otherwise create it with "begin" status and initialize
            k = CreateKey(HKEY_CURRENT_USER, self.ploneKey)
            self.installStatus = "begin"
            SetValueEx(k, "install_status", 0, REG_SZ, self.installStatus)
            
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

        if self.installStatus == "wsl_enabled":
            l = Label(self.fr2, text="Picking up where we left off.")
            l.grid(sticky="NW")
            self.continueInstall()

        elif self.installStatus == "begin":
            requiredBuildNumber = 15063
            envWinBuildNumber = win32api.GetVersionEx()[2]

            if envWinBuildNumber >= requiredBuildNumber:
                self.install_type = IntVar(value=1)
                checkbox = Checkbutton(self.fr2, text="Install using Ubuntu for Windows (recommended)", variable=self.install_type)
                checkbox.grid(sticky="NW")
            else:
                self.install_type = IntVar(value=0)
                l = Label(self.fr2, text="You do not have a new enough version of Windows to install with Ubuntu for Windows.\n Please install Creator's Update or newer to use Ubuntu.\nOr press OK to install using standard buildout.")
                l.grid(sticky="NW")

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
            self.runPS("./PS/enableWSL.ps1") #Enable WSL and restart the machine.
            self.waitForStatusChange()

            if self.installStatus == "wsl_enabled":
                runOnceKey = r'Software\Microsoft\Windows\CurrentVersion\RunOnce'
                installerPath = os.path.realpath(__file__).split(".")[0]+".exe"
                SetValue(HKEY_CURRENT_USER, runOnceKey, REG_SZ,installerPath) #Set Win Registry to load our installer after the next restart

                win32api.InitiateSystemShutdown()
            elif self.installStatus == "wsl_installed":
                self.continueInstall()

        else: #either this machine isn't high enough version,or user has selected standard buildout route manually.
            self.runPS("./PS/installChoco.ps1") #Chocolatey will allow us to grab dependencies.
            self.waitForStatusChange()

            if self.installStatus == "choco_installed":
                self.runPS("./PS/installPloneBuildout.ps1")  #Run the regular Plone buildout script for users who are not using Ubuntu/Bash
    
    def continueInstall(self):
        self.runPS("./PS/installPlone.ps1") #Install Ubuntu on Windows

    def runPS(self, scriptName):
        scriptPath = self.base_path + scriptName
        sp.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", ". "+scriptPath+" -ExecutionPolicy Unrestricted;"])

    def waitForStatusChange(self):
        oldStatus = self.installStatus
        k = OpenKey(HKEY_CURRENT_USER, self.ploneKey)
        while self.installStatus == oldStatus:
            time.sleep(1) #to prevent this from overkill
            self.installStatus = QueryValueEx(k, "install_status")[0]
        return

if __name__ == "__main__":
    try:
        app = WindowsPloneInstaller()
    except KeyboardInterrupt:
        raise SystemExit("Aborted by user request.")