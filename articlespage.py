import os
import csv
import ttkbootstrap as ttk
from tkinter import Toplevel, Text, Scrollbar
from Scripts.quantumpasswordtime import QuantumPasswordTime
from Scripts.classicalcomputertime import ClassicalPasswordTime

# CONF
ARTICLES = [
    {"title": "How Fast Do Passwords Get Cracked?", "description": "Learn how computers crack passwords, and the rapidly-approaching future of password cracking."},
    {"title": "How Does AI Affect Security on the Internet?", "description": "Explore how rapidly-evolving AI affects your security and privacy on the internet."},
    {"title": "What is the Deal With Biometrics and Their Security?", "description": "Find out what biometrics are, what makes them helpful, and what makes them dangerous."},
    {"title": "What is the Craze With Cryptocurrencies?", "description": "Learn what cryptocurrencies are, the benefits, the downsides, and the controversies with it."}
]
QUANTUMRATES = {
    "No hashing": 1e126,
    "MD5": 1e75,
    "SHA-1": 1e74,
    "bcrypt": 1e4,
    "Argon2id": 1e3
}

CLASSICALRATES = {
    "No hashing": 1e60,
    "MD5": 1e9,
    "SHA-1": 1e8,
    "bcrypt": 1e4,
    "Argon2id": 1e3
}

hashingoptionsclassical = ["No hashing — near infinite guesses/second", "MD5 — 10⁹ gusses/second", "SHA-1 — 10⁸ guesses/second", "bcrypt — 10⁴ guesses/second", "Argon2id — 10³ guesses/second"]


class ArticlesPage(ttk.Frame):
    def __init__(self, master, sidebarfuncs):
        super().__init__(master)
        self.sidebarfuncs = sidebarfuncs
        self.createwidgets()
        self.pack_propagate(False)
        
    def quantumactivity(self):
        window = ttk.Toplevel(self)
        window.title("Quantum Password Cracking")
        
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = sw // 4, sh // 4
        x, y = (sw - w) // 2, (sh - h) // 2
        
        window.geometry(f"{w}x{h}+{x}+{y}")
        window.resizable(False, False)
        
        title = ttk.Label(window, text="Hashing is a way to take any length of text and turn it into a fixed length. Methods such as Argon2id and bcrypt are built to take a while than other methods. Remember, quantum computers are fundamentally different than normal computers and will produce some unexpected results with the options below:", anchor="center", font=("Helvetica", 9), wraplength=window.winfo_screenwidth() // 4 - 20)
        title.pack(pady=5)
        
        optionsrow = ttk.Frame(window)
        optionsrow.pack(padx=10, pady=10, fill="x")
        
        quantumornotvar = ttk.StringVar(value="Quantum computer")
        quantumornotoptions = ["Quantum computer", "Classical computer"]
        
        quantumornotdropdown = ttk.OptionMenu(optionsrow, quantumornotvar, quantumornotoptions[0], *quantumornotoptions)
        quantumornotdropdown.config(width=10)
        quantumornotdropdown.pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        hashingoptionsclassical = ["No hashing — near infinite guesses/second", "MD5 — 10⁹ hashes/second", "SHA-1 — 10⁸ hashes/second", "bcrypt — 10⁴ hashes/second", "Argon2id — 10³ hashes/second"]
        hashingoptionsquantum = ["No hashing — near infinite guesses/second", "MD5 — 10⁷⁵ hashes/second", "SHA-1 — 10⁷⁴ hashes/second", "bcrypt — 10⁴ hashes/second", "Argon2id — 10³ hashes/second"]

        hashingvar = ttk.StringVar(value="No hashing — near infinite guesses/second")
        hashingdropdown = ttk.OptionMenu(optionsrow, hashingvar, hashingoptionsquantum[0], *hashingoptionsquantum)
        hashingdropdown.config(width=10)
        hashingdropdown.pack(side="left", expand=True, fill="x", padx=(0, 5))


        def update(*args):
            menu = hashingdropdown["menu"]
            menu.delete(0, "end")
            
            if quantumornotvar.get() == "Quantum computer":
                options = hashingoptionsquantum
            else:
                options = hashingoptionsclassical
            for option in options:
                menu.add_command(label=option, command=lambda value=option: hashingvar.set(value))
            
            hashingvar.set(options[0])
        
        quantumornotvar.trace_add("write", update)

        rowframe = ttk.Frame(window)
        rowframe.pack(padx=10, pady=10, fill="x")
        
        entryvar = ttk.StringVar(value="Password")
        entry = ttk.Entry(rowframe, textvariable=entryvar)
        entry.pack(side="left", expand=True, fill="x")

        def clearplaceholder(e):
            if entryvar.get() == "Password":
                entryvar.set("")
                
        def restoreplaceholder(e):
            if not entryvar.get():
                entryvar.set("Password")   
                
        entry.bind("<FocusIn>", clearplaceholder)
        entry.bind("<FocusOut>", restoreplaceholder)
        
        def submit():
            isquantumornot = quantumornotvar.get()

            if isquantumornot == "Quantum computer":
                hashingstr = hashingvar.get()
                splitted = hashingstr[:hashingstr.index("—")].rstrip(" ")
                
                hashingrate = QUANTUMRATES.get(splitted)
                result = QuantumPasswordTime(entryvar.get(), hashingrate)
            else:
                hashingstr = hashingvar.get()
                splitted = hashingstr[:hashingstr.index("—")].rstrip(" ")

                hashingrate = CLASSICALRATES.get(splitted)
                result = ClassicalPasswordTime(entryvar.get(), hashingrate)
            output.config(text=result)

        submit = ttk.Button(rowframe, text="Go!", command=submit)
        submit.pack(side="left", padx=(5, 0))
        
        output = ttk.Label(window, text="", anchor="w", justify="left",  wraplength=window.winfo_screenwidth() // 4 - 20)
        output.pack(padx=10, pady=(5, 10), fill="x")

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
            bootstyle="primary", 
            width=20,
            command=self.sidebarfuncs["articles"]
        ).pack(fill="x", pady=4, ipady=4)

        ttk.Button(
            btncontainer,
            text="Settings",
            bootstyle="secondary-outline",
            width=20,
            command=self.sidebarfuncs["settings"],
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
        content.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        canvas = ttk.Canvas(content)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(content, orient="vertical", command=canvas.yview)
        scrollableframe = ttk.Frame(canvas)

        scrollableframe.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        def mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind("<MouseWheel>", mousewheel)
        scrollableframe.bind("<MouseWheel>", mousewheel)

        canvas.create_window((0, 0), window=scrollableframe, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        ttk.Label(
            scrollableframe,
            text="Educational Articles",
            font=("Helvetica", 20, "bold"),
            bootstyle="primary",
            background="#222222"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        for i, article in enumerate(ARTICLES):
            row = i // 2 
            column = i % 2
            
            outer = ttk.Frame(scrollableframe)
            outer.grid(row=row+1, column=column, padx=75, pady=20, sticky="nsew")
            outer.configure(style="Outer.TFrame")

            card = ttk.Frame(
                scrollableframe, 
                bootstyle="dark",
                borderwidth=0.5,
                relief="solid",
                padding=20
            )
            card.grid(row=row+1, column=column, padx=75, pady=20, sticky="nsew")
            card.grid_propagate(False)

            title = ttk.Label(
                card,
                text=article["title"],
                font=("Helvetica", 14),
                bootstyle="primary",
                wraplength=280,
                anchor="center",
                justify="center",
                background="#303030"
            )
            title.pack(pady=(0, 10))

            desc = ttk.Label(
                card, 
                text=article["description"],
                font=("Helvetica", 10),
                wraplength=280,
                justify="center",
                background="#303030"
            )
            desc.pack(pady=(0, 15))

            ttk.Button(
                card,
                text="Read More",
                bootstyle="outline-primary",
                command=lambda a = article: self.openarticle(a)
            ).pack()

        scrollableframe.grid_rowconfigure(0, weight=1)
        scrollableframe.grid_columnconfigure(0, weight=1)
        scrollableframe.grid_columnconfigure(1, weight=1)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def openarticle(self, article):
        viewerwindow = Toplevel(self)
        viewerwindow.title(article["title"])
        
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = sw // 2, sh // 3
        x, y = (sw - w) // 2, (sh - h) // 3
        
        viewerwindow.geometry(f"{w}x{h}+{x}+{y}")
        viewerwindow.resizable(False, False)

        scrollbar = Scrollbar(viewerwindow)
        scrollbar.pack(side="right", fill="y")
        
        text =  Text(viewerwindow, wrap="word", yscrollcommand=scrollbar.set, font=("Helvetica", 12), state="normal")
        text.pack(side="left", fill="both", expand=True)
        text.tag_configure("bold", font=("Helvetica", 14, "bold"))
        text.tag_configure("header", font=("Helvetica", 24, "bold"))
        text.tag_configure("normal", font=("Helvetica", 12))
        
        scrollbar.config(command=text.yview)
        
        index = next(i for i, a in enumerate(ARTICLES) if a["title"] == article["title"])

        if not isinstance(index, int) or index is None:
            return
        
        content = []
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"./Articles/{index}.csv"), newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                content.append((row["text"], row["style"]))
        
        for line, tag in content:
            text.insert("end", line, tag)
        
        if index == 0:
            btn = ttk.Button(text, text="Try it out!", command=self.quantumactivity, width=25)
            
            text.window_create("end", window=btn)
            
        text.config(state="disabled")