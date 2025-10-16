import os
import json
import ttkbootstrap as ttk
from Scripts.https import Post
from Scripts.encrypt import Encrypt

# CONF
AUTHFILE = os.path.expanduser("~/scamsight.auth.json")

class ContactPage(ttk.Frame):
    def __init__(self, master, sidebarfuncs):
        super().__init__(master)
        self.sidebarfuncs = sidebarfuncs
        self.createwidgets()
        self.pack_propagate(False)

    def sendmessage(self):
        token = ""

        try:
            with open(AUTHFILE) as f:
                authdata = json.load(f)

            token = authdata.get("token")
        except Exception:
            pass

        if not token:
            return

        email = self.emailentry.get()

        issue = self.issuetext.get("1.0", "end-1c")
        encrypted = Encrypt(issue)
        response = Post(
            "https://api.scamsight.app/contactus",
            headers={"Authorization": token, "email": email},
            data=encrypted
        )
        
        if response.status_code == 200:
            ttk.dialogs.Messagebox.show_info(
                    "Successfully sent message! Please allow up to 48 hours for a response before sending another message.", "Success"
                )
        elif response.status_code == 422:
            ttk.dialogs.Messagebox.show_error(
                "Please enter the email you registered this account with. ScamSight does not store emails in their plain form.", "Contact Us Error"
            )
        elif response.status_code == 500:
            ttk.dialogs.Messagebox.show_info(
                "An internal error occurred. Please try again later.", "Server Error"
            )

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
            bootstyle="primary",
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
            bootstyle="secondary-outline", 
            width=20,
            command=self.sidebarfuncs["settings"]
        ).pack(fill="x", pady=4, ipady=4)

        ttk.Button(
            btncontainer, 
            text="Contact Us",
            bootstyle="primary", 
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
        content.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        contactframe = ttk.Frame(content)
        contactframe.grid(row=0, column=0, padx=20, pady=20, sticky="nswe")
        contactframe.grid_rowconfigure(2, weight=1)
        contactframe.grid_columnconfigure(0, weight=1)

        ttk.Label(
            contactframe,
            text="Contact Us",
            font=("Helvetica", 20, "bold"),
            bootstyle="primary",
            anchor="center",
            justify="center"
        ).grid(row=0, column=0, sticky="ew", pady=(0, 20))

        emailframe = ttk.Frame(contactframe)
        emailframe.grid(row=1, column=0, sticky="we", pady=(0, 15))
        emailframe.grid_columnconfigure(1, weight=1)

        ttk.Label(
            emailframe,
            text="Email address:",
            font=("Helvetica", 10),
            bootstyle="primary"
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")

        self.emailentry = ttk.Entry(
            emailframe,
            font=("Helvetica", 10),
            bootstyle="light"
        )
        self.emailentry.grid(row=0, column=1, sticky="we", padx=(0, 20))

        issueframe = ttk.Frame(contactframe)
        issueframe.grid(row=2, column=0, sticky="nswe", pady=(0, 15))
        issueframe.grid_rowconfigure(1, weight=1)
        issueframe.grid_columnconfigure(0, weight=1)

        ttk.Label(
            issueframe,
            text="Describe your issue:",
            font=("Helvetica", 10),
            bootstyle="primary"
        ).grid(row=0, column=0, sticky="w", pady=(0, 5))

        self.issuetext = ttk.Text(
            issueframe,
            font=("Helvetica", 10),
            height=10,
            wrap="word"
        )
        self.issuetext.grid(row=1, column=0, sticky="nswe")

        scrollbar = ttk.Scrollbar(
            issueframe, 
            orient="vertical",
            command=self.issuetext.yview
        )
        scrollbar.grid(row=1, column=1, sticky="ns")
        self.issuetext.config(yscrollcommand=scrollbar.set)

        buttonframe = ttk.Frame(contactframe)
        buttonframe.grid(row=3, column=0, sticky="we", pady=(0, 20))
        buttonframe.grid_columnconfigure(0, weight=1)

        ttk.Button(
            buttonframe,
            text="Send Message",
            bootstyle="warning-outline",
            width=15,
            command=self.sendmessage
        ).grid(row=0, column=0, pady=(0, 10))
