# ScamSight

**Welcome to ScamSight**
This will guide you on how to run the app from this GitHub. There will be two ways: running from Python and compiling the code into an .exe file. To download the .exe directly, download it under "Releases" or from the website (https://scamsight.app).

## Running with Python
1. If not done already, install Python 3.14.0 by running the following command. Command prompt can be opened by pressing the Windows key, then typing "cmd" and pressing enter:
`winget install Python.Python.3.14`
Or install via the official Python website: https://www.python.org/downloads/release/python-3140. If you choose to do this, ensure to click the "Add to PATH" option.

2. Once Python 3.14 is installed, the following command should be run in a new command prompt:
`pip install certifi pillow requests rsa pyaes ttkbootstrap winrt-Windows.Foundation winrt-Windows.Globalization winrt-Windows.Graphics.Imaging winrt-Windows.Media.Ocr winrt-Windows.Storage.Streams`
This will install all the packages needed to run ScamSight:

- Certifi and requests handle HTTPs requests with added security from certifi, which verifies websites are who it says they are.
- Pillow handles images.
- Pyaes and rsa encrypt data for more sensitive information over the internet.
- All winrt packages are for taking text out of inputted images (see ocr.py).

3. Next, on this repository (https://github.com/andy-stern/ScamSight), click the green "Code" button. Then, click "Download ZIP." In File Explorer (Windows key, search "File Explorer"), right click the .zip file you downloaded and click "Extract all..."
From there, a new window in File Explorer will appear. To run ScamSight, find the image that looks like this:
<p align="center">
  <img width="50" height="50" src="https://github.com/user-attachments/assets/921df132-1d1d-4f3d-aa11-5e2a9104f170" />
</p>

To the right of it, press the long area. If you do it correctly, a **path** should appear, or where on your computer you are located. From there, type "cmd" and wait for a window to open.
A command prompt window should appear. From there, type "python main.py" and the ScamSight login page should appear 🥳

## Building from source
1. To build from source, please complete steps 1 and 2 from "Running with Python" and step 3 until typing "python main.py"
2. In the command window from step 3 in "Running with Python", run the following command:
`pip install pyinstaller`
3. Once pyinstaller is successfully installed, run this command to make an .exe file:
`pyinstaller --onefile --windowed --icon "ScamSight.ico" --strip --add-data "articlespage.py;." --add-data "contactspage.py;." --add-data "homepage.py;." --add-data "loginpage.py;." --add-data "registerpage.py;." --add-data "ScamSight.ico;." --add-data "settingspage.py;." --add-data "Scripts;Scripts/" --add-data "Articles;Articles/" "main.py"`
- Onefile makes it one .exe, not an .exe with other files.
- Windowed makes it without a console, so only the ScamSight interface.
- All data added is to ensure all required local scripts are added to the .exe as one file.
4. Finally, double click the .exe and the ScamSight login page should appear 🥳
