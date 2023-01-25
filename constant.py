from tkinter import *
from tkinter import messagebox
from tkinter.messagebox import *
from tkinter.filedialog import *

# Colors
PURPLE = "#8B5CF6"
YELLOW = "#816300"
LIGHT  = "#CDAA6E"
LIME   = "#6fb10e"
DARKER = "#0d1117"
DARK   = "#1F2937"
DKGRAY = "#313131"
GRAY   = "#545454"


# keyboard match for Thai and English button
alphabets = {
    "1": "ๅ", "!": "+", "2": "/", "@": "๑", "3": "-", "#": "๒", "4": "ภ", "$": "๓",
    "5": "ถ", "%": "๔", "6": "ุ", "^": "ู", "7": "ึ", "&": "฿", "8": "ค", "*": "๕",
    "9": "ต", "(": "๖", "0": "จ", ")": "๗", "-": "ข", "_": "๘", "=": "ช", "+": "๙",
    "q": "ๆ", "Q": "๐", "w": "ไ", "W": "\"", "e": "ำ", "E": "ฎ", "r": "พ", "R": "ฑ",
    "t": "ะ", "T": "ธ", "y": "ั", "Y": "ํ", "u": "ี", "U": "๊", "i": "ร", "I": "ณ",
    "o": "น", "O": "ฯ", "p": "ย", "P": "ญ", "[": "บ", "{": "ฐ", "]": "ล", "}": ",",
    "a": "ฟ", "A": "ฤ", "s": "ห", "S": "ฆ", "d": "ก", "D": "ฏ", "f": "ด", "F": "โ",
    "g": "เ", "G": "ฌ", "h": "้", "H": "็", "j": "่", "J": "๋", "k": "า", "K": "ษ",
    "l": "ส", "L": "ศ", ";": "ว", ":": "ซ", "'": "ง", "\"": ".", "z": "ผ", "Z": "(",
    "x": "ป", "X": ")", "c": "แ", "C": "ฉ", "v": "อ", "V": "ฮ", "b": "ิ", "B": "ฺ",
    "n": "ื", "N": "์", "m": "ท", "M": "?", ",": "ม", "<": "ฒ", ".": "ใ", ">": "ฬ",
    "/": "ฝ", "?": "ฦ", "\\": "ฃ", "\\": "ฅ"
}


# Hoover Custom Button
class HooverButton(Button):
    def __init__(self, *args, **kwargs):
        Button.__init__(self, *args, **kwargs)
        self["borderwidth"] = 0
        self["width"] = 10
        self["fg"] = "white"
        self["bg"] = GRAY
        self["cursor"] = "hand2"
        self["activeforeground"] = "white"
        self["activebackground"] = DARKER
        self["disabledforeground"] = DARKER

        self.bind('<Enter>', lambda e: self.config(background=PURPLE))
        self.bind('<Leave>', lambda e: self.config(background=GRAY))