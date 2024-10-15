import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

# Create database connection
conn = sqlite3.connect('daily_notebook.db')
c = conn.cursor()

# Create notes table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS notes 
             (id INTEGER PRIMARY KEY, date TEXT, content TEXT)''')
conn.commit()

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

# GUI setup
root = tk.Tk()
root.title("Daily Notebook")

# Entry area for adding new notes
text_entry = tk.Text(root, height=5, width=50)
text_entry.pack(pady=10)

# Button to add a new note
add_button = tk.Button(root, text="Add Note", command=add_note)
add_button.pack(pady=5)

# Listbox to display notes
notes_list = tk.Listbox(root, height=10, width=
