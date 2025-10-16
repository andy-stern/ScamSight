import ctypes
from ctypes import wintypes
from typing import List

# CONF
MAXEXTENSIONDISPLAY = 7

def _BuildEL(formats: List[str], label: str) -> str:
    extensionslist = [f"*{ext}" for ext in formats[:MAXEXTENSIONDISPLAY]]
    if len(formats) > MAXEXTENSIONDISPLAY:
        extensionslist.append("...")
    
    labeltext = f"{label} ({', '.join(extensionslist)})"
    patterntext = ";".join(f"*{ext}" for ext in formats)
    return f"{labeltext}\0{patterntext}\0"

def ChooseFile(formats: List[str], label="Custom Files") -> str | None:
    extensions = _BuildEL(formats, label)
    
    class OPENFILENAMEW(ctypes.Structure):
        _fields_ = [
            ("lStructSize", wintypes.DWORD),
            ("hwndOwner", wintypes.HWND),
            ("hInstance", wintypes.HINSTANCE),
            ("lpstrFilter", wintypes.LPCWSTR),
            ("lpstrCustomFilter", wintypes.LPWSTR),
            ("nMaxCustFilter", wintypes.DWORD),
            ("nFilterIndex", wintypes.DWORD),
            ("lpstrFile", wintypes.LPWSTR),
            ("nMaxFile", wintypes.DWORD),
            ("lpstrFileTitle", wintypes.LPWSTR),
            ("nMaxFileTitle", wintypes.DWORD),
            ("lpstrInitialDir", wintypes.LPCWSTR),
            ("lpstrTitle", wintypes.LPCWSTR),
            ("Flags", wintypes.DWORD),
            ("nFileOffset", wintypes.WORD),
            ("nFileExtension", wintypes.WORD),
            ("lpstrDefExt", wintypes.LPCWSTR),
            ("lCustData", wintypes.LPARAM),
            ("lpfnHook", wintypes.LPVOID),
            ("lpTemplateName", wintypes.LPCWSTR),
            ("pvReserved", wintypes.LPVOID),
            ("dwReserved", wintypes.DWORD),
            ("FlagsEx", wintypes.DWORD),
        ]
        
    buffer = ctypes.create_unicode_buffer(260)
    ofnstruct = OPENFILENAMEW()
    ofnstruct.lStructSize = ctypes.sizeof(ofnstruct)
    ofnstruct.lpstrFile = ctypes.cast(buffer, wintypes.LPWSTR)  
    ofnstruct.nMaxFile = 260
    ofnstruct.lpstrFilter = extensions
    ofnstruct.lpstrTitle = "Select a file" 
    
    if ctypes.windll.comdlg32.GetOpenFileNameW(ctypes.byref(ofnstruct)):   
        return buffer.value
    
    return None