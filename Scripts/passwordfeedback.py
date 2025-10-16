import json
import ttkbootstrap as ttk
from .https import Post
from .extractpwdfeatures import Extract

def PasswordFeedback(password: str): 
    if password == "" or password == "Password" or password == "New Password":
        ttk.dialogs.Messagebox.show_error("Please enter a password.", "Error")
        return

    if len(password) < 8:
        ttk.dialogs.Messagebox.show_info("Ensure your password is 8 characters or more.", "Password Feedback")
        return

    features = Extract(password)

    feedback = Post(
        "https://api.scamsight.app/passwordfeedback",
        json=features
    )
    
    if feedback.status_code == 500:
        ttk.dialogs.Messagebox.show_error(
            "An internal server error occurred. Please try again later.", "Server Error"
        )

    feedback = json.loads(json.loads(feedback.text)["feedback"])["choices"][0]["message"]["content"]

    ttk.dialogs.Messagebox.show_info(feedback, "Password Feedback")
