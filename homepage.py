import os
import asyncio
import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageGrab
from Scripts.screenshot import Screenshot
from Scripts.choosefile import ChooseFile
from Scripts.ocr import OCR

# CONF
IMAGEFORMATS = list(Image.registered_extensions().keys())

class HomePage(ttk.Frame):
    def __init__(self, master, sidebarfuncs):
        super().__init__(master)
        self.sidebarfuncs = sidebarfuncs
        self.createwidgets()
        self.pack_propagate(False)

    def displayimage(self, img: Image.Image):
        frame = self.inputframe

        if hasattr(self, "imglabel") and self.imglabel.winfo_exists():
            self.imglabel.destroy()
            self.imglabelimg = None

        frame.update_idletasks()

        maxw = frame.winfo_width() - 20
        maxh = frame.winfo_height() // 2 - 10

        scale = min(maxw / img.width, maxh / img.height, 1)
        neww = int(img.width * scale)
        newh = int(img.height * scale)

        resized = img.resize((neww, newh), Image.Resampling.BOX)
        tkimg = ImageTk.PhotoImage(resized)

        label = ttk.Label(frame, image=tkimg)
        label.image = tkimg
        label.place(
            x=(maxw - neww) // 2, y=(frame.winfo_height() // 2) + (maxh - newh) // 2
        )

        self.imglabel = label
        self.imglabelimg = img

    def choosefile(self):
        imagepath = ChooseFile(IMAGEFORMATS, "Images")
        if imagepath and imagepath.endswith(tuple(IMAGEFORMATS)):
            img = Image.open(imagepath)
            self.displayimage(img)

    def screenshot(self):
        Screenshot("tempss.png")
        img = Image.open("tempss.png")
        self.displayimage(img)
        os.remove("tempss.png")

    def pasteimage(self, event):
        try:
            img = ImageGrab.grabclipboard()
            if img:
                self.displayimage(img)
        except Exception:
            pass

    async def _ocr(self):
        if self.imglabelimg:
            img = self.imglabelimg
            self.analysis.config(text="")

        result = await OCR(img)
        if isinstance(result, int):
            if result == 401:
                ttk.dialogs.Messagebox.show_error(
                    "Authentication token required. Please close and reopen the app.", "Error"
                )
            elif result == 403:
                ttk.dialogs.Messagebox.show_error(
                    "Invalid or expired token. Please close and reopen the app.", "Error"
                )
            elif result == 400:
                ttk.dialogs.Messagebox.show_error(
                    "Bad OCR. Are you sure the image has text?", "Error"
                )
            elif result == 500:
                ttk.dialogs.Messagebox.show_error(
                    "An internal server error occurred. Please try again later.", "Error"
                )
            elif result == 429:
                ttk.dialogs.Messagebox.show_error(
                    "Too many requests. Please try again later.", "Server Error"
                )
                

        self.analysis.config(text=result)

    def ocr(self):
        asyncio.run(self._ocr())

    def updateanalysiswraplen(self, event):
        self.analysis.config(wraplength=event.width - 10)

    def createwidgets(self):
        self.bind_all("<Control-v>", self.pasteimage)

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
            bootstyle="primary",
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

        content = ttk.Frame(self, bootstyle="dark")
        content.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)

        inputframe = ttk.Frame(content)
        inputframe.grid(row=0, column=0, sticky="nswe")
        inputframe.pack_propagate(False)
        self.inputframe = inputframe

        ttk.Label(
            inputframe,
            text="Upload an image",
            font=("Helvetica", 12, "bold"),
            foreground="#5dade2",
            bootstyle="primary",
        ).pack(pady=(20, 20))

        btnframe = ttk.Frame(inputframe)
        btnframe.pack(pady=10)

        ttk.Button(
            btnframe,
            text="Choose File",
            bootstyle="success-outline",
            width=15,
            command=self.choosefile,
        ).pack(side="left", padx=5)

        ttk.Button(
            btnframe,
            text="Take Screenshot",
            bootstyle="info-outline",
            width=15,
            command=self.screenshot,
        ).pack(side="left", padx=5)

        ttk.Label(
            inputframe,
            text="Pick a file, take a screenshot, or paste (Ctrl+V) an image here",
            font=("Helvetica", 9),
        ).pack(pady=20)

        analysisframe = ttk.Frame(content, bootstyle="secondary")
        analysisframe.grid(row=1, column=0, sticky="nswe")
        analysisframe.pack_propagate(False)

        self.analysis = ttk.Label(
            analysisframe,
            text="Image analysis will appear here...",
            font=("Helvetica", 12),
            foreground="#bbbbbb",
            background="#444444",
            bootstyle="primary",
            anchor="nw",
            justify="left",
            wraplength=analysisframe.winfo_width(),
        )
        self.analysis.pack(fill="both", expand=True, padx=5, pady=5)

        analysisframe.bind("<Configure>", self.updateanalysiswraplen)

        ttk.Button(
            sidebar, 
            text="Submit", 
            bootstyle="warning", 
            width=20, 
            command=self.ocr
        ).pack(side="bottom", pady=20, padx=10, ipady=4)