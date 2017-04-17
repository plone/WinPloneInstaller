import subprocess as sp
import os
import platform
from winreg import *

try:
    from tkinter import *
    from tkinter.ttk import *
    import tkinter.filedialog as filedialog
except ImportError:
    from Tkinter import *
    from ttk import *
    import tkFileDialog as filedialog

class WindowsPloneInstaller:

    def __init__(self):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            self.base_path = sys._MEIPASS
        except Exception:
            self.base_path = os.path.abspath(".")

        #self.powershell_windowstyle = "normal"
        log = open(self.base_path+"installLog.txt","w+")
        log.write("Beginning Plone Install")
        log.close()

        self.restartKey = r'SOFTWARE\PLONE\wslRestart'
        try: #Check if key exists
            k = OpenKey(HKEY_CURRENT_USER, self.restartKey)
            restarted = QueryValue(HKEY_CURRENT_USER, self.restartKey)
            self.initGUI(restarted)

        except:
            k = CreateKey(HKEY_CURRENT_USER, self.restartKey)
            restarted = "0"
            SetValue(HKEY_CURRENT_USER, self.restartKey, REG_SZ, restarted)
            self.initGUI(restarted)

    def killapp(self, event):
        sys.exit(0)

    def GetFile(self, event):
        self.fin = filedialog.askopenfilename()
        self.filein.delete(0, 'end')
        self.filein.insert(0, self.fin)

    def initGUI(self, restarted):
        root = Tk()
        root.title("Windows Plone Installer")
        fr1 = Frame(root, width=300, height=100)
        fr1.pack(side="top")

        fr2 = Frame(root, width=300, height=300,
                    borderwidth=2, relief="ridge")
        fr2.pack(ipadx=10, ipady=10)
        fr4 = Frame(root, width=300, height=100)
        fr4.pack(side="bottom", pady=10)

        if restarted == "1":
            l = Label(fr2, text="Picking up where we left off.")
            l.grid(sticky="NW")

            ws = root.winfo_screenwidth()
            hs = root.winfo_screenheight()
            x = (ws/2) - (400/2)
            y = (hs/2) - (250/2)
            root.geometry('%dx%d+%d+%d' % (400, 250, x, y))

            root.mainloop()

            #Install Ubuntu on Windows
            psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',"-Command", "Set-Location "+self.base_path, self.base_path+'./PS/installWSL.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
            #psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted','-windowstyle',powershell_windowstyle,base_path+'./PS/installWSL.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
            output, error = psResult.communicate()
            rc = psResult.returncode

            #Run our p
            psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',self.base_path+'./PS/installPloneWSL.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
            #psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted','-windowstyle',powershell_windowstyle,base_path+'./PS/installPloneWSL.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
            output, error = psResult.communicate()
            rc = psResult.returncode
        else:
            requiredBuildNumber = 15063
            envWinBuildNumber = int(platform.platform().split('.')[2].split('-')[0])
            if envWinBuildNumber >= requiredBuildNumber:
                self.install_type = IntVar(value=1)
                checkbox = Checkbutton(fr2, text="Install using Ubuntu for Windows (recommended)", variable=self.install_type)
                checkbox.grid(sticky="NW")
            else:
                l = Label(fr2, text="You do not have a new enough version of Windows to install with Ubuntu for Windows.\n Please install Creator's Update or newer to use Ubuntu.\nOr press OK to install using standard buildout.")
                l.grid(sticky="NW")

            okaybutton = Button(fr4, text="Okay   ")
            okaybutton.bind("<Button>", self.initInstall)
            okaybutton.pack(side="left")

            cancelbutton = Button(fr4, text="Cancel")
            cancelbutton.bind("<Button>", self.killapp)
            cancelbutton.pack(side="right")
            self.fin = ''

            ws = root.winfo_screenwidth()
            hs = root.winfo_screenheight()
            x = (ws/2) - (400/2)
            y = (hs/2) - (250/2)
            root.geometry('%dx%d+%d+%d' % (400, 250, x, y))

            root.mainloop()
        
    def initInstall(self, event):

        #Install Chocolatey for every user
        psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',self.base_path+'./PS/installChoco.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
        #psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted','-windowstyle',powershell_windowstyle,base_path+'./PS/installChoco.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
        output, error = psResult.communicate()
        rc = psResult.returncode

        self.waitFor("choco installed")

        if self.install_type.get():
            #Enable WSL for user's who are willing and able to install using Ubuntu/Bash
            psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',self.base_path+'./PS/enableWSL.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
            #psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted','-windowstyle',powershell_windowstyle,base_path+'./PS/enableWSL.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
            output, error = psResult.communicate()
            rc = psResult.returncode

            #Set Win Registry to load our installer after the next restart
            runOnceKey = r'Software\Microsoft\Windows\CurrentVersion\RunOnce'
            installerPath = os.path.realpath(__file__)
            SetValue(HKEY_CURRENT_USER, runOnceKey, REG_SZ,installerPath+"\WinPloneInstaller.exe")

            #we should probably set this at the end of enableWSL.ps1
            restarted = "1"
            SetValue(HKEY_CURRENT_USER, self.restartKey, REG_SZ, restarted)
        else:
            #Grab dependencies with Choco
            psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',self.base_path+'./PS/chocoBuildout.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
            #psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted','-windowstyle',powershell_windowstyle,base_path+'./PS/installPloneBuildout.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
            output, error = psResult.communicate()
            rc = psResult.returncode

            #Run the regular Plone buildout script for users who are not using Ubuntu/Bash
            psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted',self.base_path+'./PS/installPloneBuildout.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
            #psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted','-windowstyle',powershell_windowstyle,base_path+'./PS/installPloneBuildout.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
            output, error = psResult.communicate()
            rc = psResult.returncode

        # If debugging is needed, this should help
        #print ("Return code given to Python script is: " + str(rc))
        #print ("\n\nstdout:\n\n" + str(output))
        #print ("\n\nstderr: " + str(error))

    def waitFor(self, line):
        lastLine = ""
        while lastLine != line:
            logFile = open(self.base_path+"installLog.txt")
            lineList = logFile.readlines()
            print(lineList)
            logFile.close()
            lastLine = lineList[len(lineList)-1]

if __name__ == "__main__":
    try:
        app = WindowsPloneInstaller()
    except KeyboardInterrupt:
        raise SystemExit("Aborted by user request.")