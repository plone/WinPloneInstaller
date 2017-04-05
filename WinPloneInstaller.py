import subprocess as sp
import os
import platform
import winreg

try:
    from tkinter import *
    from tkinter.ttk import *
    import tkinter.filedialog as filedialog
except ImportError:
    from Tkinter import *
    from ttk import *
    import tkFileDialog as filedialog

class WindowsPloneInstaller:

    def make_checkbutton(self, frame, text):
        var = IntVar()
        widget = Checkbutton(frame, text=text, variable=var)
        widget.grid(sticky="NW")
        return var

    def __init__(self):

        requiredBuildNumber = 15063

        root = Tk()
        root.title("Windows Plone Installer")
        fr1 = Frame(root, width=300, height=100)
        fr1.pack(side="top")

        fr2 = Frame(root, width=300, height=300,
                    borderwidth=2, relief="ridge")
        fr2.pack(ipadx=10, ipady=10)
        fr4 = Frame(root, width=300, height=100)
        fr4.pack(side="bottom", pady=10)

        Hkey = winreg.OpenKey("HKEY_CURRENT_USER\SOFTWARE\PLONE\wslRestart")
        restarted = winreg.QueryValue(Hkey)
        if restarted == "1":
            psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted','-windowstyle','hidden',base_path+'./PS/insallWSL.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
            output, error = psResult.communicate()
            rc = psResult.returncode
        else:

            if int(platform.platform().split('.')[2].split('-')[0]) > requiredBuildNumber:
                self.installType = self.make_checkbutton(fr2, "Install using Ubuntu for Windows (recommended)")
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

    def killapp(self, event):
        sys.exit(0)

    def GetFile(self, event):
        self.fin = filedialog.askopenfilename()
        self.filein.delete(0, 'end')
        self.filein.insert(0, self.fin)
        
    def initInstall(self, event):
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        psResult = sp.Popen([r'C:\WINDOWS\system32\WindowsPowerShell\v1.0\powershell.exe','-ExecutionPolicy','Unrestricted','-windowstyle','hidden',base_path+'./PS/installChoco.ps1',""],stdout = sp.PIPE,stderr = sp.PIPE)
        output, error = psResult.communicate()
        rc = psResult.returncode

        # If debugging is needed, this should help
        #print ("Return code given to Python script is: " + str(rc))
        #print ("\n\nstdout:\n\n" + str(output))
        #print ("\n\nstderr: " + str(error))

        input("Finished...")

if __name__ == "__main__":
    try:
        app = WindowsPloneInstaller()
    except KeyboardInterrupt:
        raise SystemExit("Aborted by user request.")