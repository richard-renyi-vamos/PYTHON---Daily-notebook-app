import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
from datetime import datetime

# Default database path
db_path = 'daily_notebook.db'

# Create database connection
def connect_db(path):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes 
                 (id INTEGER PRIMARY KEY, date TEXT, content TEXT)''')
    conn.commit()
    return conn, c

conn, c = connect_db(db_path)

# Function to add a new note
def add_note():
    note = text_entry.get("1.0", tk.END).strip()
    if not note:
        messagebox.showwarning("Input error", "Note cannot be empty!")
        return

    today_date = datetime.now().strftime("%Y-%m-%d")
    c.execute("INSERT INTO notes (date, content) VALUES (?, ?)", (today_date, note))
    conn.commit()
    display_notes()  # Refresh the list of notes
    text_entry.delete("1.0", tk.END)  # Clear the text box

# Function to display today's notes
def display_notes():
    today_date = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT * FROM notes WHERE date=?", (today_date,))
    rows = c.fetchall()
    
    notes_list.delete(0, tk.END)  # Clear the listbox
    for row in rows:
        notes_list.insert(tk.END, row[2])  # Display only the content

# Function to delete a selected note
def delete_note():
    selected_note = notes_list.curselection()
    if not selected_note:
        messagebox.showwarning("Selection error", "Please select a note to delete!")
        return

    note_content = notes_list.get(selected_note)
    today_date = datetime.now().strftime("%Y-%m-%d")
    c.execute("DELETE FROM notes WHERE date=? AND content=?", (today_date, note_content))
    conn.commit()
    display_notes()  # Refresh the list

# Function to open settings window
def open_settings():
    def save_settings():
        global db_path, conn, c
        new_path = db_path_entry.get().strip()
        if not new_path:
            messagebox.showwarning("Input error", "Database path cannot be empty!")
            return

        try:
            conn.close()  # Close current connection
            conn, c = connect_db(new_path)  # Reconnect with new path
            db_path = new_path
            messagebox.showinfo("Success", "Settings saved successfully!")
            settings_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to the database: {e}")

    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")

    tk.Label(settings_window, text="Database Path:").pack(pady=5)
    db_path_entry = tk.Entry(settings_window, width=50)
    db_path_entry.insert(0, db_path)
    db_path_entry.pack(pady=5)

    browse_button = tk.Button(settings_window, text="Browse", command=lambda: db_path_entry.insert(0, filedialog.askopenfilename()))
    browse_button.pack(pady=5)

    save_button = tk.Button(settings_window, text="Save", command=save_settings)
    save_button.pack(pady=10)

# GUI setup
root = tk.Tk()
root.title("Daily Notebook")

# Menu bar
menu_bar = tk.Menu(root)
settings_menu = tk.Menu(menu_bar, tearoff=0)
settings_menu.add_command(label="Settings", command=open_settings)
menu_bar.add_cascade(label="Options", menu=settings_menu)
root.config(menu=menu_bar)

# Entry area for adding new notes
text_entry = tk.Text(root, height=5, width=50)
text_entry.pack(pady=10)

# Button to add a new note
add_button = tk.Button(root, text="Add Note", command=add_note)
add_button.pack(pady=5)

# Listbox to display notes
notes_list = tk.Listbox(root, height=10, width=50)
notes_list.pack(pady=10)

# Button to delete a selected note
delete_button = tk.Button(root, text="Delete Note", command=delete_note)
delete_button.pack(pady=5)

# Display notes on startup
display_notes()

root.mainloop()
