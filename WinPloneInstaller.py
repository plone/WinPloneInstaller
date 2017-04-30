import subprocess as sp
import os
import platform
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
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            self.base_path = sys._MEIPASS
        except Exception:
            self.base_path = os.path.abspath(".")

        #self.powershell_windowstyle = "normal"

        self.ploneKey = r'SOFTWARE\PLONE'
        try: #Check if key exists, initialize with it's value if so.
            k = OpenKey(HKEY_CURRENT_USER, self.ploneKey)
            installStatus = QueryValueEx(k, "install_status")[0]
            self.initGUI(installStatus)

        except: #otherwise create it with "begin" status and initialize
            k = CreateKey(HKEY_CURRENT_USER, self.ploneKey)
            installStatus = "begin"
            SetValueEx(k, "install_status", 0, REG_SZ, installStatus)
            self.initGUI(installStatus)

    def killapp(self, event):
        sys.exit(0)

    def GetFile(self, event):
        self.fin = filedialog.askopenfilename()
        self.filein.delete(0, 'end')
        self.filein.insert(0, self.fin)

    def initGUI(self, status):
        self.root = Tk()
        self.root.title("Windows Plone Installer")
        fr1 = Frame(self.root, width=300, height=100)
        fr1.pack(side="top")

        fr2 = Frame(self.root, width=300, height=300,
                    borderwidth=2, relief="ridge")
        fr2.pack(ipadx=10, ipady=10)
        fr4 = Frame(self.root, width=300, height=100)
        fr4.pack(side="bottom", pady=10)

        if status == "wsl_enabled":
            l = Label(fr2, text="Picking up where we left off.")
            l.grid(sticky="NW")

        elif status == "begin":
            requiredBuildNumber = 15063
            envWinBuildNumber = int(platform.platform().split('.')[2].split('-')[0])

            if envWinBuildNumber >= requiredBuildNumber:
                self.install_type = IntVar(value=1)
                checkbox = Checkbutton(fr2, text="Install using Ubuntu for Windows (recommended)", variable=self.install_type)
                checkbox.grid(sticky="NW")
            else:
                self.install_type = IntVar(value=0)
                l = Label(fr2, text="You do not have a new enough version of Windows to install with Ubuntu for Windows.\n Please install Creator's Update or newer to use Ubuntu.\nOr press OK to install using standard buildout.")
                l.grid(sticky="NW")

            okaybutton = Button(fr4, text="Okay   ")
            okaybutton.bind("<Button>", self.initInstall)
            okaybutton.pack(side="left")

            cancelbutton = Button(fr4, text="Cancel")
            cancelbutton.bind("<Button>", self.killapp)
            cancelbutton.pack(side="right")
            self.fin = ''

        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (400/2)
        y = (hs/2) - (250/2)
        self.root.geometry('%dx%d+%d+%d' % (400, 250, x, y))

        self.root.mainloop()

        if status == "wsl_enabled":
            self.continueInstall(self)
        
    def initInstall(self, event):

        #Install Chocolatey for every user
        self.runPS("./PS/installChoco.ps1")

        self.waitFor("choco_installed")

        if self.install_type.get():
            #Enable WSL for user's who are willing and able to install using Ubuntu/Bash
            rc = self.runPS("./PS/enableWSL.ps1")

            self.waitFor("wsl_enabled")

            #Set Win Registry to load our installer after the next restart
            runOnceKey = r'Software\Microsoft\Windows\CurrentVersion\RunOnce'
            installerPath = os.path.realpath(__file__).split(".")[0]+".exe" #This gets a .py rather than .exe
            SetValue(HKEY_CURRENT_USER, runOnceKey, REG_SZ,installerPath)

            #User must restart here.

        else:
            #Grab dependencies with Choco
            rc = self.runPS("./PS/chocoBuildout.ps1")

            self.waitFor("dependencies_installed")

            #Run the regular Plone buildout script for users who are not using Ubuntu/Bash
            rc = self.runPS("./PS/installPloneBuildout.ps1")
    
    def continueInstall(self):
        #Install Ubuntu on Windows
        rc = self.runPS("./PS/installWSL.ps1")

        #Run our bash script to download and run Plone's universal installer
        rc = self.runPS("./PS/installPloneWSL.ps1")

    def runPS(self, scriptName):
        scriptPath = self.base_path + scriptName
        sp.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", ". "+scriptPath+" -ExecutionPolicy Unrestricted;"])

    def waitFor(self, status):
        installStatus = "begin" #Just saying default 'begin' for now
        while status != installStatus:
            k = OpenKey(HKEY_CURRENT_USER, self.ploneKey)
            installStatus = QueryValueEx(k, "install_status")[0]
        return

if __name__ == "__main__":
    try:
        app = WindowsPloneInstaller()
    except KeyboardInterrupt:
        raise SystemExit("Aborted by user request.")