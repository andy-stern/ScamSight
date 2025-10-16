import sys
sys.dont_write_bytecode = True
import os
import ctypes
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from loginpage import LoginPage
from registerpage import RegisterPage
from homepage import HomePage
from articlespage import ArticlesPage
from settingspage import SettingsPage
from contactspage import ContactPage
from Scripts.logout import Logout

# CONF
AUTHFILE = os.path.expanduser("~/scamsight.auth.json")

class ScamSightApp(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("ScamSight")
        
        self.iconbitmap(os.path.join(os.path.dirname(__file__), "ScamSight.ico"))

        icon = Image.open(os.path.join(os.path.dirname(__file__), "ScamSight.ico"))
        icon = ImageTk.PhotoImage(icon)
        
        self.iconphoto(True, icon)
        self.after(10, lambda: self.iconphoto(True, icon))

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = sw // 2, sh // 2
        x, y = (sw - w) // 2, (sh - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.resizable(False, False)

        self.sidebarfuncs = {"home": self.showhome, "articles": self.showarticles, "settings": self.showsettings, "contactus": self.showcontactus, "logout": self.logout}

        self.currentframe = None
        self.homepage = HomePage(self, self.sidebarfuncs)
        self.loginpage = LoginPage(self, self.showregister, self.showhome)
        self.registerpage = RegisterPage(self, self.showlogin)
        self.articlespage = ArticlesPage(self, self.sidebarfuncs)
        self.settingspage = SettingsPage(self, self.sidebarfuncs)
        self.contactspage = ContactPage(self, self.sidebarfuncs)

        self.attributes("-topmost", True)
        self.showlogin()
        self.loginpage.checktokenstatus()
        self.after(10, lambda: self.attributes("-topmost", False))

    def showlogin(self):
        self.switchframe(self.loginpage)

    def showregister(self):
        self.switchframe(self.registerpage)

    def showhome(self):
        self.switchframe(self.homepage)

    def showarticles(self):
        self.switchframe(self.articlespage)

    def showsettings(self):
        self.switchframe(self.settingspage)

    def showcontactus(self):
        self.switchframe(self.contactspage)

    def logout(self):
        confirmation = ttk.dialogs.Messagebox.show_question(
            "Confirm log out?",
            "Log Out Confirmation",
            buttons=["No:secondary", "Yes:danger"],
        )
        if confirmation == "Yes":
            response = Logout()
            if response == 200:
                self.showlogin()
            elif response == 403:
                ttk.dialogs.Messagebox.show_error(
                    "Invalid or expired token. Please close and reopen the app.", "Logout Error"
                )
            elif response == 500:
                ttk.dialogs.Messagebox.show_error(
                    "An internal server error occurred. Please try again later.", "Server Error"
                )

    def switchframe(self, newframe):
        if self.currentframe:
            self.currentframe.pack_forget()
        self.currentframe = newframe
        self.currentframe.pack(fill="both", expand=True)

if __name__ == "__main__":
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("com.scamsight.app")
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
    
    app = ScamSightApp()
    app.mainloop()