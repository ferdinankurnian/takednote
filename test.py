import json
import tkinter as tk
from tkinter import messagebox

# Asumsi variabel global
current_id = None
current_index_listbox = None
datanotes = []

# Inisialisasi tkinter
root = tk.Tk()
root.geometry("400x300")

# Inisialisasi Listbox
listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH, expand=True)

# Buat Menu Bar
menubar = tk.Menu(root)
root.config(menu=menubar)

# Buat Menu "File"
file_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file_menu)

# Tambah item menu "Delete Note"
file_menu.add_command(label="Delete Note", command=lambda: delete_note(), state=tk.DISABLED)

def update_menu_state():
    # Perbarui state item menu berdasarkan current_id
    if current_id is not None:
        file_menu.entryconfig("Delete Note", state=tk.NORMAL)
    else:
        file_menu.entryconfig("Delete Note", state=tk.DISABLED)

def load_note(title, content):
    # Fungsi ini harus diimplementasikan
    pass

def new_note():
    global current_id, current_index_listbox, datanotes
    randomID = random.randint(1, 10000)
    
    # Insert new item into the listbox
    listbox.select_clear(0, tk.END)
    listbox.insert(tk.END, "Add Title..")
    
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
        update_menu_state()

def delete_note():
    global current_index_listbox, current_id, datanotes
    
    current_selection = listbox.curselection()
    
    if current_selection:
        current_index = current_selection[0]
        
        if current_index < len(datanotes):
            # Menampilkan kotak pesan konfirmasi
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this note?")
            if confirm:
                del datanotes[current_index]

                with open('notes.json', 'w') as file:
                    json.dump({"notes": datanotes}, file, indent=4)

                listbox.delete(current_index)
                
                # Pilih item sebelumnya jika memungkinkan, atau item berikutnya jika item pertama dihapus
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
                    # Penanganan kasus saat listbox kosong
                    current_id = None
                    current_index_listbox = None
                    load_note("", "")
                update_menu_state()

# Contoh penggunaan
# Bind new_note ke tombol
root.bind('<Control-n>', lambda event: new_note())

# Start main loop
root.mainloop()
