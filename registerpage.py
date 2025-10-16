import ttkbootstrap as ttk
from tkinter import Toplevel, Text, Scrollbar
from Scripts.register import Register
from Scripts.passwordfeedback import PasswordFeedback


class RegisterPage(ttk.Frame):
    def __init__(self, master, logincallback):
        super().__init__(master)
        self.logincallback = logincallback
        self.createwidgets()
        self.focus_set()

    def register(self):
        if not self.agreevar.get():
            ttk.dialogs.Messagebox.show_info(
                "You must agree to the Terms of Service and Privacy Policy before registering.",
                "Agreement Required",
            )
            return
        
        response = Register(self.emailentry.get(), self.passwordentry.get())
        if type(response) == int:
            if response == 200:
                ttk.dialogs.Messagebox.show_info(
                    "You have successfully registered! Please check the inbox or spam of the email you used to register to verify it.",
                    "Registration Success!",
                )
            elif response == 400:
                ttk.dialogs.Messagebox.show_error(
                    "Email and password required.", "RegistrationError"
                )
            elif response == 401:
                ttk.dialogs.Messagebox.show_error(
                    "Email already registered.", "Registration Server Error"
                )
            elif response == 500:
                ttk.dialogs.Messagebox.show_error(
                    "An internal server error occurred. Please try again later.", "Server Error"
                )
            elif response == 429:
                ttk.dialogs.Messagebox.show_error(
                    "Too many requests. Please try again later.", "Server Error"
                )
        else:
            ttk.dialogs.Messagebox.show_info(response, "Registration Error")


    def showtos(self):
        viewerwindow = Toplevel(self)
        viewerwindow.title("ScamSight Privacy Policy")
        
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = sw // 2, sh // 3
        x, y = (sw - w) // 2, (sh - h) // 3
        
        viewerwindow.geometry(f"{w}x{h}+{x}+{y}")
        viewerwindow.resizable(False, False)
        
        scrollbar = Scrollbar(viewerwindow)
        scrollbar.pack(side="right", fill="y")
        
        text = Text(viewerwindow, wrap="word", yscrollcommand=scrollbar.set, font=("Helvetica", 12), state="normal")
        text.pack(side="left", fill="both", expand=True)
        text.tag_configure("bold", font=("Helvetica", 14, "bold"))
        text.tag_configure("header", font=("Helvetica", 24, "bold"))
        text.tag_configure("normal", font=("Helvetica", 12))
        
        scrollbar.config(command=text.yview)

        content = [
            ("Effective Date:\n", "bold"),
            ("Last Updated:\n\n", "bold"),
            ("Accounts\n", "header"),
            ("• You are responsible for maintaining the confidentiality of your login credentials; ScamSight does not store any credentials in an accessible or decryptable form.\n", "normal"),
            ("• You are responsible for all activity on your account.\n", "normal"),
            ("• Misusing, abusing, or violating the Terms of Service subjects your account to deletion.\n\n", "normal"),
            ("Acceptable Use\n", "header"),
            ("• ScamSight may only be used for lawful activities.\n", "normal"),
            ("• You agree to not use the app to generate, share, or promote harmful, or misleading content.\n", "normal"),
            ("• You agree not to tamper or abuse the ScamSight server. All user-end functions are available as open source.\n", "normal"),
            ("• You agree not to misuse the OpenRoute functionality in ways that violate their rights.\n\n", "normal"),
            ("Intellectual Property\n", "header"),
            ("• ScamSight, its features, and design, are open source, allowing free access to all.\n", "normal"),
            ("• ScamSight may not be rebranded for commercial use without explicit, written consent.\n\n", "normal"),
            ("Service Availability\n", "header"),
            ("• ScamSight is provided “as is” and “as available.”\n", "normal"),
            ("• We do not guarantee uninterrupted or error-free operation.\n", "normal"),
            ("• We may discontinue features at any time. All changes will be posted on GitHub and the official scamsight.app website with notice if applicable.\n\n", "normal"),
            ("Limitation of Liability\n", "header"),
            ("• ScamSight is not responsible for damages resulting from the use or inability to use the app.\n", "normal"),
            ("• We make no warranties beyond those required by law.\n", "normal"),
            ("• Outputs made by any generative AI (Artificial Intelligence) may not be accurate. Please verify all information outputted.\n\n", "normal"),
            ("Terminations\n", "header"),
            ("• You may suspend using ScamSight at any time.\n", "normal"),
            ("• We may terminate your access to ScamSight if you violate any of these Terms or if required by law.\n\n", "normal"),
            ("Governing Law\n", "header"),
            ("• The Terms are governed by the laws of the United States of America and the state in which we are headquartered, without regard to conflict of law provisions.\n\n", "normal"),
            ("Privacy\n", "header"),
            ("• Your use of ScamSight is also governed by our Privacy Policy.\n", "normal"),
            ("• Please review the Privacy Policy to understand how we use and safeguard your data.\n\n", "normal"),
            ("Contact Us\n", "header"),
            ("• For questions or concerns about privacy, please contact us through the in-app support form.\n", "normal"),
        ]

        for line, tag in content:
            text.insert("end", line, tag)

        text.config(state="disabled")

    def showprivacypolicy(self):
        viewerwindow = Toplevel(self)
        viewerwindow.title("ScamSight Terms of Service")
        
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = sw // 2, sh // 3
        x, y = (sw - w) // 2, (sh - h) // 3
        viewerwindow.geometry(f"{w}x{h}+{x}+{y}")
        viewerwindow.resizable(False, False)
        
        scrollbar = Scrollbar(viewerwindow)
        scrollbar.pack(side="right", fill="y")
        
        text = Text(
            viewerwindow,
            wrap="word",
            yscrollcommand=scrollbar.set,
            font=("Helvetica", 12),
            state="normal"
        )
        text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text.yview)

        text.tag_configure("bold", font=("Helvetica", 14, "bold"))
        text.tag_configure("header", font=("Helvetica", 24, "bold"))
        text.tag_configure("normal", font=("Helvetica", 12))

        content = [
            ("Effective Date:\n", "bold"),
            ("Last Updated:\n\n", "bold"),
            ("Introduction\n", "header"),
            ("ScamSight (“we”, “our”, “the app”) values your privacy. This Privacy Policy explains what information we collect, how we use it, and your rights as a user of our Windows application.\n\n", "normal"),
            ("Information We Collect\n", "header"),
            ("• We require an email address to create an account. Emails are hashed and salted with up-to-date measures, making them inaccessible to server administrators.\n", "normal"),
            ("• Your login credentials and tokens are stored securely to allow easy account access.\n", "normal"),
            ("• ScamSight uses OCR (Optical Character Recognition) on screenshots the user provides and sends processed data to TogetherGPT to deliver core app functionality. This data is only used to provide the service and is not stored beyond the scope of the API request.\n", "normal"),
            ("• No other personal or sensitive data is collected. We do not track location, device info, IP addresses, or any other analytics.\n\n", "normal"),
            ("How We Use Your Data\n", "header"),
            ("• Verifying your login credentials securely\n", "normal"),
            ("• Using extracted text via OCR (Optical Character Recognition), TogetherGPT is used to generate responses.\n\n", "normal"),
            ("Data Storage and Security\n", "header"),
            ("• Emails are hashed with modern, secure algorithms with salt.\n", "normal"),
            ("• User logins are permanently stored in a hashed form.\n", "normal"),
            ("• All communications with our servers use HTTPS and RSA encryption.\n", "normal"),
            ("• Server access is restricted, and administrators cannot access hashed emails directly.\n\n", "normal"),
            ("User Rights\n", "header"),
            ("• Users may request access to account information or correct inaccuracies via the in-app contact form.\n", "normal"),
            ("• Users may request the deletion of their accounts and associated data.\n", "normal"),
            ("• Users may withdraw consent to account storage via account deletion.\n\n", "normal"),
            ("Legal Compliance\n", "header"),
            ("• ScamSight is designed as a Windows application for general users. We comply with applicable U.S. privacy laws, including CCPA for California residents.\n", "normal"),
            ("• We do not knowingly collect data from users under 13 years of age. All users must be of age according to local law to use this app.\n\n", "normal"),
            ("Third-Party Services\n", "header"),
            ("• ScamSight uses TogetherGPT to process OCR (Optical Character Recognition) data. Only necessary image data is sent to this service to provide this app’s core functionality.\n", "normal"),
            ("• We do not share user emails, login credentials, or other personal information with third parties.\n\n", "normal"),
            ("Contact Us\n", "header"),
            ("• For questions or concerns about privacy, please contact us through the in-app support form.\n", "normal"),
        ]


        for line, tag in content:
            text.insert("end", line, tag)

        text.config(state="disabled")
    
    def passwordfeedback(self):
        PasswordFeedback(self.passwordvar.get())
        
    def createwidgets(self):
        self.backbtn = ttk.Button(
            self, text="← Back", command=self.logincallback, bootstyle="link"
        )
        self.backbtn.pack(anchor="nw", padx=10, pady=10)

        self.logo = ttk.Label(
            self, text="ScamSight", font=("Helvetica", 24, "bold"), bootstyle="primary"
        )
        self.logo.pack(pady=(20, 30))

        self.subtitle = ttk.Label(
            self, text="Register", font=("Helvetica", 12), bootstyle="secondary"
        )
        self.subtitle.pack(pady=(0, 20))

        self.emailvar = ttk.StringVar()
        self.emailentry = ttk.Entry(
            self, textvariable=self.emailvar, width=30, bootstyle="primary"
        )
        self.emailentry.pack(pady=10, anchor="center")
        self.emailentry.insert(0, "Email")
        self.emailentry.bind("<FocusIn>", lambda e: self.clearplaceholder(e, "email"))
        self.emailentry.bind(
            "<FocusOut>", lambda e: self.restoreplaceholder(e, "email", "Email")
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

        self.feedbackbtn = ttk.Button(
            self, text="Get Password Feedback", bootstyle="info", width=20, command=self.passwordfeedback
        )
        self.feedbackbtn.pack(pady=5)

        self.emailentry.bind("<Escape>", self.handleescape)
        self.passwordentry.bind("<Escape>", self.handleescape)

        self.emailentry.bind("<Button-1>", self.handletextentryclick)
        self.passwordentry.bind("<Button-1>", self.handletextentryclick)

        self.registerbtn = ttk.Button(
            self, text="Register", bootstyle="sucess", width=15, command=self.register
        )
        self.registerbtn.pack(pady=10)
        
        style = ttk.Style()
        style.configure("Custom.TCheckbutton", font=("Helvetica", 8))
        
        self.agreevar = ttk.BooleanVar(value=False)
        self.agreecheckbox = ttk.Checkbutton(self, text="I agree to the Terms of Service and Privacy Policy", variable=self.agreevar, bootstyle="secondary", style="Custom.TCheckbutton")
        self.agreecheckbox.pack(pady=0)

        self.legalframe = ttk.Frame(self)
        self.legalframe.pack(pady=10)

        self.tosbtn = ttk.Button(
            self.legalframe, text="Terms of Service", bootstyle="link", command=self.showtos
        )
        self.tosbtn.pack(side="left", padx=5)
        
        ttk.Label(
            self.legalframe,
            text="•",
        ).pack(side="left", padx=0)

        self.ppbtn = ttk.Button(self.legalframe, text="Privacy Policy", bootstyle="link", command=self.showprivacypolicy)
        self.ppbtn.pack(side="left", padx=5)

    def clearplaceholder(self, event, field):
        entry = event.widget
        if field == "email" and entry.get() == "Email":
            entry.delete(0, "end")
        elif field == "password" and entry.get() == "Password":
            entry.delete(0, "end")

    def restoreplaceholder(self, event, field, placeholder):
        entry = event.widget
        if field == "email" and not entry.get():
            entry.insert(0, placeholder)
        elif field == "password" and not entry.get():
            entry.insert(0, placeholder)
            entry.config(show="")

    def handleescape(self, event):
        if self.focus_get() in (self.emailentry, self.passwordentry):
            self.focus_set()
        else:
            self.logincallback()

    def handletextentryclick(self, event):
        entry = event.widget
        if not entry.select_present():
            entry.focus()