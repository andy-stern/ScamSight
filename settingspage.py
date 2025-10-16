import re
import os
import json
import ttkbootstrap as ttk
from Scripts.https import Post
from Scripts.passwordfeedback import PasswordFeedback

# CONF
EMAILREGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
AUTHFILE = os.path.expanduser("~/scamsight.auth.json")

class SettingsPage(ttk.Frame):
    def __init__(self, master, sidebarfuncs):
        super().__init__(master)
        self.sidebarfuncs = sidebarfuncs
        self.createwidgets()

    def createwidgets(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        sidebar = ttk.Frame(self, width=200, bootstyle="dark")
        sidebar.grid(row=0, column=0, sticky="nswe")
        sidebar.grid_propagate(False)

        ttk.Label(
            sidebar,
            text="ScamSight",
            font=("Helvetica", 24, "bold"),
            foreground="#5dade2",
            background="#303030",
            bootstyle="primary"
        ).pack(pady=(40, 30))

        btncontainer = ttk.Frame(sidebar, bootstyle="dark")
        btncontainer.pack(fill="x", padx=10, pady=10)

        ttk.Button(
            btncontainer, 
            text="New Analysis",
            bootstyle="secondary-outline",
            width=20,
            command=self.sidebarfuncs["home"]
        ).pack(fill="x", pady=4, ipady=4)

        ttk.Button(
            btncontainer, 
            text="Articles",
            bootstyle="secondary-outline", 
            width=20,
            command=self.sidebarfuncs["articles"]
        ).pack(fill="x", pady=4, ipady=4)

        ttk.Button(
            btncontainer, 
            text="Settings",
            bootstyle="primary", 
            width=20,
            command=self.sidebarfuncs["settings"]
        ).pack(fill="x", pady=4, ipady=4)

        ttk.Button(
            btncontainer, 
            text="Contact Us",
            bootstyle="secondary-outline", 
            width=20,
            command=self.sidebarfuncs["contactus"]
        ).pack(fill="x", pady=4, ipady=4)

        ttk.Button(
            btncontainer,
            text="Log Out",
            bootstyle="secondary-outline",
            width=20,
            command=self.sidebarfuncs["logout"],
        ).pack(fill="x", pady=4, ipady=4)

        content = ttk.Frame(self)
        content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)

        ttk.Label(
            content,
            text="Settings",
            font=("Helvetica", 20, "bold"),
            bootstyle="primary",
            background="#222222"
        ).grid(row=0, column=0, pady=(0, 20))

        container = ttk.Frame(content)
        container.grid(row=1, column=0, sticky="nsew")
        container.grid_rowconfigure(4, weight=1)
        container.grid_columnconfigure(0, weight=1)

        emailframe = ttk.LabelFrame(container, text="Change Email", bootstyle="primary", padding=10)
        emailframe.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        emailframe.grid_columnconfigure(0, weight=1)

        emailinner = ttk.Frame(emailframe)
        emailinner.pack(fill="x")
        emailinner.grid_columnconfigure(0, weight=1)

        self.newemailvar = ttk.StringVar()
        self.newemailentry = ttk.Entry(emailinner, textvariable=self.newemailvar)
        self.newemailentry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.newemailentry.insert(0, "New Email")
        self.newemailentry.bind("<FocusIn>", lambda e: self.clearplaceholder(e, "newemail"))
        self.newemailentry.bind("<FocusOut>", lambda e: self.restoreplaceholder(e, "newemail", "New Email"))

        ttk.Button(
            emailinner,
            text="Change Email",
            command=self.initiateemailchange,
            width=15
        ).grid(row=0, column=1)

        passwordframe = ttk.LabelFrame(container, text="Change Password", bootstyle="primary", padding=10)
        passwordframe.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        passwordframe.grid_columnconfigure(0, weight=1)

        self.currentpaswordvar = ttk.StringVar()
        self.currentpasswordentry = ttk.Entry(passwordframe, textvariable=self.currentpaswordvar, show="")
        self.currentpasswordentry.pack(fill="x", pady=(0, 10))
        self.currentpasswordentry.insert(0, "Current Password")
        self.currentpasswordentry.bind("<FocusIn>", lambda e: self.clearplaceholder(e, "currentpassword"))
        self.currentpasswordentry.bind("<FocusOut>", lambda e: self.restoreplaceholder(e, "currentpassword", "Current Password"))

        self.newpasswordvar = ttk.StringVar()
        self.newpasswordentry = ttk.Entry(passwordframe, textvariable=self.newpasswordvar, show="")
        self.newpasswordentry.pack(fill="x", pady=(0, 10))
        self.newpasswordentry.insert(0, "New Password")
        self.newpasswordentry.bind("<FocusIn>", lambda e: self.clearplaceholder(e, "newpassword"))
        self.newpasswordentry.bind("<FocusOut>", lambda e: self.restoreplaceholder(e, "newpassword", "New Password"))

        self.confirmpasswordvar = ttk.StringVar()
        self.confirmpasswordentry = ttk.Entry(passwordframe, textvariable=self.confirmpasswordvar, show="")
        self.confirmpasswordentry.pack(fill="x", pady=(0, 10))
        self.confirmpasswordentry.insert(0, "Confirm New Password")
        self.confirmpasswordentry.bind("<FocusIn>", lambda e: self.clearplaceholder(e, "confirmpassword"))
        self.confirmpasswordentry.bind("<FocusOut>", lambda e: self.restoreplaceholder(e, "confirmpassword", "Confirm New Password"))

        btnframe = ttk.Frame(passwordframe)
        btnframe.pack(fill="x")

        ttk.Button(
            btnframe,
            text="Get Password Feedback",
            command=self.passwordfeedback,
            bootstyle="info",
        ).pack(side="left")

        ttk.Button(
            btnframe,
            text="Change Password",
            command=self.changepassword,
            bootstyle="success"
        ).pack(side="right")

        tfaframe = ttk.LabelFrame(container, text="Two-Factor Authentication", bootstyle="primary", padding=10)
        tfaframe.grid(row=2, column=0, sticky="ew", pady=(0, 20))

        self.tfavar = ttk.BooleanVar(value=False)

        token = ""

        try:
            with open(AUTHFILE) as f:
                authdata = json.load(f)

            token = authdata.get("token")
        except Exception:
            pass

        if token:
            response = Post(
                "https://api.scamsight.app/get2fastatus", 
                headers={"Authorization": token}
            )

            if response.status_code == 403:
                ttk.dialogs.Messagebox.show_error(
                    "Invalid or expired token. Please close and reopen the app.", "Get 2FA Status Error",
                )
            elif response.status_code == 500:
                ttk.dialogs.Messagebox.show_error(
                    "An internal server error occurred. Please try again later.", "Server Error"
                )
                
            if response.json().get("status"):
                self.tfavar.set(True)

        ttk.Checkbutton(
            tfaframe, 
            text="Enable/Disable Two-Factor Authentication",
            variable=self.tfavar,
            command=self.toggle2fa,
            bootstyle="primary-round-toggle"
        ).pack(anchor="w")

        deletionframe = ttk.LabelFrame(container, text="Account Deletion", bootstyle="danger", padding=5)
        deletionframe.grid(row=3, column=0, sticky="ew", pady=(0, 20))

        ttk.Label(
            deletionframe, 
            text="Warning: This action is irreversible. All your data will be lost."
        ).pack(anchor="w", pady=(0, 10))

        ttk.Button(
            deletionframe,
            text="Delete Account",
            command=self.initiateaccountdeletion, 
            bootstyle="danger",
            width=15
        ).pack(anchor="e")

        ttk.Frame(container).grid(row=4, column=0, sticky="nsew")

    def clearplaceholder(self, event, field):
        entry = event.widget
        placeholders = {
            "newemail": "New Email",
            "currentpassword": "Current Password",
            "newpassword": "New Password",
            "confirmpassword": "Confirm New Password"
        }

        if entry.get() == placeholders.get(field, ""):
            entry.delete(0, "end")
            if "password" in field:
                entry.config(show="•")

    def restoreplaceholder(self, event, field, placeholder):
        entry = event.widget
        if not entry.get():
            entry.insert(0, placeholder)
            if "password" in field:
                entry.config(show="")

    def initiateemailchange(self):
        newemail = self.newemailvar.get().strip()
        if not newemail or newemail == "New Email":
            ttk.dialogs.Messagebox.show_error(
                "Please enter a valid email address.", "Email Change Error"
            )
            return
        if not bool(EMAILREGEX.match(newemail)): 
            ttk.dialogs.Messagebox.show_error(
                "Please enter a valid email address.", "Email Change Error"
            )
            return
        with open(AUTHFILE) as f:
            authdata = json.load(f)

        result = ttk.dialogs.Messagebox.show_question(
            "This will permanently change your account's email. Confirm?",
            "Final Confirmation",
            buttons=["No:secondary", "Yes:danger"],
        )

        if result == "No":
            return

        token = authdata.get("token")
        headers = {
            "Authorization": token,
            "newemail": newemail
        }
        response = Post("https://api.scamsight.app/changeemail", headers=headers)
        if response.status_code == 200:
            ttk.dialogs.Messagebox.show_info(
                "Email changed successfully! Please check your email on the new email provided to verify it.", "Success"
            )
            self.master.showlogin()
            os.remove(AUTHFILE)
        elif response.status_code == 403:
            ttk.dialogs.Messagebox.show_error(
                "Invalid or expired token. Please close and reopen the app.", "Email Change Error"
            )
        elif response.status_code == 500:
            ttk.dialogs.Messagebox.show_error(
                "An internal server error occurred. Please try again later.", "Server Error"
            )
        elif response.status_code == 429:
            ttk.dialogs.Messagebox.show_error(
                "Too many requests. Please try again later.", "Server Error"
            )

    def centerdialog(self, dialog, w, h):
        dialog.geometry(f"{w}x{h}")
        dialog.update_idletasks()
        
        root = self.winfo_toplevel()
        x = root.winfo_x() + (root.winfo_width() // 2) - (w // 2)
        y = root.winfo_y() + (root.winfo_height() // 2) - (h // 2)
        dialog.geometry(f"+{x}+{y}")

    def passwordfeedback(self):
        password = self.newemailvar.get().strip()
        if not password or password == "New Password":
            ttk.dialogs.Messagebox.show_error(
                "Please enter a password to get feedback.", "Passsword Feedback Error"
            )
            return
        PasswordFeedback(self.newpasswordvar.get())

    def changepassword(self):
        current = self.currentpaswordvar.get().strip()
        new = self.newpasswordvar.get().strip()
        confirm = self.confirmpasswordvar.get().strip()

        if not current or current == "Current Password":
            ttk.dialogs.Messagebox.show_error(
                "Please enter your current password.", "Change Password Error"
            )
            return
        if not new or new == "New Password":
            ttk.dialogs.Messagebox(
                "Please enter a new password.", "Change Password Error"
            )
            return
        if new != confirm:
            ttk.dialogs.Messagebox(
                "New passwords do not match.", "Change Password Error"
            )
            return

        with open(AUTHFILE) as f:
            authdata = json.load(f)

        token = authdata.get("token")
        response = Post(
            "https://api.scamsight.app/changepassword",
            headers={"Authorization": token, "currentpassword": current, "newpassword": new},
        )

        if response.status_code == 200:
            ttk.dialogs.Messagebox.show_info(
                "Password changed successfully. Please log in again.", "Success"
            )
            self.master.showlogin()
        elif response.status_code == 403:
            ttk.dialogs.Messagebox.show_error(
                "Invalid or expired token. Please close and reopen the app.", "Change Password Error"
            )
        elif response.status_code == 402:
            ttk.dialogs.Messagebox.show_error(
                "Incorrect credentials. Please close the application and log in again.", "Change Password Error"
            )
        elif response.status_code == 404:
            ttk.dialogs.Messagebox.show_error(
                "User not found. Please close and reopen the app.", "Change Password Error"
            )
        elif response.status_code == 500:
            ttk.dialogs.Messagebox.show_error(
                "An internal server error occurred. Please try again later.", "Server Error"
            )

    def toggle2fa(self):
        if self.tfavar.get():
            dialog = ttk.Toplevel(self)
            dialog.title("Information Needed")
            self.centerdialog(dialog, 400, 200)
            dialog.resizable(False, False)
            dialog.transient(self)
            dialog.grab_set()

            ttk.Label(
                dialog,
                text="Enter the same email address linked to this account:",
                wraplength=350
            ).pack(pady=(20, 10))

            emailvar = ttk.StringVar()
            emailentry = ttk.Entry(dialog, textvariable=emailvar, width=20, font=("Helvetica", 14))
            emailentry.pack(pady=10)
            emailentry.focus_set()

            def cancel():
                dialog.destroy()
                self.tfavar.set(False)

            def verify():
                if not bool(EMAILREGEX.match(emailvar.get())): 
                    ttk.dialogs.Messagebox.show_error(
                        "Please enter a valid email address.", "Enable 2FA Error"
                    )
                    return

                with open(AUTHFILE) as f:
                    authdata = json.load(f)

                token = authdata.get("token")
                response = Post(
                    "https://api.scamsight.app/enable2fa",
                    headers = {"Authorization": token, "email": emailvar.get()}
                )
                if response.status_code == 200:
                    ttk.dialogs.Messagebox.show_info(
                        "Two-factor authentication has been enabled. Please check your email and click the link to confirm this change.", "Success"
                    )
                    self.tfavar.set(True)
                    dialog.destroy()
                    return
                elif response.status_code == 403:
                    ttk.dialogs.Messagebox.show_error(
                        "Invalid or expired token. Please close the application and log in again.", "2FA Error"
                    )
                    self.tfavar.set(False)
                    dialog.destroy()
                    return
                elif response.status_code == 422:
                    ttk.dialogs.Messagebox.show_error(
                        "Please enter the email you registered this account with. ScamSight does not store emails in their plain form.", "2FA Error"
                    )
                    self.tfavar.set(False)
                    dialog.destroy()
                    return
                elif response.status_code == 421:
                    ttk.dialogs.Messagebox.show_error(
                        "Two-factor authentication is already enabled.", "2FA Error"
                    )
                    dialog.destroy()
                    return
                else:
                    ttk.dialogs.Messagebox.show_error(
                        "An internal server error occurred. Please try again later.", "Server Error"
                    )
                    self.tfavar.set(False)
                    return

            ttk.Button(
                dialog, text="Verify", command=verify, bootstyle="success", width=10
            ).pack(pady=10)

            dialog.bind("<Return>", lambda e: verify())
            dialog.bind("<Escape>", lambda e: cancel())
            dialog.protocol("WM_DELETE_WINDOW", cancel)
        else:
            result = ttk.dialogs.Messagebox.show_question(
                "This will turn off 2FA until it is reenabled. Confirm?",
                "Final Confirmation",
                buttons=["No:secondary", "Yes:danger"],
            )

            if result == "No":
                self.tfavar.set(True)
                return

            with open(AUTHFILE) as f:
                authdata = json.load(f)

            token = authdata.get("token")

            response = Post(
                "https://api.scamsight.app/disable2fa",
                headers={"Authorization": token}
            )

            if response.status_code == 200:
                ttk.dialogs.Messagebox.show_info(
                    "Two-factor authentication has been disabled.", "Success"
                )
                self.tfavar.set(False)
            elif response.status_code == 403:
                    ttk.dialogs.Messagebox.show_error(
                        "Invalid or expired token. Please close and reopen the app.", "Disable 2FA Error"
                    )
            elif response.status_code == 500:
                ttk.dialogs.Messagebox.show_error(
                    "An internal server error occurred. Please try again later.", "Server Error"
                )
                self.tfavar.set(True)

    def initiateaccountdeletion(self):
        dialog = ttk.Toplevel(self)
        dialog.title("Confirm Account Deletion")
        self.centerdialog(dialog, 500, 300)
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()

        ttk.Label(
            dialog,
            text="To continue with the account deletion process, please type 'I understand':",
            wraplength=450
        ).pack(pady=(20, 10))

        var = ttk.StringVar()
        entry = ttk.Entry(dialog, textvariable=var, width=30)
        entry.pack(pady=10)
        entry.focus_set()

        def proceed():
            if var.get().strip() != "I understand":
                ttk.dialogs.Messagebox.show_error(
                    "Please type 'I understand' to continue.", "Account Deletion Error"
                )
                return
            dialog.destroy()
            result = ttk.dialogs.Messagebox.show_question(
                "This will permanently delete your account and all associated data. Confirm?", "Final Confirmation", buttons=["No:secondary", "Yes:danger"]
            )
            if result == "Yes":
                with open(AUTHFILE) as f:
                    authdata = json.load(f)

                token = authdata.get("token")
                userid = authdata.get("userid")
                headers = {
                    "Authorization": token,
                    "userid": userid
                }
                response = Post("https://api.scamsight.app/deleteaccount", headers=headers)
                if response.status_code == 200:
                    ttk.dialogs.Messagebox.show_info(
                        "Your account has been deleted.", "Account Deleted"
                    )
                    self.master.showlogin()
                    os.remove(AUTHFILE)
                elif response.status_code == 403:
                    ttk.dialogs.Messagebox.show_error(
                        "Invalid or expired token. Please close and reopen the app.", "Account Deletion Error"
                    ) 
                elif response.status_code == 402:
                    ttk.dialogs.Messagebox.show_error(
                        "Spoofed headers or critical server error. Please contact scamsight.app@gmail.com if you receive this error.", "Account Deletion Error"
                    ) 
                elif response.status_code == 500:
                    ttk.dialogs.Messagebox.show_error(
                        "An internal server error occurred. Please try again later.", "Server Error"
                    )
                elif response.status_code == 429:
                    ttk.dialogs.Messagebox.show_error(
                        "Too many requests. Please try again later.", "Server Error"
                    )

        ttk.Button(
            dialog,
            text="Continue",
            command=proceed,
            bootstyle="success",
            width=10
        ).pack(pady=10)

        dialog.bind("<Return>", lambda e: proceed())
