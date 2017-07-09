import os
import platform
import io
import subprocess as sp
import time
from winreg import *
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

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

        if self.install_status == "begin":
            k = OpenKey(HKEY_CURRENT_USER, self.plone_key, 0, KEY_ALL_ACCESS)
            self.install_status = "elevated"
            SetValueEx(k, "install_status", 1, REG_SZ, self.install_status)
            CloseKey(k)
            self.run_PS("elevate.ps1", pipe=False)
            self.kill_app()

        self.required_build = 15063
        self.get_build_number()

        self.init_GUI()

    def get_build_number(self):
        self.run_PS("get_build_number.ps1", pipe=False)
        k = OpenKey(HKEY_CURRENT_USER, self.plone_key, 0, KEY_ALL_ACCESS)
        self.build_number = int(QueryValueEx(k, "build_number")[0])
        CloseKey(k)

    def init_GUI(self):
        self.gui = Tk()
        self.gui.title("Windows Plone Installer")
        window_width = 500
        window_height = 325
        self.fr1 = Frame(self.gui, width=window_width, height=window_height)
        self.fr1.pack(side="top")

        self.start_plone = IntVar(value=1)
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
        default_pass_button = Checkbutton(self.fr1, text="Use username:admin password:admin for Plone (otherwise be prompted)", variable=self.default_password)
        default_pass_button.grid(row=3,sticky="EW")

         #GUI Row 4
        Checkbutton(self.fr1, text="Install to default directory (otherwise be prompted)", variable=self.default_directory).grid(row=4, sticky="EW")

         #GUI Row 5
        self.auto_restart_checkbutton = Checkbutton(self.fr1, text="Reboot automatically (otherwise be prompted)", variable=self.auto_restart)
        self.auto_restart_checkbutton.grid(row=5,stick="EW")

        #GUI Row 6
        button_frame = Frame(self.fr1)

        load_logo = Image.open(self.base_path + '\\resources\\plone.png')
        logo = ImageTk.PhotoImage(load_logo.resize((45, 45), Image.ANTIALIAS))
        img = Label(button_frame, image=logo)
        img.grid(row=0, column=0, sticky="E")

        self.okaybutton = Button(button_frame, text="Okay")
        self.okaybutton.grid(row = 0, column=1, sticky="E")
        self.okaybutton.bind("<Button>", self.okay_handler)

        cancelbutton = Button(button_frame, text="Cancel")
        cancelbutton.grid(row = 0, column = 2, sticky="W")
        cancelbutton.bind("<Button>", self.cancel_handler)
        self.fin = ''

        button_frame.grid(row=6)

        self.log("Welcome to Plone Installer for Windows.")

        try:
            self.get_reg_vars()
        except:
            self.log("No previous installation config found.", display=False)

        if self.install_status == "enabling_wsl":
            self.okaybutton.configure(state="disabled")
            self.log("Picking up where we left off. Installing Linux Subsystem...")
            self.run_PS("install_wsl.ps1")

        if self.build_number < self.required_build:
            self.log("This system has Windows build number " + str(self.build_number))
            self.log("Windows 10 with Creator's Update (build 15063) required to install on WSL (recommended)")
            self.log("Will install Plone with buildout, configure and select Okay")
            #following lines commented out due to Win7 trouble, finding alternative solution
            #default_pass_button.grid_forget() #default password is always used for buildout version
            #self.auto_restart_checkbutton.grid_forget() #No restart necessary for buildout version
            #window_height = 275
            #self.fr1.config(height=window_height)

        #GUI Settings
        ws = self.gui.winfo_screenwidth()
        hs = self.gui.winfo_screenheight()
        x = (ws/2) - (window_width/2)
        y = (hs/2) - (window_height/2)
        self.gui.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))

        self.gui.mainloop()
        
    def okay_handler(self, event):
        self.okaybutton.configure(state="disabled")
        self.set_reg_vars()
        if self.install_status == "elevated":
            self.init_install()
        elif self.install_status == "enabling_wsl":
            self.log("Installation should continue after the machine restarts, thank you.")
            time.sleep(3)
            ps_process = sp.Popen(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "-WindowStyle", "Hidden", "Restart-Computer"])

    def cancel_handler(self, event):
        self.kill_app()

    def init_install(self):
        self.update_scripts()
        self.progress["value"] = 10

        if self.build_number < self.required_build:
            self.install_plone_buildout()
        else:
            self.run_PS("enable_wsl.ps1")

    def update_scripts(self):
        if self.build_number >= self.required_build:
            install_call = "sudo ./install.sh"

            if self.default_password.get():
                install_call += " --password=admin"

            if self.default_directory.get():
                install_call += " --target=/etc/Plone"

            install_call += " standalone"

            with io.open(self.base_path + "\\bash\\plone.sh", "a", newline='\n') as bash_script: #io.open allows explicit unix-style newline characters
                bash_script.write("\n"+install_call) #I've done this using ; for now because Windows new line characters are written instead of Unix ones.

                bash_script.close()

    def install_plone_buildout(self):
            self.log("Installing Chocolatey package manager...")
            self.run_PS("install_choco.ps1", pipe=False)
            self.log("Chocolatey Installed")
            self.progress["value"] = 25
            self.run_PS("install_plone_buildout.ps1", pipe=False, hide=False)
            self.progress["value"] = 95
            self.log("Installation Complete")
            self.clean_up()

    def set_reg_vars(self):
        k = OpenKey(HKEY_CURRENT_USER, self.plone_key, 0, KEY_ALL_ACCESS)
        SetValueEx(k, "start_plone", 1, REG_SZ, str(self.start_plone.get()))
        SetValueEx(k, "default_directory", 1, REG_SZ, str(self.default_directory.get()))
        SetValueEx(k, "default_password", 1, REG_SZ, str(self.default_password.get()))
        SetValueEx(k, "auto_restart", 1, REG_SZ, str(self.auto_restart.get()))
        CloseKey(k)

    def get_reg_vars(self):
        k = OpenKey(HKEY_CURRENT_USER, self.plone_key, 0, KEY_ALL_ACCESS)
        self.start_plone.set(int(QueryValueEx(k, "start_plone")[0]))
        self.default_directory.set(int(QueryValueEx(k, "default_directory")[0]))
        self.default_password.set(int(QueryValueEx(k, "default_password")[0]))
        self.auto_restart.set(int(QueryValueEx(k, "auto_restart")[0]))
        CloseKey(k)

    def run_PS(self,script_name, pipe=True, hide=True):
        script_path = self.base_path+"\\PS\\"+script_name

        if pipe and hide:
            self.log("Calling " + script_name + " in Microsoft PowerShell, please accept any prompts.")
            ps_process = sp.Popen(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "-ExecutionPolicy", "Unrestricted", "-WindowStyle", "Hidden", ". " + script_path], stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)

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
                        self.log(line, display=False)
                else:
                    break #No more lines to read from the PowerShell process.

            if status == "normal":
                return
            else:
                self.PS_status_handler(status)
        elif hide:
            #self.log("Calling " + script_name + " in Microsoft PowerShell, it should remain hidden.")
            ps_process = sp.Popen(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "-ExecutionPolicy", "Unrestricted", "-WindowStyle", "Hidden", ". " + script_path])
            ps_process.wait()
        else: #This will have to change if there's ever a reason for pipe=True & hide=False (doubtful)
            self.log("Please follow PowerShell prompts to continue. Calling " + script_name + " in Microsoft PowerShell.")
            ps_process = sp.Popen(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "-ExecutionPolicy", "Unrestricted", ". " + script_path])
            self.gui.withdraw() #We'll close our window and focus on PowerShell
            ps_process.wait()
            self.gui.deiconify()

    def PS_status_handler(self, status):
        if status == "Installing WSL":
            self.log('Linux Subsystem is enabled')
            self.progress["value"] = 20
            self.run_PS("install_wsl.ps1", pipe=False, hide=False)
        elif status == "Installing Plone on WSL":
            self.progress["value"] = 35
            self.run_PS("install_plone_wsl.ps1", pipe=False, hide=False) #Install Plone on the new instance of WSL
        elif status == "Plone must restart the machine":
            if self.auto_restart.get():
                ps_process = sp.Popen(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", "-WindowStyle", "Hidden", "Restart-Computer"])
            else:
                self.install_status = "enabling_wsl"
                self.okaybutton.configure(state="enabled")
                log("Please press Okay when you're ready!")
        elif status == "Plone Installed Succesffully":
            self.progress["value"] = 95
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

    def run_plone(self):
        with open(self.base_path + "\\PS\\start_plone.ps1", "a") as start_script:
            if self.build_number >= self.required_build:
                start_script.write('\nbash -c "sudo -u plone_daemon /etc/Plone/zinstance/bin/plonectl start"') #this line will start plone in WSL
            else:
                start_script.write('\nC:\bin\instance fg')

            start_script.close()
        self.run_PS("start_plone.ps1", pipe=False, hide=False)

    def clean_up(self):
        self.log('Cleaning up.')
        k = OpenKey(HKEY_CURRENT_USER, self.plone_key, 0, KEY_ALL_ACCESS)
        DeleteKey(k, "auto_restart")
        DeleteKey(k, "base_path")
        DeleteKey(k, "build_number")
        DeleteKey(k, "default_directory")
        DeleteKey(k, "default_password")
        DeleteKey(k, "install_status")
        DeleteKey(k, "installer_path")
        DeleteKey(k, "log_path")
        DeleteKey(k, "show_all")
        DeleteKey(k, "start_plone")
        CloseKey(k)
        DeleteKey(HKEY_CURRENT_USER, self.plone_key)
        self.progress["value"] = 100
        self.log("Thank you! The installer will close.")
        time.sleep(5)
        if self.start_plone:
            self.run_plone()
        self.kill_app()

    def kill_app(self):
        sys.exit(0)

if __name__ == "__main__":
    try:
        app = WindowsPloneInstaller()
    except KeyboardInterrupt:
        raise SystemExit("Aborted by user request.")