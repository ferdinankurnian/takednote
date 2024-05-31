# import tkinter modules
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import json
import random
import ast

# buat jendela utama
root = tk.Tk()
root.title("TakedNote")
root.geometry("1000x600")
root.config(bg='#2F2F2F')
root.iconbitmap("TakedNote.ico")

# Variabel
current_id = 0
current_index_listbox = 0
file_saved = False


# -- semua fungsi --

# buat fungsi cek isi
def check_text_content():
    content = text_widget.get("1.0", "end-1c")  # Get the text content
    if content:
        return True
    else:
        return False

def load_json():
    with open('notes.json', 'r') as file:
        data = json.load(file)
        return data['notes']

def loadTheList(notes):
    listbox.delete(0, tk.END)
    for note in notes:
        listbox.insert(tk.END, note["title"])

def load_note(titlenote, contentnote):
    title_widget.delete("1.0", tk.END)
    text_widget.delete("1.0", tk.END)
    title_widget.insert("1.0", titlenote)
    text_widget.insert("1.0", contentnote)

# Event handler untuk klik pada item listbox
def on_listbox_select(event):
    global current_id, current_index_listbox
    selected_index = listbox.curselection()  # Mendapatkan indeks item yang dipilih
    if selected_index:
        index = selected_index[0]
        selected_note = datanotes[index]
        note_id = selected_note["id"]
        note_title = selected_note["title"]
        note_content = selected_note["noteContent"]
        load_note(note_title, note_content)
        current_id = note_id
        current_index_listbox = index
    
def new_note():
    global current_id, current_index_listbox, datanotes
    randomID = random.randint(1, 10000)
    
    # Insert new item into the listbox
    listbox.select_clear(0, tk.END)
    listbox.insert(tk.END, "Add Title..")
    
    # Get the last index and select it
    last_index = listbox.size() - 1
    listbox.select_set(last_index)
    selected_index = listbox.curselection()
    
    if selected_index:
        index = selected_index[0]
        
        # Check if index is valid in datanotes
        if index >= len(datanotes):
            # Add a new note to datanotes if it does not exist
            datanotes.append({"id": randomID, "title": "Add Title..", "noteContent": ""})
        else:
            # Update the existing note in datanotes
            selected_note = datanotes[index]
            selected_note["id"] = randomID
            selected_note["title"] = "Add Title.."
            selected_note["noteContent"] = ""
        
        # Save notes to file
        with open('notes.json', 'w') as file:
            json.dump({"notes": datanotes}, file, indent=4)
        
        # Update globals
        current_id = randomID
        current_index_listbox = index
        load_note("Add Title..", "")


def delete_note():
    global current_index_listbox, current_id, datanotes
    
    current_selection = listbox.curselection()
    
    if current_selection:
        current_index = current_selection[0]
        
        if current_index < len(datanotes):
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?")
            if confirm:
                del datanotes[current_index]

                with open('notes.json', 'w') as file:
                    json.dump({"notes": datanotes}, file, indent=4)

                listbox.delete(current_index)
                
                # Select the previous item if possible, otherwise select the next one
                if listbox.size() > 0:
                    if current_index > 0:
                        new_index = current_index - 1
                    else:
                        new_index = 0
                    listbox.select_set(new_index)
                    listbox.see(new_index)
                    
                    selected_note = datanotes[new_index]
                    note_id = selected_note["id"]
                    note_title = selected_note["title"]
                    note_content = selected_note["noteContent"]
                    load_note(note_title, note_content)
                    
                    current_id = note_id
                    current_index_listbox = new_index
                else:
                    # Handle case when listbox is empty
                    current_id = None
                    current_index_listbox = None
                    load_note("Welcome to TakedNote", "Select Note from Sidebar or Create New one!")

def save_note():
    global current_index_listbox

    if current_index_listbox is not None and current_index_listbox < len(datanotes):
        new_title = title_widget.get(1.0, tk.END).strip()
        new_content = text_widget.get(1.0, tk.END).strip()
        datanotes[current_index_listbox]["title"] = new_title
        datanotes[current_index_listbox]["noteContent"] = new_content
        loadTheList(datanotes)
        listbox.select_set(current_index_listbox)
        with open('notes.json', 'w') as file:
            json.dump({"notes": datanotes}, file, indent=4)


# fungsi untuk autosave
def autoload():
    global current_id, current_index_listbox

    if current_id != 0:
        save_note()

    root.after(1000, autoload)

autoload()

# fungsi untuk shortcut keyboard

def cut():
    text_widget.event_generate("<<Cut>>")

def copy():
    text_widget.event_generate("<<Copy>>")

def paste():
    text_widget.event_generate("<<Paste>>")

def select_all():
    text_widget.tag_add("sel", "1.0", "end")

# fungsi untuk munculkan dialog keluar
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()

def nextToNoteContent(event):
    text_widget.focus_set()
    return "break"  # Prevent the default behavior

def about_dialog():
    messagebox.showinfo("About", "TakedNote is an simple note-taking app")


# GUI

# buat menu bar
menu_bar = tk.Menu(root, font=("Ubuntu", 11), bg="#C5C5C5")
menu_bar.config(borderwidth=0)

# buat menu file
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.config(borderwidth=0)

file_menu.add_command(label="New Note..", command=new_note, accelerator="Ctrl+N")
file_menu.add_separator()
file_menu.add_command(label="Save", command=save_note, accelerator="Ctrl+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=on_closing, accelerator="Ctrl+Q")

menu_bar.add_cascade(label="File", menu=file_menu)

# buat menu edit
edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.config(borderwidth=0)

edit_menu.add_command(label="Cut", command=cut, accelerator="Ctrl+X")
edit_menu.add_command(label="Copy", command=copy, accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command=paste, accelerator="Ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")

menu_bar.add_cascade(label="Edit", menu=edit_menu)

# buat menu help
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.config(borderwidth=0)

help_menu.add_command(label="About", command=about_dialog, accelerator="Ctrl+L")

menu_bar.add_cascade(label="Help", menu=help_menu)

# tambahkan menu bar ke jendela utama
root.config(menu=menu_bar)

ribbonmenu = tk.Frame(root, padx=5, pady=5, bg='#606060')
ribbonmenu.pack(fill='x', side='top')

newnotebtn = tk.Button(ribbonmenu, text="New Note", command=new_note)
newnotebtn.pack(side='left', ipadx=10, ipady=5)
newnotebtn.config(highlightthickness=0, borderwidth=0)

delnotebtn = tk.Button(ribbonmenu, text="Delete Note", bg='#810604', foreground='#fff', command=delete_note)

datanotes = load_json()

listbox = tk.Listbox(root, bg='#2F2F2F', foreground='#fff', font=("Ubuntu", 13), width=25)
listbox.pack(fill='both', side='left', padx=10, pady=10)
listbox.config(highlightthickness=0, borderwidth=0)


def loadDeleteBtn():
    global current_index_listbox, datanotes, delnotebtn, listbox
    current_selection = listbox.curselection()
    
    if current_selection:
        if current_index_listbox is not None and current_index_listbox < len(datanotes):
            delnotebtn.pack(side='right', ipadx=10, ipady=5)
            delnotebtn.config(highlightthickness=0, borderwidth=0)
        else:
            delnotebtn.pack_forget()

    root.after(1000, loadDeleteBtn)

loadDeleteBtn()

loadTheList(datanotes)

# Bind the event to the listbox
listbox.bind("<<ListboxSelect>>", on_listbox_select)

es = tk.Entry(root, bg="#3E3E3E")

title_widget = tk.Text(root, bg='#3E3E3E', height=1, foreground='#fff', padx=20, pady=15, font=("Ubuntu", 15)) 
title_widget.pack(fill='x', side='top')
title_widget.config(highlightthickness=0, borderwidth=0)

title_template = """Welcome to TakedNote"""
title_widget.insert(tk.END, title_template)

text_widget = tk.Text(root, bg='#3E3E3E', foreground='#fff', padx=20, pady=5, font=("Ubuntu", 12))
text_widget.pack(fill='both', side='right', expand=True)
text_widget.config(highlightthickness=0, borderwidth=0)

text_template = """Select Note from Sidebar or Create New one!"""
text_widget.insert(tk.END, text_template)

title_widget.bind('<Return>', nextToNoteContent)

root.bind('<Control-a>', lambda e: select_all())
root.bind('<Control-x>', lambda e: cut())
root.bind('<Control-c>', lambda e: copy())
root.bind('<Control-v>', lambda e: paste())
root.bind('<Control-s>', lambda e: save_note())
root.bind('<Control-d>', lambda e: delete_note())
root.bind('<Control-l>', lambda e: about_dialog())
root.bind('<Control-n>', lambda e: new_note())

root.protocol("WM_DELETE_WINDOW", on_closing)

# Looping forever until the user exits
root.mainloop()
