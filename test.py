import tkinter as tk
from tkinter import messagebox
import json

# Fungsi untuk memuat data dari file JSON
def load_data_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data["notes"]
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
        return []
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Error decoding JSON.")
        return []

# Fungsi untuk menyimpan data ke file JSON
def save_data_to_json(file_path, notes):
    try:
        with open(file_path, 'w') as file:
            json.dump({"notes": notes}, file, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Error saving to JSON: {e}")

# Fungsi untuk mengisi listbox dengan data
def populate_listbox(listbox, notes):
    listbox.delete(0, tk.END)
    for note in notes:
        listbox.insert(tk.END, note["title"])

# Event handler untuk klik pada item listbox
def on_listbox_select(event):
    try:
        selected_index = listbox.curselection()  # Mendapatkan indeks item yang dipilih
        if selected_index:
            index = selected_index[0]
            selected_note = notes[index]
            entry_title.delete(0, tk.END)  # Hapus teks yang ada di Entry
            entry_title.insert(0, selected_note["title"])  # Masukkan judul yang dipilih ke Entry
            entry_content.delete(1.0, tk.END)  # Hapus teks yang ada di Text
            entry_content.insert(tk.END, selected_note["noteContent"])  # Masukkan konten yang dipilih ke Text
            current_selection.set(index)  # Simpan indeks item yang dipilih
    except IndexError:
        messagebox.showerror("Error", "Selected index is out of range.")

# Fungsi untuk mengganti judul dan konten dari item yang dipilih dan menyimpan perubahan ke JSON
def update_note():
    try:
        index = current_selection.get()
        if index is not None and index < len(notes):
            new_title = entry_title.get()
            new_content = entry_content.get(1.0, tk.END).strip()
            notes[index]["title"] = new_title
            notes[index]["noteContent"] = new_content
            populate_listbox(listbox, notes)
            listbox.select_set(index)
            save_data_to_json(file_path, notes)  # Simpan perubahan ke file JSON
            messagebox.showinfo("Success", "Note updated and saved to JSON successfully.")
        else:
            messagebox.showerror("Error", "No item selected or index out of range.")
    except IndexError:
        messagebox.showerror("Error", "Error updating note, index out of range.")

# Fungsi untuk menghapus item yang dipilih dan menyimpan perubahan ke JSON
def delete_note():
    try:
        index = current_selection.get()
        if index is not None and index < len(notes):
            del notes[index]
            populate_listbox(listbox, notes)
            entry_title.delete(0, tk.END)
            entry_content.delete(1.0, tk.END)
            save_data_to_json(file_path, notes)  # Simpan perubahan ke file JSON
            current_selection.set(None)
            messagebox.showinfo("Success", "Note deleted and changes saved to JSON successfully.")
        else:
            messagebox.showerror("Error", "No item selected or index out of range.")
    except IndexError:
        messagebox.showerror("Error", "Error deleting note, index out of range.")

# Buat instance Tkinter
root = tk.Tk()
root.title("Listbox from JSON")

# Buat listbox
listbox = tk.Listbox(root, width=50, height=15)
listbox.pack(pady=10)

# Muat data dari file JSON
file_path = 'notes.json'
notes = load_data_from_json(file_path)

# Isi listbox dengan data yang dimuat
populate_listbox(listbox, notes)

# Hubungkan event handler ke listbox
listbox.bind('<<ListboxSelect>>', on_listbox_select)

# Buat Entry untuk mengganti judul
entry_title = tk.Entry(root, width=50)
entry_title.pack(pady=10)

# Buat Text untuk mengganti konten catatan
entry_content = tk.Text(root, width=50, height=10)
entry_content.pack(pady=10)

# Buat tombol untuk mengganti judul dan konten
button_update = tk.Button(root, text="Update Note", command=update_note)
button_update.pack(pady=5)

# Buat tombol untuk menghapus item
button_delete = tk.Button(root, text="Delete Note", command=delete_note)
button_delete.pack(pady=5)

# Variable untuk menyimpan indeks item yang dipilih
current_selection = tk.IntVar()
current_selection.set(None)

# Jalankan aplikasi Tkinter
root.mainloop()
