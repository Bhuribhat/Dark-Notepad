import os

from time import strftime
from constant import *


class Notepad:
    def __init__(self, **kwargs):
        self.__size      = 12
        self.__width     = 900
        self.__height    = 700
        self.__file      = None
        self.__bgColor   = DARK
        self.__checkFind = False

        # user's information
        self.__name      = kwargs["name"]
        self.__mail      = kwargs["mail"]
        self.__phone     = kwargs["phone"]
        self.__social    = kwargs["social"]

        # default window width and height
        self.__root      = Tk()
        self.__menuBar   = Menu(self.__root)
        self.__fileMenu  = Menu(self.__menuBar, tearoff=0)
        self.__editMenu  = Menu(self.__menuBar, tearoff=0)
        self.__helpMenu  = Menu(self.__menuBar, tearoff=0)
        self.__zoomMenu  = Menu(self.__menuBar, tearoff=0)
        self.__highlight = Menu(self.__menuBar, tearoff=0)
        self.__decrypt   = Menu(self.__menuBar, tearoff=0)
        self.__textArea  = Text(self.__root, undo=True)

        # To add scrollbar
        self.__scrollBar = Scrollbar(self.__textArea, cursor="arrow")

        try:
            self.__root.wm_iconbitmap("./assets/notepad.ico")
            self.__width  = kwargs['width']
            self.__height = kwargs['height']
        except KeyError:
            pass

        # Set the window text
        self.__root.title("Untitled - Dark Notepad")
        self.__root.bind("<Button-3>", self.popup)
        self.__root.bind("<Control-Up>", self.zoom_in)
        self.__root.bind("<Control-Down>", self.zoom_out)
        self.__root.bind("<Control-o>", self.open_file)
        self.__root.bind("<Control-s>", self.save_file)
        self.__root.bind("<Control-n>", self.clear_file)
        self.__root.bind("<Control-f>", self.find_replace_text)

        # User quits the program (using X button)
        self.__root.protocol("WM_DELETE_WINDOW", self.quit_application)

        # Center the window
        screenWidth  = self.__root.winfo_screenwidth()
        screenHeight = self.__root.winfo_screenheight()

        # For left-align and right-align
        left = (screenWidth  / 2) - (self.__width  / 2)
        top  = (screenHeight / 2) - (self.__height / 2)

        # For top and bottom
        self.__root.geometry('%dx%d+%d+%d' % (self.__width, self.__height, left, top))

        # To make the textarea auto resizable
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)

        # Add controls (widget)
        self.__textArea.grid(sticky=N + E + S + W)
        self.__textArea.configure(bg=DARK, fg="white", font=f"Consolas 12",
                                  insertbackground="orange", selectbackground=YELLOW)

        # To give a feature of File
        self.__menuBar.add_cascade(label="File", menu=self.__fileMenu)
        self.__fileMenu.add_command(label="New", command=self.clear_file)
        self.__fileMenu.add_command(label="New Window", command=self.new_file)
        self.__fileMenu.add_command(label="Open", command=self.open_file)
        self.__fileMenu.add_command(label="Save As", command=self.save_as)
        self.__fileMenu.add_command(label="Save", command=self.save_file)

        self.__fileMenu.add_separator()
        self.__fileMenu.add_command(label="Exit", command=self.quit_application)

        # To give a feature of Edit
        self.__menuBar.add_cascade(label="Edit", menu=self.__editMenu)
        self.__editMenu.add_command(label="Cut", accelerator="Ctrl+X", command=self.__cut)
        self.__editMenu.add_command(label="Copy", accelerator="Ctrl+C", command=self.__copy)
        self.__editMenu.add_command(label="Paste", accelerator="Ctrl+V", command=self.__paste)
        self.__editMenu.add_command(label="Select All", accelerator="Ctrl+A", command=self.select_all)

        self.__editMenu.add_separator()
        self.__editMenu.add_command(label="Find", accelerator="Ctrl+F", command=self.find_replace_text)

        self.__editMenu.add_separator()
        self.__editMenu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.__textArea.edit_undo)
        self.__editMenu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.__textArea.edit_redo)

        # To give a feature of View
        self.__menuBar.add_cascade(label="View", menu=self.__zoomMenu)
        self.__zoomMenu.add_command(label="Zoom In", accelerator="Ctrl+Up", command=self.zoom_in)
        self.__zoomMenu.add_command(label="Zoom Out", accelerator="Ctrl+Down", command=self.zoom_out)
        self.__zoomMenu.add_command(label="Restore Zoom", command=self.restore_size)

        self.__zoomMenu.add_separator()
        self.__zoomMenu.add_command(label="Transparent", command=self.transparent)
        self.__zoomMenu.add_command(label="Opaque", command=self.opaque)

        self.__zoomMenu.add_separator()
        self.__zoomMenu.add_command(label="Light mode", command=self.light_mode)
        self.__zoomMenu.add_command(label="Dark mode", command=self.dark_mode)

        # To give a feature of Highlight
        self.__menuBar.add_cascade(label="Highlight", menu=self.__highlight)
        self.__highlight.add_command(label="Highlight", command=self.highlight_text)
        self.__highlight.add_command(label="Remove", command=self.clear_select)
        self.__highlight.add_command(label="Clear All", command=self.clear_highlight)

        # To give a feature of decrypt language
        self.__menuBar.add_cascade(label="Decrypt", menu=self.__decrypt)
        self.__decrypt.add_command(label="To Thai", command=self.decrypt_thai)
        self.__decrypt.add_command(label="To English", command=self.decrypt_eng)

        # To create a feature of description of the notepad
        self.__menuBar.add_cascade(label="Help", menu=self.__helpMenu)
        self.__helpMenu.add_command(label="Contact", command=self.contact)
        self.__helpMenu.add_command(label="Time/Date", command=self.display_time)

        self.__helpMenu.add_separator()
        self.__helpMenu.add_command(label="About", command=self.show_about)

        self.__root.config(menu=self.__menuBar)

        self.__scrollBar.pack(side=RIGHT, fill=Y)
        self.__scrollBar.configure(background="black", troughcolor="gray")

        # Scrollbar will adjust automatically according to the content
        self.__scrollBar.config(command=self.__textArea.yview)
        self.__textArea.config(yscrollcommand=self.__scrollBar.set)

        # Highlight Text Configuration
        self.__textArea.tag_configure("start", foreground="deepskyblue", 
                                      font=f"Consolas {self.__size} underline")

    def show_about(self):
        showinfo("Dark Notepad", "Created by Python Tkinter")

    # Quit without save if text is empty
    def quit_application(self):
        if len(self.__textArea.get("1.0", "end-1c")):
            message = messagebox.askquestion('Notepad', "Do you want to save before exit")
            if message == "yes":
                self.save_file()

        self.__root.destroy()

        try:
            if self.__checkFind == True:
                find_window.destroy()
        except TclError:
            pass

    def open_file(self):
        self.__file = askopenfilename(defaultextension=".txt",
                                      filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.__file == "":
            self.__file = None
        else:
            self.__root.title(os.path.basename(self.__file) + " - Notepad")
            self.__textArea.delete(1.0, END)
            file = open(self.__file, "r", encoding="utf-8")
            self.__textArea.insert(1.0, file.read())
            file.close()

    def clear_file(self, event=None):
        message = messagebox.askquestion('Notepad', "Do you want to create new file")
        if message == "yes":
            self.__root.title("Untitled - Notepad")
            self.__file = None
            self.__textArea.delete(1.0, END)

    def new_file(self):
        contract = {
            "name"  : self.__name,
            "mail"  : self.__mail,
            "phone" : self.__phone,
            "social": self.__social
        }
        Notepad(**contract).run()

    def save_as(self):
        self.__file = asksaveasfile(initialfile='Untitled.txt', defaultextension=".txt",
                                    filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
        if self.__file == "":
            self.__file = None
        else:
            self.__file.write(str(self.__textArea.get(1.0, END)))
            self.__file.close()
            self.__file = None

    def save_file(self, event=None):
        if self.__file is None:
            self.__file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")])
            if self.__file == "":
                self.__file = None
            else:
                file = open(self.__file, "w", encoding="utf-8")
                file.write(self.__textArea.get(1.0, END))
                file.close()
                self.__root.title(os.path.basename(self.__file) + " - Dark Notepad")
        else:
            file = open(self.__file, "w", encoding="utf-8")
            file.write(self.__textArea.get(1.0, END))
            file.close()

    def zoom_in(self, event=None):
        if self.__size + 1 <= 25:
            self.__size += 1
        self.__textArea.configure(font=f"consolas {self.__size}")
        self.__textArea.tag_configure("start", font=f"Consolas {self.__size} underline")

    def zoom_out(self, event=None):
        if self.__size - 1 >= 1:
            self.__size -= 1
        self.__textArea.configure(font=f"consolas {self.__size}")
        self.__textArea.tag_configure("start", font=f"Consolas {self.__size} underline")

    def restore_size(self, event=None):
        self.__size = 12
        self.__textArea.configure(font=f"consolas {self.__size}")
        self.__textArea.tag_configure("start", font=f"Consolas {self.__size} underline")

    def transparent(self):
        self.__root.wm_attributes('-alpha', 0.7)

    def opaque(self):
        self.__root.wm_attributes('-alpha', 1)

    def light_mode(self):
        self.__bgColor = LIGHT
        self.__textArea.configure(bg=self.__bgColor, fg="black", insertbackground="black",
                                  selectbackground="black")
        self.__textArea.tag_configure("start", foreground="black", background=LIME,
                                      font=f"Consolas {self.__size} underline")
        self.__textArea.tag_configure('found', foreground = "white", background = "black")

        try:
            if self.__checkFind == True:
                self.__checkFind = False
                find_window.destroy()
                self.find_replace_text()
        except TclError as error:
            print(error)

    def dark_mode(self):
        self.__bgColor = DARK
        self.__textArea.configure(bg=self.__bgColor, fg="white", insertbackground="orange", 
                                  selectbackground=YELLOW)
        self.__textArea.tag_configure("start", foreground="deepskyblue", background=self.__bgColor,
                                      font=f"Consolas {self.__size} underline")
        self.__textArea.tag_configure('found', foreground = PURPLE, background = self.__bgColor)

        try:
            if self.__checkFind == True:
                self.__checkFind = False
                find_window.destroy()
                self.find_replace_text()
        except TclError as error:
            print(error)

    def contact(self):
        name   = f"Name:         {self.__name}"
        mail   = f"Mail:         {self.__mail}"
        phone  = f"Telephone:    {self.__phone}"
        social = f"Social Media: {self.__social}"

        display = f"{name}\n{mail}\n{social}\n{phone}"
        self.__textArea.insert(END, display)

    def __cut(self):
        self.__textArea.event_generate("<<Cut>>")

    def __copy(self):
        self.__textArea.event_generate("<<Copy>>")

    def __paste(self):
        self.__textArea.event_generate("<<Paste>>")

    def __get_key(self, val):
        for key, value in alphabets.items():
            if val == value:
                return key
        return " "

    # find = self.__textArea.get(SEL_FIRST, SEL_LAST)
    def find_replace_text(self, event=None):
        global find_window
        if self.__checkFind:
            self.__checkFind = False
            find_window.destroy()
            return

        find_window = Toplevel(self.__root)
        self.__checkFind = True
        x = self.__root.winfo_x()
        y = self.__root.winfo_y()
        width = self.__root.winfo_width()

        find_window.geometry("300x100")
        find_window.geometry("+%d+%d" % (x + width - 325, y + 55))
        find_window.title("Find and Replace")
        find_window.resizable(False, False)

        if self.__bgColor == DARK:
            find_window.configure(background=DARK)
    
            Label(find_window, text="Find", fg="white", bg=DARK).grid(row=0, column=0, padx=5)
            find_entry = Entry(find_window, font=8, width=25, textvariable=StringVar(), fg="yellow", bg=DARKER)
            find_entry.configure(insertbackground="orange")
            find_entry.grid(row=0, column=1, columnspan=2, padx=4, pady=4, sticky="ew")

            Label(find_window, text="Replace", fg="white", bg=DARK).grid(row=1, column=0, padx=5)
            replace_entry = Entry(find_window, font=8, width=25, textvariable=StringVar(), fg="yellow", bg=DARKER)
            replace_entry.configure(insertbackground="orange")
            replace_entry.grid(row=1, column=1, columnspan=2, padx=4, pady=4, sticky="ew")

        else:
            find_window.configure(background=LIGHT)

            Label(find_window, text="Find", fg="black", bg=LIGHT).grid(row=0, column=0, padx=5)
            find_entry = Entry(find_window, font=8, width=25, textvariable=StringVar(), fg="black", bg="white")
            find_entry.configure(insertbackground="black")
            find_entry.grid(row=0, column=1, columnspan=2, padx=4, pady=4, sticky="ew")

            Label(find_window, text="Replace", fg="black", bg=LIGHT).grid(row=1, column=0, padx=5)
            replace_entry = Entry(find_window, font=8, width=25, textvariable=StringVar(), fg="black", bg="white")
            replace_entry.configure(insertbackground="black")
            replace_entry.grid(row=1, column=1, columnspan=2, padx=4, pady=4, sticky="ew")

        try:
            select = self.__textArea.selection_get()
            find_entry.insert(0, select)
        except TclError:
            pass

        def find():
            self.__textArea.tag_remove('found', '1.0', END)
            find = find_entry.get()
            
            if find:
                idx = '1.0'
                while True:
                    # searches for desired string from index 1
                    idx = self.__textArea.search(find, idx, nocase = 1, stopindex = END)
                    if not idx: break
                    
                    # last index sum of current index and length of text
                    lastidx = '% s+% dc' % (idx, len(find))
                    
                    # overwrite 'Found' at idx
                    self.__textArea.tag_add('found', idx, lastidx)
                    idx = lastidx
        
                # mark located string as purple
                if self.__bgColor == DARK:
                    self.__textArea.tag_configure('found', foreground = PURPLE, background = self.__bgColor)
                else:
                    self.__textArea.tag_configure('found', foreground = "white", background = "black")
            
            find_entry.focus_set()

        def replace():
            find = find_entry.get()
            new_text = replace_entry.get()

            text = self.__textArea.get(1.0, END)
            text = text.replace(find, new_text)

            self.__textArea.delete(1.0, END)
            self.__textArea.insert(1.0, text[:-1])

            find_entry.focus_set()

        def cancle(event=None):
            self.__checkFind = False
            find_window.destroy()

        found_button = HooverButton(find_window, text="Find", command=find)
        apply_button = HooverButton(find_window, text="Replace", command=replace)
        found_button.grid(row=2, column=1, padx=5, pady=7)
        apply_button.grid(row=2, column=2, padx=5, pady=7)

        if self.__bgColor == LIGHT:
            found_button['bg'] = "black"
            apply_button['bg'] = "black"
            found_button.bind('<Leave>', lambda e: found_button.config(background="black"))
            apply_button.bind('<Leave>', lambda e: apply_button.config(background="black"))

        find_entry.focus_force()
        find_window.attributes('-topmost', 'true')
        find_window.protocol("WM_DELETE_WINDOW", cancle)
        find_window.bind("<Control-f>", cancle)
        find_window.mainloop()

    def highlight_text(self):
        try:
            self.__textArea.tag_add("start", "sel.first", "sel.last")        
        except TclError:
            pass

    def clear_select(self):
        try:
            self.__textArea.tag_remove("start",  "sel.first", "sel.last")
        except TclError:
            pass
  
    def clear_highlight(self):
        self.__textArea.tag_remove("start", "1.0", 'end')

    def select_all(self):
        self.__textArea.tag_add('sel', '1.0', 'end')

    def display_time(self):
        day_string = strftime("%B %d, %Y\n%A, %X %p")
        self.__textArea.insert('end', day_string)

    # method to decrypt mistype language to English
    def decrypt_eng(self):
        new_text = ""
        text = self.__textArea.get(1.0, END)
        self.__textArea.delete(1.0, END)
        for char in text:
            if char in alphabets.values():
                new_text += self.__get_key(char)
            else:
                new_text += char
        self.__textArea.insert(1.0, new_text[:-1])

    # method to decrypt mistype language to Thai
    def decrypt_thai(self):
        new_text = ""
        text = self.__textArea.get(1.0, END)
        self.__textArea.delete(1.0, END)
        for char in text:
            if char in alphabets:
                new_text += alphabets[char]
            else:
                new_text += char
        self.__textArea.insert(1.0, new_text[:-1])

    # method to popup right click menu
    def popup(self, event):
        menu = Menu(self.__root, tearoff=0)

        menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.__cut)
        menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.__copy)
        menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.__paste)
        menu.add_command(label="Select All", accelerator="Ctrl+A", command=self.select_all)

        menu.add_separator()
        menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.__textArea.edit_undo)
        menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.__textArea.edit_redo)
    
        menu.add_separator()
        menu.add_command(label="Highlight", command=self.highlight_text)
        menu.add_command(label="Remove", command=self.clear_select)
        menu.add_command(label="Clear", command=self.clear_highlight)

        menu.add_separator()
        menu.add_command(label="Time/Date", command=self.display_time)
        menu.add_command(label="Contact", command=self.contact)

        if self.__bgColor == DARK:
            menu.configure(bg=self.__bgColor, fg="white")
        else:
            menu.configure(bg=self.__bgColor, fg="black")

        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()

    # Run main application
    def run(self):
        self.__root.mainloop()