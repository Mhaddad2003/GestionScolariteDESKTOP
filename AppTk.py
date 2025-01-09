import tkinter as tk
from tkinter.font import Font
from tkinter import ttk
from PIL import Image, ImageTk

class ScolariteApp:
    def center_window(self, window, width, height):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def on_hover(self, event):
        event.widget.configure(bg="#16a085")

    def on_leave(self, event):
        event.widget.configure(bg="#1abc9c")

    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Scolarité")
        self.root.geometry("1100x500")
        self.center_window(self.root, 1100, 500)
        self.root.configure(bg="#2c3e50")
        self.root.iconbitmap("images/appIcone.ico")

        self.pages = {}

        self.create_main_page()
        self.create_secondary_pages()

        self.show_page("main")

    def create_main_page(self):
        """Crée la page principale."""
        page = tk.Frame(self.root, bg="#2c3e50")
        self.pages["main"] = page

        title_font = Font(family="Arial Black", size=20, weight="bold")
        button_font = Font(family="Arial", size=14, weight="bold")

        title_label = tk.Label(
            page,
            text="Gestion de Scolarité",
            font=title_font,
            bg="#2c3e50",
            fg="white"
        )
        title_label.place(relx=0.5, y=60, anchor="center")

        main_frame = tk.Frame(page, bg="#2c3e50")
        main_frame.pack(expand=True)

        image_path = "images/image.png"
        img = Image.open(image_path)
        img_resized = img.resize((750, 242))
        self.photo = ImageTk.PhotoImage(img_resized)
        image_label = tk.Label(main_frame, image=self.photo, bg="#2c3e50")
        image_label.grid(row=0, column=0, rowspan=4, padx=10, pady=12, sticky="n")

        button_frame = tk.Frame(main_frame, bg="#2c3e50")
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        buttons = [
            ("Gérer Étudiants", "form_etudiant"),
            ("Gérer Enseignants", "form_enseignant"),
            ("Gérer Modules", "form_module"),
            ("Gérer Inscriptions", "form_inscription")
        ]

        for i, (text, page_name) in enumerate(buttons):
            button = tk.Button(
                button_frame,
                text=text,
                font=button_font,
                bg="#1abc9c",
                fg="white",
                activebackground="#16a085",
                activeforeground="white",
                bd=0,
                padx=20,
                pady=10,
                command=lambda p=page_name: self.show_page(p),
                cursor="hand2"  # Curseur de clic (main)
            )
            button.bind("<Enter>", self.on_hover)
            button.bind("<Leave>", self.on_leave)
            button.grid(row=i, column=0, pady=5, sticky="ew")

        button_frame.grid_columnconfigure(0, weight=1)

        self.add_footer(page)  # Ajout du footer

    def add_footer(self, page):
        """Ajoute le footer à la page."""
        footer = tk.Label(
            page,
            text="© 2025 Scolarité App. Tous droits réservés.",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="white"
        )
        footer.pack(side=tk.BOTTOM, pady=10)

    def create_form_page(self, page_name, title, fields, table_columns):
        """Crée une page contenant un formulaire et un tableau."""
        page = tk.Frame(self.root, bg="#2c3e50")
        self.pages[page_name] = page

        title_font = Font(family="Arial Black", size=20, weight="bold")
        label_font = Font(family="Arial", size=12, weight="bold")
        entry_font = Font(family="Arial", size=12)

        title_label = tk.Label(
            page,
            text=title,
            font=title_font,
            bg="#2c3e50",
            fg="white"
        )
        title_label.place(relx=0.5, y=60, anchor="center")

        form_frame = tk.Frame(page, bg="#2c3e50")
        form_frame.place(relx=0.3, rely=0.5, anchor="center")

        self.form_entries = {}  

        for i, (field_name, field_type, *extra) in enumerate(fields):
            label = tk.Label(
                form_frame,
                text=field_name,
                font=label_font,
                bg="#2c3e50",
                fg="white"
            )
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            if field_type == "entry":
                entry = tk.Entry(form_frame, font=entry_font)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
                self.form_entries[field_name] = entry 

        form_frame.grid_columnconfigure(1, weight=1)

        table_frame = tk.Frame(page, bg="#2c3e50")
        table_frame.place(relx=0.71, rely=0.5, anchor="center")

        self.table = ttk.Treeview(table_frame, columns=table_columns, show="headings")
        for col in table_columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100)

        self.table.grid(row=0, column=0, padx=10, pady=10)

        scrollbar = tk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky='ns', padx=5, pady=10)

        button_frame = tk.Frame(page, bg="#2c3e50")
        button_frame.place(relx=0.5, rely=0.85, anchor="center")

        def on_hover_x_button(event):
            event.widget.configure(bg="#0c0c0c")

        def on_leave_x_button(event):
            event.widget.configure(bg="Black")

        def on_hover_delete_button(event):
            event.widget.configure(bg="#e74c3c")  

        def on_leave_delete_button(event):
            event.widget.configure(bg="#c0392b")  

        def clear_inputs():
           for entry in self.form_entries.values():
            if isinstance(entry, tk.Entry): 
                entry.delete(0, "end")  

        buttons = [
            ("Vider", clear_inputs), 
            ("Ajouter", lambda: self.add_to_table(table_columns)),
            ("Modifier", lambda: self.modify_table(table_columns)),
            ("Supprimer", lambda: self.delete_from_table())
        ]

        for i, (text, command) in enumerate(buttons):
            button = tk.Button(
                button_frame,
                text=text,
                font=("Arial", 12, "bold"),
                bg="Black" if text != "Supprimer" else "#c0392b",  
                fg="white",
                activebackground="#0c0c0c" if text != "Supprimer" else "#e74c3c",
                activeforeground="white",
                bd=0,
                padx=20,
                pady=10,
                command=command,
                cursor="hand2"  
            )
            if text == "Supprimer":
                button.bind("<Enter>", on_hover_delete_button)
                button.bind("<Leave>", on_leave_delete_button)
            else:
                button.bind("<Enter>", on_hover_x_button)
                button.bind("<Leave>", on_leave_x_button)
            button.grid(row=0, column=i, padx=5, pady=10, sticky="ew")

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)

        back_button = tk.Button(
            page,
            text="Retour",
            font=("Arial", 12, "bold"),
            bg="#1abc9c",
            fg="white",
            activebackground="#16a085",
            activeforeground="white",
            bd=0,
            padx=20,
            pady=10,
            command=lambda: self.show_page("main"),
            cursor="hand2"  
        )
        back_button.place(relx=0.9, y=60, anchor="center")
        back_button.bind("<Enter>", self.on_hover)
        back_button.bind("<Leave>", self.on_leave)

        page.pack_propagate(False)
        page.pack(fill="both", expand=True)

        self.add_footer(page)  

    def add_to_table(self, table_columns):
        data = []
        for col in table_columns:
            data.append(self.form_entries[col].get())
        self.table.insert("", "end", values=data)
        for col in table_columns:
            self.form_entries[col].delete(0, "end")

    def modify_table(self, table_columns):
        pass  

    def delete_from_table(self):
        selected_item = self.table.selection()
        if selected_item:
            self.table.delete(selected_item)

    def create_secondary_pages(self):

        self.create_form_page("form_etudiant", "Espace des Étudiants", [
            ("Appoge", "entry"),
            ("Nom", "entry"),
            ("Prenom", "entry"),
            ("CIN", "entry"),
            ("Date Naissance", "entry")
        ], ["Appoge", "Nom", "Prenom", "CIN", "Date Naissance"])

        self.create_form_page("form_module", "Espace des Modules", [
            ("Id", "entry"),
            ("Matière", "entry"),
            ("Semestre", "entry")
        ], ["Id", "Matière", "Semestre"])
      
        self.create_form_page("form_enseignant", "Espace des Enseignants", [
            ("Id", "entry"),
            ("Nom", "entry"),
            ("Prenom", "entry"),
            ("CIN", "entry"),
            ("Département", "entry")
        ], ["Id", "Nom", "Prenom", "CIN", "Département"])

        self.create_form_page("form_inscription", "Espace des Inscriptions", [
            ("Id-Etudiant", "entry"),
            ("Id-Module", "entry"),
            ("Note", "entry"),
            ("Valide", "entry")
        ], ["Id-Etudiant", "Id-Module", "Note", "Valide"])

    def show_page(self, page_name):
        """Affiche la page spécifiée."""
        for page in self.pages.values():
            page.pack_forget()
        self.pages[page_name].pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScolariteApp(root)
    root.mainloop()
