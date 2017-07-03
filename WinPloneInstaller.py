import subprocess as sp
import os
import io
import platform
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
        #self.run_once_key = r'Software\Microsoft\Windows\CurrentVersion\RunOnce'

        self.installer_path = os.path.realpath(__file__).split(".")[0]+".exe"
        self.log_path = os.path.dirname(self.installer_path) + "\install.log"

        try: #Grab installation state from registry if it exists
            k = OpenKey(HKEY_CURRENT_USER, self.plone_key, 0, KEY_ALL_ACCESS)
            self.install_status = QueryValueEx(k, "install_status")[0]

        except: #Otherwise create it with ititial "begin" value
            k = CreateKey(HKEY_CURRENT_USER, self.plone_key)
            self.install_status = "begin"
            SetValueEx(k, "install_status", 1, REG_SZ, self.install_status)

        SetValueEx(k, "base_path", 1, REG_SZ, self.base_path) #This ensures powershell and bash can find this path.
        SetValueEx(k, "installer_path", 1, REG_SZ, self.installer_path)
        SetValueEx(k, "log_path", 1, REG_SZ, self.log_path)
        CloseKey(k)

        self.last_status = self.install_status

        self.init_GUI()

    def init_GUI(self):
        self.gui = Tk()
        self.gui.title("Windows Plone Installer")
        window_width = 500
        window_height = 325
        self.fr1 = Frame(self.gui, width=window_width, height=window_height)
        self.fr1.pack(side="top")

        self.start_plone = IntVar(value=1)
        self.show_all = IntVar(value=0)
        self.default_password = IntVar(value=1)
        self.default_directory = IntVar(value=1)
        self.auto_restart = IntVar(value=1)

        #GUI Row 0
        self.log_text = Text(self.fr1, borderwidth=3, relief="sunken",spacing1=1, height=8, width=50, bg="black", fg="white")
        self.log_text.config(font=("consolas", 12), undo=True, wrap='word')
        self.log_text.grid(row=0, column=0, sticky="nsew", padx=2, pady=2) 

        scrollb = Scrollbar(self.fr1, command=self.log_text.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.log_text['yscrollcommand'] = scrollb.set

        #GUI Row 1
        self.progress = Progressbar(self.fr1, orient="horizontal", length=200, mode="determinate")
        self.progress.grid(row=1, sticky="EW")

        #GUI Row 2
        Checkbutton(self.fr1, text="Start Plone after installation", variable=self.start_plone).grid(row=2,sticky="EW")

        #GUI Row 3
        Checkbutton(self.fr1, text="Show all PowerShell output", variable=self.show_all).grid(row=3,sticky="EW")

        #GUI Row 4
        Checkbutton(self.fr1, text="Use username:admin password:admin for Plone (otherwise be prompted)", variable=self.default_password).grid(row=4,sticky="EW")

         #GUI Row 5
        Checkbutton(self.fr1, text="Install to default directory (/etc/Plone, otherwise be prompted)", variable=self.default_directory).grid(row=5, sticky="EW")

         #GUI Row 6
        self.auto_restart_checkbutton = Checkbutton(self.fr1, text="Reboot automatically (otherwise be prompted)", variable=self.auto_restart)
        self.auto_restart_checkbutton.grid(row=6,stick="EW")

        #GUI Row 7
        button_frame = Frame(self.fr1)

        self.okaybutton = Button(button_frame, text="Okay")
        self.okaybutton.grid(row = 0, column=0, sticky="W")
        self.okaybutton.bind("<Button>", self.okay_handler)

        cancelbutton = Button(button_frame, text="Cancel")
        cancelbutton.grid(row = 0, column = 1, sticky="E")
        cancelbutton.bind("<Button>", self.cancel_handler)
        self.fin = ''

        button_frame.grid(row=7)

        #GUI Settings
        ws = self.gui.winfo_screenwidth()
        hs = self.gui.winfo_screenheight()
        x = (ws/2) - (window_width/2)
        y = (hs/2) - (window_height/2)
        self.gui.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

        self.log("Welcome to Plone Installer for Windows.")

        try:
            self.get_reg_vars()
        except:
            self.log("No previous installation config found.", display=False)

        if self.install_status == "begin":
            self.log("Press 'Okay' to launch PowerShell and make sure we are running as Administrator")
        elif self.install_status == "elevated":
            self.log("Running as Administrator; thank you")
            self.init_install()
        elif self.install_status == "enabling_wsl":
            self.log("Picking up where we left off. Installing Linux Subsystem...")
            self.run_PS("install_wsl.ps1")

        self.gui.mainloop()
        
    def okay_handler(self, event):
        self.set_reg_vars()
        if self.install_status == "begin":
            k = OpenKey(HKEY_CURRENT_USER, self.plone_key, 0, KEY_ALL_ACCESS)
            self.install_status = "elevated"
            SetValueEx(k, "install_status", 1, REG_SZ, self.install_status)
            CloseKey(k)
            self.run_PS("elevate.ps1")
        elif self.install_status == "elevated":
            self.init_install()

    def cancel_handler(self, event):
        self.kill_app()

    def init_install(self):

        self.okaybutton.configure(state="disabled")

        self.update_scripts()
        self.run_PS("enable_wsl.ps1") #Make sure WSL is enabled and check if it is already installed

    def update_scripts(self):
        install_call = "sudo ./install.sh"

        if self.default_password.get():
            install_call += " --password=admin"

        if self.default_directory.get():
            install_call += " --target=/etc/Plone"

        install_call += " standalone"

        with io.open(self.base_path + "\\bash\\plone.sh", "a", newline='\n') as bash_script: #io.open allows explicit unix-style newline characters
            bash_script.write("\n"+install_call) #I've done this using ; for now because Windows new line characters are written instead of Unix ones.

            if self.start_plone.get():
                bash_script.write("\nsudo -u plone_daemon /etc/Plone/zinstance/bin/plonectl start") #this line will start plone in WSL

            #bash_script.write("\nrm -rf ") #this will delete the universal installer archive and directory
            bash_script.close()
            
        if self.start_plone.get():
            with open(self.base_path + "\\PS\\install_plone_buildout.ps1", "a") as buildout_script:
                    buildout_script.write('\nbin\instance start')

                    buildout_script.close()
                        
    def set_reg_vars(self):
        k = OpenKey(HKEY_CURRENT_USER, self.plone_key, 0, KEY_ALL_ACCESS)
        SetValueEx(k, "start_plone", 1, REG_SZ, str(self.start_plone.get()))
        SetValueEx(k, "default_directory", 1, REG_SZ, str(self.default_directory.get()))
        SetValueEx(k, "default_password", 1, REG_SZ, str(self.default_password.get()))
        SetValueEx(k, "auto_restart", 1, REG_SZ, str(self.auto_restart.get()))
        SetValueEx(k, "show_all", 1, REG_SZ, str(self.show_all.get()))
        CloseKey(k)

    def get_reg_vars(self):
        k = OpenKey(HKEY_CURRENT_USER, self.plone_key, 0, KEY_ALL_ACCESS)
        self.start_plone.set(int(QueryValueEx(k, "start_plone")[0]))
        self.default_directory.set(int(QueryValueEx(k, "default_directory")[0]))
        self.default_password.set(int(QueryValueEx(k, "default_password")[0]))
        self.auto_restart.set(int(QueryValueEx(k, "auto_restart")[0]))
        self.show_all.set(int(QueryValueEx(k, "show_all")[0]))
        CloseKey(k)

    def run_PS(self,script_name,pipe=True):
        script_path = self.base_path+"\\PS\\"+script_name

        if pipe:
            self.log("Calling " + script_name + " in Microsoft PowerShell, please accept any prompts.")
            ps_process = sp.Popen(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "-WindowStyle", "Hidden", ". " + script_path], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
            status = "normal"
            while True:
                line = ps_process.stdout.readline().decode("utf-8").rstrip()
                if line != '':                    
                    if line[:2] == "**": #this is a log flag echoed out from the powershell process.
                        self.log(line[2:])
                    elif line[:2] == "*!": #this is an important status/command flag to the installer from the powershell process.
                        status = line[2:]
                        self.log(status)
                        break #we need to get out of this loop before we proceed with the message for control flow
                    else:
                        if self.show_all.get():
                            self.log(line)
                        else:
                            self.log(line, display=False)
                else:
                    break #No more lines to read from the PowerShell process.

            if status == "normal":
                return
            else:
                self.PS_status_handler(status)
        else:
            self.log("Please follow PowerShell prompts to continue. Calling " + script_name + " in Microsoft PowerShell.")
            ps_process = sp.Popen(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", ". " + script_path])
            self.gui.withdraw() #We'll close our window and focus on PowerShell
            ps_process.wait()
            self.gui.deiconify()

    def PS_status_handler(self, status):
        if status == "Installing WSL":
            self.log('Linux Subsystem is enabled')
            self.progress["value"] = 10
            self.run_PS("install_wsl.ps1", pipe=False)
        elif status == "Installing Plone with buildout":
            self.run_PS("install_choco.ps1") #This will install chocolatey and send status 'Chocolatey Installed'
        elif status == "Chocolatey Instaled":
            self.run_PS("install_plone_buildout.ps1")
        elif status == "Installing Plone on WSL":
            self.progress["value"] = 30
            self.run_PS("install_plone_wsl.ps1", pipe=False) #Install Plone on the new instance of WSL
        elif status == "Plone must restart the machine":
            if self.auto_restart.get():
                ps_process = sp.Popen(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "-WindowStyle", "Hidden", "Restart-Computer"])
            else:
                log("")
        elif status == "Elevating Process":
            self.log("Will restart executable as Admin; please accept any prompts.")
            time.sleep(3) #Don't close the program before the user gets a chance to understand what's happening
            self.kill_app() #PowerShell will reopen as administrator
        elif status == "Running as Admin":
            self.okaybutton.configure(state="enabled")
            self.log("Press 'Okay' to launch PowerShell, gather information about your system and prepare to install Plone.")
        elif status == "Plone Installed Succesffully":
            self.progress["value"] = 100
            self.clean_up()

    def log(self, message, display=True):
        with open(self.log_path, "a") as log:
            log.write(message+"\n")
        if display:
            self.log_text.config(state="normal")
            self.log_text.insert(END, "> " + message + '\n')
            self.log_text.config(state="disabled")
            self.log_text.see(END)
            self.gui.update()

    def clean_up(self):
        self.log('Cleaning up.')
        k = OpenKey(HKEY_CURRENT_USER, self.plone_key, 0, KEY_ALL_ACCESS)
        DeleteKey(k, "install_status")
        DeleteKey(k, "base_path")
        DeleteKey(k, "installer_path")
        DeleteKey(k, "win_version")
        CloseKey(k)
        DeleteKey(HKEY_CURRENT_USER, self.plone_key)

    def kill_app(self):
        sys.exit(0)

if __name__ == "__main__":
    try:
        app = WindowsPloneInstaller()
    except KeyboardInterrupt:
        raise SystemExit("Aborted by user request.")