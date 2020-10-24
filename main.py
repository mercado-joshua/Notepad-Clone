#===========================
# Imports
#===========================

import tkinter as tk
from tkinter import ttk, colorchooser as cc, Menu, Spinbox as sb, scrolledtext as st, messagebox as mb, filedialog as fd

import os


#===========================
# Main App
#===========================

class App(tk.Tk):
    """Main Application."""

    # ==========================================
    def __init__(self):
        super().__init__()
        self.init_config()
        self.init_UI()
        self.init_events()

    def init_config(self):
        self.geometry('850x550+0+0')
        self.iconbitmap('notepad.ico')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.filename = None
        self.set_title(self.filename)

    def init_UI(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # ------------------------------------------
        menubar = tk.Menu(self.frame)
        self.config(menu=menubar)

        file = tk.Menu(menubar, tearoff=0)
        file.add_command(label='New', accelerator='Ctrl+N', command=self.new)
        file.add_command(label='Open...', accelerator='Ctrl+O', command=self.open)
        file.add_command(label='Save', accelerator='Ctrl+S', command=self.save)
        file.add_command(label='Save As', command=self.saveas)
        file.add_separator()
        file.add_command(label='Page Setup...', accelerator='Ctrl+S', command=None, state=tk.DISABLED)
        file.add_command(label='Print...', accelerator='Ctrl+P', command=None, state=tk.DISABLED)
        file.add_separator()
        file.add_command(label='Exit', command=self.exit_)
        menubar.add_cascade(label='File', menu=file)

        self.edit = tk.Menu(menubar, tearoff=0, postcommand=self.enable)
        self.edit.add_command(label='Undo', accelerator='Ctrl+Z', command=self.undo)
        self.edit.add_separator()
        self.edit.add_command(label='Cut', accelerator='Ctrl+X', command=self.cut)
        self.edit.add_command(label='Copy', accelerator='Ctrl+C', command=self.copy)
        self.edit.add_command(label='Paste', accelerator='Ctrl+V', command=self.paste)
        self.edit.add_command(label='Delete', accelerator='Del', command=self.delete)
        self.edit.add_separator()
        self.edit.add_command(label='Find...', accelerator='Ctrl+F', command=None, state=tk.DISABLED)
        self.edit.add_command(label='Find Next', accelerator='F3', command=None, state=tk.DISABLED)
        self.edit.add_command(label='Replace...', accelerator='Ctrl+H', command=None, state=tk.DISABLED)
        self.edit.add_command(label='Go To...', accelerator='Ctrl+G', command=None, state=tk.DISABLED)
        self.edit.add_separator()
        self.edit.add_command(label='Select All', accelerator='Ctrl+A', command=self.select_all)
        self.edit.add_command(label='Time/Date', accelerator='F5', command=None, state=tk.DISABLED)
        menubar.add_cascade(label='Edit', menu=self.edit)

        format_ = tk.Menu(menubar, tearoff=0)
        self.toggle = tk.BooleanVar()
        format_.add_checkbutton(label='Word Wrap', onvalue=True, offvalue=False, variable=self.toggle, command=self.wrap)
        format_.add_command(label='Font...', command=None, state=tk.DISABLED)
        menubar.add_cascade(label='Format', menu=format_)

        view = tk.Menu(menubar, tearoff=0)
        view.add_command(label='Status Bar', command=None, state=tk.DISABLED)
        menubar.add_cascade(label='View', menu=view)

        help_ = tk.Menu(menubar, tearoff=0)
        help_.add_command(label='View Help', command=None, state=tk.DISABLED)
        help_.add_separator()
        help_.add_command(label='About Notepad', command=None, state=tk.DISABLED)
        menubar.add_cascade(label='Help', menu=help_)

        # ------------------------------------------
        self.textarea = st.ScrolledText(self.frame, undo=True)
        self.textarea.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # ------------------------------------------
        self.popupmenu = Menu(self.frame, tearoff=0, postcommand=self.enable)
        self.popupmenu.add_command(label='Undo', command=self.undo)
        self.popupmenu.add_separator()
        self.popupmenu.add_command(label='Cut', command=self.cut)
        self.popupmenu.add_command(label='Copy', command=self.copy)
        self.popupmenu.add_command(label='Paste', command=self.paste)
        self.popupmenu.add_command(label='Delete', command=self.delete)
        self.popupmenu.add_separator()
        self.popupmenu.add_command(label='Select All', command=self.select_all)
        self.popupmenu.add_separator()
        self.popupmenu.add_command(label='Right to left Reading order', command=None, state=tk.DISABLED)
        self.popupmenu.add_command(label='Show Unicode control characters', command=None, state=tk.DISABLED)

        popupsubmenu = Menu(self.popupmenu, tearoff=0)
        popupsubmenu.add_command(label='LRM', accelerator='Left-to-right mark', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='RLM', accelerator='Right-to-left mark', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='ZWJ', accelerator='Zero width joiner', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='ZWNJ', accelerator='Zero width non-joiner', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='LRE', accelerator='Start of left-to-right embedding', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='RLE', accelerator='Start of right-to-left embedding', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='LRO', accelerator='Start of left-to-right override', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='RLO', accelerator='Start of right-to-left override', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='PDF', accelerator='Pop directional formatting', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='NADS', accelerator='National digits shapes substitution', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='NODS', accelerator='Nominal (European) digit shapes', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='ASS', accelerator='Activate symmetric swapping', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='ISS', accelerator='Inhibit symmetric swapping', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='AAFS', accelerator='Activate Arabic form shaping', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='IAFS', accelerator='Inhibit Arabic form shaping', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='RS', accelerator='Record Separator (Block separator)', command=None, state=tk.DISABLED)
        popupsubmenu.add_command(label='US', accelerator='Unit Separator (Segment separator)', command=None, state=tk.DISABLED)

        self.popupmenu.add_cascade(label='Insert Unicode control character', menu=popupsubmenu)
        self.popupmenu.add_separator()
        self.popupmenu.add_command(label='Open IME', command=None, state=tk.DISABLED)
        self.popupmenu.add_command(label='Reconversion', command=None, state=tk.DISABLED)

    def init_events(self):
        self.bind('<Button-3>', self.show_popupmenu)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-c>', self.copy)
        self.bind('<Delete>', self.delete)
        self.bind('<Control-v>', self.paste)
        self.bind('<Control-a>', self.select_all)
        self.bind('<Control-z>', self.undo)

        self.bind('<Control-n>', self.new)
        self.bind('<Control-o>', self.open)
        self.bind('<Control-s>', self.save)

    # INSTANCE METHODS -------------------------
    def exit_(self, *args):
        options = mb.askyesno('Warning', 'Your Unsaved Data May be Lost!')
        if options > 0:
            self.destroy()

    def set_title(self, filename):
        if self.filename:
            self.title(f'{filename} - Notepad')
        else:
            self.title('Untitled - Notepad')

    def __read(self, filename):
        with open(filename, 'r') as file:
            text = file.read()

        return text

    def wrap(self):
        if self.toggle.get() == True:
            self.textarea.config(wrap=tk.WORD)
        else:
            self.textarea.config(wrap=tk.CHAR)

    def enable(self):
        selection = tk.ACTIVE if self.textarea.tag_ranges(tk.SEL) else tk.DISABLED
        clipboard = tk.ACTIVE
        contents = tk.ACTIVE if not self.textarea.compare('end-1c', '==', '1.0') else tk.DISABLED

        try:
            self.clipboard_get()
        except tk.TclError:
            clipboard = tk.DISABLED

        self.edit.entryconfig(0, state=contents)
        self.edit.entryconfig(2, state=selection)
        self.edit.entryconfig(3, state=selection)
        self.edit.entryconfig(4, state=clipboard)
        self.edit.entryconfig(5, state=selection)
        self.edit.entryconfig(12, state=contents)

        self.popupmenu.entryconfig(0, state=contents)
        self.popupmenu.entryconfig(2, state=selection)
        self.popupmenu.entryconfig(3, state=selection)
        self.popupmenu.entryconfig(4, state=clipboard)
        self.popupmenu.entryconfig(5, state=selection)
        self.popupmenu.entryconfig(7, state=contents)

    # EVENTS METHODS ---------------------------
    def show_popupmenu(self, event):
        self.popupmenu.post(event.x_root, event.y_root)

    def cut(self, event=None):
        self.copy()
        self.delete()

    def copy(self, event=None):
        selection = self.textarea.tag_ranges(tk.SEL)
        if selection:
            self.clipboard_clear()
            self.clipboard_append(self.textarea.get(*selection))

    def delete(self, event=None):
        selection = self.textarea.tag_ranges(tk.SEL)
        if selection:
            self.textarea.delete(*selection)

    def paste(self, event=None):
        self.textarea.insert(tk.INSERT, self.clipboard_get())

    def select_all(self, event=None):
        self.textarea.tag_add(tk.SEL, '1.0', tk.END)
        self.textarea.mark_set(tk.INSERT, '1.0')
        self.textarea.see(tk.INSERT)

    def undo(self, event=None):
        self.textarea.edit_undo()

    def new(self, event=None):
        self.textarea.delete('1.0', tk.END)
        self.filename = None
        self.set_title(self.filename)

    def open(self, event=None):
        self.textarea.delete('1.0', tk.END)

        filetypes = (('Text Documents', '*.txt'), ('All Files', '*'))
        self.filename = fd.askopenfilename(title='Open', initialdir='/', filetypes=filetypes)

        if self.filename != '':
            text = self.__read(self.filename)
            self.textarea.insert(tk.END, text)

            name = os.path.basename(self.filename)
            self.set_title(name)

    def save(self, event=None):
        if self.filename:
            contents = self.textarea.get('1.0', tk.END)

            with open(self.filename, 'w') as file:
                save = file.write(contents)

            name = os.path.basename(self.filename)
            self.set_title(name)

        else:
            self.saveas()

    def saveas(self, event=None):
        contents = self.textarea.get(1.0, tk.END)
        file = fd.asksaveasfile(mode='a', title='Save As', initialfile='Untitled.txt', defaultextension='.txt', filetypes=(('Text Documents', '*.txt'),))

        if file:
            file.write(contents)
            file.close()

        self.filename = file.name
        name = os.path.basename(self.filename)
        self.set_title(name)


#===========================
# Start GUI
#===========================

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()