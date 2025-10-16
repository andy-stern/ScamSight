import os
import json
import ttkbootstrap as ttk
from Scripts.login import Login
from Scripts.https import Post
from Scripts.passwordfeedback import PasswordFeedback

# CONF
AUTHFILE = os.path.expanduser("~/scamsight.auth.json")
TOKENSTATUSURL = "https://api.scamsight.app/tokenstatus"


class LoginPage(ttk.Frame):
    def __init__(self, master, registercallback, homecallback):
        super().__init__(master)
        self.registercallback = registercallback
        self.homecallback = homecallback
        self.createwidgets()

    def passwordfeedback(self):
        PasswordFeedback(self.newpasswordvar.get())

    def login(self):
        response = Login(self.usernameentry.get(), self.passwordentry.get())

        if response == 200:
            self.homecallback()
        elif response == 201:
            ttk.dialogs.Messagebox.show_info(
                "Please check your email for a 2FA link.", "Two-Factor Authentication"
            )
        elif response == 400:
            ttk.dialogs.Messagebox.show_error(
                "Email and password required.", "Login Error"
            )
        elif response == 401:
            ttk.dialogs.Messagebox.show_error(
                "Username and/or password is incorrect.", "Login Error"
            )
        elif response == 403:
            ttk.dialogs.Messagebox.show_error(
                "Email not verified.", "Login Error"
            )
        elif response == 500:
            ttk.dialogs.Messagebox.show_error(
                "An internal error occurred. Please try again later.", "Server Error"
            )
        elif response == 429:
            ttk.dialogs.Messagebox.show_error(
                "Too many requests. Please try again later.", "Server Error"
            )

    def checktokenstatus(self):
        try:
            token = ""

            try: 
                with open(AUTHFILE) as f:
                    authdata = json.load(f)

                token = authdata.get("token")
            except Exception:
                pass

            if not token:
                return

            tokenstatus = Post(TOKENSTATUSURL, json={"token": token})
            if tokenstatus.json().get("ok") is True:
                self.homecallback()
            else:
                os.remove(AUTHFILE)
        except Exception as e:
            ttk.dialogs.Messagebox.show_error(
                "Invalid or expired token. Please log in again.", "Login Error"
            )

    def createwidgets(self):
        self.logo = ttk.Label(
            self, text="ScamSight", font=("Helvetica", 24, "bold"), bootstyle="primary"
        )
        self.logo.pack(pady=(50, 30))

        self.subtitle = ttk.Label(
            self, text="Login", font=("Helvetica", 12), bootstyle="secondary"
        )
        self.subtitle.pack(pady=(0, 20))

        self.usernamevar = ttk.StringVar()
        self.usernameentry = ttk.Entry(
            self, textvariable=self.usernamevar, width=30, bootstyle="primary"
        )
        self.usernameentry.pack(pady=10)
        self.usernameentry.insert(0, "Email")
        self.usernameentry.bind(
            "<FocusIn>", lambda e: self.clearplaceholder(e, "username")
        )
        self.usernameentry.bind(
            "<FocusOut>", lambda e: self.restoreplaceholder(e, "username", "Email")
        )

        self.passwordvar = ttk.StringVar()
        self.passwordentry = ttk.Entry(
            self, textvariable=self.passwordvar, width=30, show="", bootstyle="primary"
        )
        self.passwordentry.pack(pady=10)
        self.passwordentry.insert(0, "Password")
        self.passwordentry.bind(
            "<FocusIn>",
            lambda e: (
                self.clearplaceholder(e, "password"),
                self.passwordentry.config(show="•"),
            ),
        )
        self.passwordentry.bind(
            "<FocusOut>", lambda e: self.restoreplaceholder(e, "password", "Password")
        )

        self.usernameentry.bind("<Escape>", lambda e: self.focus_set())
        self.passwordentry.bind("<Escape>", lambda e: self.focus_set())

        self.forgotbtn = ttk.Button(
            self,
            text="Forgot Password?",
            bootstyle="link",
            command=self.showforgotpassworddialog,
        )
        self.forgotbtn.pack(pady=5)

        self.loginbtn = ttk.Button(
            self, text="Login", bootstyle="success", width=15, command=self.login
        )
        self.loginbtn.pack(pady=10)

        self.registerbtn = ttk.Button(
            self,
            text="Register",
            command=self.registercallback,
            bootstyle="outline",
            width=15,
        )
        self.registerbtn.pack(pady=5)

    def clearplaceholder(self, event, field):
        entry = event.widget
        if field == "username" and entry.get() == "Email":
            entry.delete(0, "end")
        elif field == "password" and entry.get() == "Password":
            entry.delete(0, "end")

    def restoreplaceholder(self, event, field, placeholder):
        entry = event.widget
        if field == "username" and not entry.get():
            entry.insert(0, placeholder)
        elif field == "password" and not entry.get():
            entry.insert(0, placeholder)
            entry.config(show="")

    def showforgotpassworddialog(self):
        currentemail = (
            self.usernamevar.get() if self.usernamevar.get() != "Email" else ""
        )

        dialog = ttk.Toplevel(self)
        dialog.title("Reset Password")
        dialog.geometry("450x400")
        dialog.resizable(False, False)
        self.centerwindow(dialog)

        dialog.grab_set()

        ttk.Label(
            dialog,
            text="Reset Password",
            font=("Helvetica", 16, "bold"),
            bootstyle="primary",
        ).pack(pady=(20, 15))

        if currentemail:
            emailframe = ttk.Frame(dialog)
            emailframe.pack(fill="x", padx=20, pady=5)

            ttk.Label(
                emailframe,
                text="Send reset link to your account email:",
                font=("Helvetica", 10),
                bootstyle="secondary",
            ).pack(anchor="w")

            ttk.Label(
                emailframe,
                text=currentemail,
                font=("Helvetica", 10, "bold"),
                bootstyle="primary",
            ).pack(anchor="w", pady=(0, 10))

            ttk.Button(
                emailframe,
                text="Send to this email",
                bootstyle="success",
                command=lambda: self.sendresetemail(dialog, currentemail),
            ).pack(pady=(0, 20))

            ttk.Separator(dialog).pack(fill="x", padx=20, pady=5)

            ttk.Label(
                dialog,
                text="Or send to another email:",
                font=("Helvetica", 10, "bold"),
                bootstyle="secondary",
            ).pack(pady=(5, 5))

        else:
            ttk.Label(
                dialog,
                text="Enter email to receive an 8-digit code:",
                font=("Helvetica", 10, "bold"),
                bootstyle="secondary",
            ).pack(pady=(0, 5))

        self.altemailvar = ttk.StringVar()
        altemailframe = ttk.Frame(dialog)
        altemailframe.pack(pady=10)

        altemailentry = ttk.Entry(
            altemailframe,
            textvariable=self.altemailvar,
            width=30,
            bootstyle="primary",
        )
        altemailentry.pack(side="left", padx=(0, 5), ipady=3)

        ttk.Button(
            altemailframe,
            text="Send",
            bootstyle="success-outline",
            command=lambda: self.validateandsend(dialog, True),
        ).pack(side="left")

        btnframe = ttk.Frame(dialog)
        btnframe.pack(pady=25)

        ttk.Button(
            btnframe,
            text="Cancel",
            bootstyle="outline-secondary",
            command=dialog.destroy,
        ).pack(side="left", padx=5)

        altemailentry.focus()
        altemailentry.bind(
            "<Return>", lambda e: self.validateandsend(dialog, True)
        )

    def validateandsend(self, dialog, usealt=False):
        if usealt:
            email = self.altemailvar.get()
            if not email:
                ttk.dialogs.Messagebox.show_error(
                    "Please enter an email address", "Error"
                )
                return
        else:
            email = (
                self.usernamevar.get() if self.usernamevar.get() != "Username" else ""
            )
            if not email:
                return

        self.sendresetemail(dialog, email)

    def sendresetemail(self, dialog, email):
        try:
            response = Post(
                "https://api.scamsight.app/resetpassword", json={"email": email}
            )
            if response.status_code == 400:
                ttk.dialogs.Messagebox.show_error(
                    "Provided email address not found in database.", "Password Reset Error"
                )
            elif response.status_code == 429:
                ttk.dialogs.Messagebox.show_error(
                    "Too many requests. Please try again later.", "Error"
                )

        except Exception:
            ttk.dialogs.Messagebox.show_error(
                "An internal error occurred. Please try again later.", "Server Error"
            )
            return


        dialog.destroy()

        self.showverificationdialog(email)

    def showverificationdialog(self, email):
        dialog = ttk.Toplevel(self)
        dialog.title("Reset Password")
        dialog.geometry("500x750")
        dialog.resizable(False, False)
        self.centerwindow(dialog)
        dialog.transient(self)
        dialog.grab_set()

        container = ttk.Frame(dialog, padding=20)
        container.pack(fill="both", expand=True)

        ttk.Label(
            container,
            text="Reset Password",
            font=("Helvetica", 16, "bold"),
            bootstyle="primary",
        ).pack(pady=(0, 15))

        ttk.Label(
            container,
            text=f"Enter the 8-digit code sent to {email} and set a new password:",
            wraplength=400,
            justify="center",
        ).pack(pady=(0, 20))

        codeframe = ttk.Frame(container)
        codeframe.pack(fill="x", pady=(0, 20))

        ttk.Label(
            codeframe, text="Verification Code:", font=("Helvetica", 10, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.codevar = ttk.StringVar()
        codeentry = ttk.Entry(
            codeframe,
            textvariable=self.codevar,
            width=20,
            font=("Helvetica", 14),
            justify="center",
        )
        codeentry.pack(fill="x", pady=5)
        codeentry.focus_set()

        passwordframe = ttk.LabelFrame(
            container, text="New Password", bootstyle="primary", padding=10
        )
        passwordframe.pack(fill="x", pady=(0, 20))

        ttk.Label(passwordframe, text="New Password:", font=("Helvetica", 10)).pack(
            anchor="w", pady=(0, 5)
        )

        self.newpasswordvar = ttk.StringVar()
        newpasswordentry = ttk.Entry(
            passwordframe, textvariable=self.newpasswordvar, show="•", width=30
        )
        newpasswordentry.pack(fill="x", pady=(0, 10))

        ttk.Label(
            passwordframe, text="Confirm Password:", font=("Helvetica", 10)
        ).pack(anchor="w", pady=(0, 5))

        self.confirmpasswordvar = ttk.StringVar()
        confirmpasswordentry = ttk.Entry(
            passwordframe, textvariable=self.confirmpasswordvar, show="•", width=30
        )
        confirmpasswordentry.pack(fill="x", pady=(0, 10))

        btnframe = ttk.Frame(container)
        btnframe.pack(fill="x", pady=20)

        ttk.Button(
            btnframe,
            text="Cancel",
            bootstyle="outline-secondary",
            command=dialog.destroy,
            width=15,
        ).pack(side="left", padx=(0, 10))

        ttk.Button(
            btnframe,
            text="Submit",
            bootstyle="success",
            command=lambda: self.verifyandreset(dialog, email),
            width=15,
        ).pack(side="right")
        
        feedbackframe = ttk.Frame(container)
        feedbackframe.pack(fill="x", pady=(10, 0))

        self.feedbackbtn = ttk.Button(
            feedbackframe,
            text="Get Password Feedback",
            bootstyle="info",
            width=20,
            command=self.passwordfeedback,
        )
        self.feedbackbtn.pack()

        dialog.bind("<Return>", lambda e: self.verifyandreset(dialog, email))
        dialog.bind("<Escape>", lambda e: dialog.destroy())

    def verifyandreset(self, dialog, email):
        code = self.codevar.get().strip()
        newpassword = self.newpasswordvar.get().strip()
        confirmpassword = self.confirmpasswordvar.get().strip()

        if len(code) != 8 or not code.isdigit():
            ttk.dialogs.Messagebox.show_error(
                "Please enter a valid 8-digit code", "Error", parent=dialog
            )
            return

        if not newpassword or not confirmpassword:
            ttk.dialogs.Messagebox.show_error(
                "Please fill in both password fields", "Error", parent=dialog
            )
            return

        if newpassword != confirmpassword:
            ttk.dialogs.Messagebox.show_error(
                "Passwords do not match", "Error", parent=dialog
            )
            return

        try:
            response = Post(
                "https://api.scamsight.app/resetpassword",
                json={"email": email, "code": code, "newpwd": newpassword},
            )
            
            if response.status_code == 200:
                ttk.dialogs.Messagebox.show_info(
                    "Password reset successfully! You can now login.", "Success", parent=dialog
                )
                dialog.destroy()
            elif response.status_code == 400:
                ttk.dialogs.Messagebox.show_error(
                    "Invalid 8-digit code.", "Password Reset Error", parent=dialog
                )
            elif response.status_code == 500:
                ttk.dialogs.Messagebox.show_error(
                    "An internal error occurred. Please try again later.", "Server Error", parent=dialog
                )
            elif response.status_code == 429:
                ttk.dialogs.Messagebox.show_error(
                    "Too many requests. Please try again later.", "Server Error", parent=dialog
                )
                
        except Exception:
            ttk.dialogs.Messagebox.show_error(
                "An internal error occurred. Please try again later.", "Server Error", parent=dialog
            ) 
            
    def centerwindow(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"+{x}+{y}")
