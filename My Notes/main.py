import tkinter as tk
from tkinter import ttk, messagebox
import os, json
from datetime import datetime

class MyNotesApp:
    def __init__(self, root):
        root.title("My Notes")
        root.geometry("1000x600")
        root.config(bg="#FDFDFD")
        os.makedirs("project_folder", exist_ok=True)

        # Toolbar
        toolbar = tk.Frame(root, bg="#FFFFFF", height=40)
        toolbar.pack(fill="x", side="top")
        toolbar_row = tk.Frame(toolbar, bg="#FFFFFF")
        toolbar_row.pack(fill="x", pady=5, padx=10)

        tk.Button(toolbar_row, text="Save", command=self.save_note).pack(side="left", padx=5)

        self.title_var = tk.StringVar()
        self.title_entry = tk.Entry(toolbar_row, textvariable=self.title_var, font=("Helvetica", 12, "bold"))
        self.title_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Theme selection buttons
        theme_button_frame = tk.Frame(toolbar_row, bg="#FFFFFF")
        theme_button_frame.pack(side="left", padx=5)

        themes = [
            {"bg": "#FFFFFF", "fg": "#000000"},
            {"bg": "#1E1E1E", "fg": "#D4D4D4"},
            {"bg": "#FFFAF0", "fg": "#5F4B8B"},
            {"bg": "#F0FFFF", "fg": "#008B8B"},
            {"bg": "#FFFACD", "fg": "#8B0000"},
            {"bg": "#E6E6FA", "fg": "#4B0082"}
        ]

        def apply_theme(bg, fg):
            self.text_editor.config(bg=bg, fg=fg)

        for theme in themes:
            btn = tk.Label(theme_button_frame, text=" A ", font=("Helvetica", 10, "bold"),
                           bg=theme["bg"], fg=theme["fg"], width=2, relief="raised", cursor="hand2")
            btn.pack(side="left", padx=2)
            btn.bind("<Button-1>", lambda e, t=theme: apply_theme(t["bg"], t["fg"]))

        # Info bar with Last Modified and Create New
        info_bar = tk.Frame(root, bg="#FDFDFD")
        info_bar.pack(fill="x", padx=10, pady=(0, 5))
        tk.Button(info_bar, text="Create New", font=("Helvetica", 10), relief="flat", borderwidth=0,
                  bg="#FDFDFD", activebackground="#FDFDFD", command=self.create_new_note).pack(side="left")
        self.last_modified_label = tk.Label(info_bar, text="Last Modified: —", font=("Helvetica", 10), bg="#FDFDFD")
        self.last_modified_label.pack(side="left", padx=15)

        # Sidebar for notes list
        list_panel = tk.Frame(root, width=200, bg="#FFFFFF")
        list_panel.pack(side="left", fill="y")
        self.note_listbox = tk.Listbox(list_panel, highlightthickness=0, bd=0)
        self.note_listbox.pack(padx=10, pady=5, fill="both", expand=True)
        self.note_listbox.bind("<<ListboxSelect>>", self.load_note)

        # Text editor panel
        editor_panel = tk.Frame(root, bg="#FDFDFD")
        editor_panel.pack(side="left", fill="both", expand=True)
        self.text_editor = tk.Text(editor_panel, wrap="word", font=("Helvetica", 12),
                                   bg="#FFFFFF", fg="#000000")
        self.text_editor.pack(expand=True, fill="both", padx=10, pady=10)
        self.font_size = tk.IntVar(value=12)

        # Load previously saved notes
        self.load_saved_notes()

        # Bind shortcuts
        root.bind_all("<Control-s>", lambda e: self.save_note())
        root.bind_all("<Control-n>", lambda e: self.create_new_note())
        root.bind_all("<Control-q>", lambda e: root.quit())
        root.bind_all("<Control-b>", lambda e: self.insert_bullet())

    def insert_bullet(self):
        self.text_editor.insert(tk.INSERT, "• ")

    def create_new_note(self):
        self.text_editor.delete("1.0", tk.END)
        self.text_editor.config(bg="#FFFFFF", fg="#000000", font=("Helvetica", 12))
        self.font_size.set(12)
        self.title_var.set("")
        self.last_modified_label.config(text="Last Modified: —")
        self.title_entry.focus_set()

    def save_note(self):
        content = self.text_editor.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Empty Note", "Write something before saving.")
            return

        title = self.title_var.get().strip() or f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        file_path = os.path.join("project_folder", f"{title}.json")

        last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        weekday = datetime.now().strftime("%A")

        note_data = {
            "title": title,
            "content": content,
            "bg_color": self.text_editor["bg"],
            "font_color": self.text_editor["fg"],
            "font_size": self.font_size.get(),
            "last_modified": last_modified
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(note_data, f, indent=2)

        self.last_modified_label.config(text=f"Last Modified: {last_modified} ({weekday})")
        self.load_saved_notes()

    def load_saved_notes(self):
        self.note_listbox.delete(0, tk.END)
        notes = []
        for file in os.listdir("project_folder"):
            if file.endswith(".json"):
                path = os.path.join("project_folder", file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        notes.append((data["title"], data.get("last_modified", "")))
                except:
                    continue
        notes.sort(key=lambda x: x[1], reverse=True)
        for title, _ in notes:
            self.note_listbox.insert(tk.END, title)

    def load_note(self, event):
        try:
            selected_title = self.note_listbox.get(self.note_listbox.curselection())
            file_path = os.path.join("project_folder", f"{selected_title}.json")
            with open(file_path, "r", encoding="utf-8") as f:
                note_data = json.load(f)

            self.title_var.set(note_data.get("title", selected_title))
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert("1.0", note_data["content"])
            self.text_editor.config(
                bg=note_data.get("bg_color", "#FFFFFF"),
                fg=note_data.get("font_color", "#000000"),
                font=("Helvetica", note_data.get("font_size", 12))
            )
            self.font_size.set(note_data.get("font_size", 12))

            modified_text = f"{note_data['last_modified']} ({datetime.strptime(note_data['last_modified'], '%Y-%m-%d %H:%M:%S').strftime('%A')})"
            self.last_modified_label.config(text=f"Last Modified: {modified_text}")
        except Exception as e:
            print("Error loading note:", e)

# Launch the app
root = tk.Tk()
app = MyNotesApp(root)
try:
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='icon.png'))
except:
    pass
root.mainloop()

