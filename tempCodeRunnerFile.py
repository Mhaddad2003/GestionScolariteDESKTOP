import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import Font

# Main Application Class
class ScolariteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Scolarité")
        self.root.geometry("1200x800")
        self.root.configure(bg="#2c3e50")  # Dark background

        # Custom Fonts
        self.title_font = Font(family="Helvetica", size=28, weight="bold")
        self.button_font = Font(family="Arial", size=14, weight="bold")
        self.label_font = Font(family="Arial", size=12)

        # Data Storage (Simulated)
        self.etudiants = []
        self.enseignants = []
        self.modules = []
        self.inscriptions = []

        # Main Container for Pages
        self.main_frame = tk.Frame(self.root, bg="#2c3e50")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Dictionary to hold all pages
        self.pages = {}

        # Create Pages
        self.create_main_page()
        self.create_crud_pages()
        self.create_form_pages()
        self.create_data_display_pages()

        # Show the main page initially
        self.show_page("main")

    # Create Main Page
    def create_main_page(self):
        page = tk.Frame(self.main_frame, bg="#2c3e50")
        self.pages["main"] = page

        # Add Title
        title_label = tk.Label(page, text="Gestion de Scolarité", font=self.title_font, bg="#2c3e50", fg="white")
        title_label.pack(pady=20)

        # Create Buttons with Modern Design
        button_frame = tk.Frame(page, bg="#2c3e50")
        button_frame.pack(pady=20)

        buttons = [
            ("📚 Étudiants", "#3498db", lambda: self.show_page("crud_etudiants")),
            ("👨‍🏫 Enseignants", "#e74c3c", lambda: self.show_page("crud_enseignants")),
            ("📝 Inscriptions", "#2ecc71", lambda: self.show_page("crud_inscriptions")),
            ("📦 Modules", "#9b59b6", lambda: self.show_page("crud_modules"))
        ]

        for i, (text, color, command) in enumerate(buttons):
            button = self.create_rounded_button(button_frame, text, color, command)
            button.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

        # Configure grid to make buttons the same size
        button_frame.grid_columnconfigure(0, weight=1)

        # Add Footer
        footer = tk.Label(page, text="© 2023 Scolarité App. Tous droits réservés.", font=("Arial", 10), bg="#2c3e50", fg="white")
        footer.pack(side=tk.BOTTOM, pady=10)

    # Create Rounded Button
    def create_rounded_button(self, parent, text, color, command):
        canvas = tk.Canvas(parent, width=200, height=50, bg="#2c3e50", highlightthickness=0, bd=0)
        self.draw_rounded_rectangle(canvas, 0, 0, 200, 50, radius=20, fill=color)
        canvas.create_text(100, 25, text=text, font=self.button_font, fill="white", anchor="center")
        canvas.bind("<Button-1>", lambda e: command())
        canvas.bind("<Enter>", lambda e: self.on_enter(e, canvas, color))
        canvas.bind("<Leave>", lambda e: self.on_leave(e, canvas, color))
        return canvas

    # Draw Rounded Rectangle
    def draw_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1 + radius, y1
        ]
        canvas.create_polygon(points, **kwargs, smooth=True)

    # Button Hover Effects
    def on_enter(self, event, canvas, color):
        canvas.config(bg=self.lighten_hex(color))
        canvas.itemconfig(1, fill=self.lighten_hex(color))  # Change button background color

    def on_leave(self, event, canvas, color):
        canvas.config(bg=color)
        canvas.itemconfig(1, fill=color)  # Reset button background color

    # Lighten Hex Color
    def lighten_hex(self, hex_color, amount=30):
        rgb = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        rgb = tuple(min(255, c + amount) for c in rgb)
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

    # Create CRUD Pages
    def create_crud_pages(self):
        # CRUD Page for Étudiants
        self.create_crud_page("crud_etudiants", "Étudiants", "#3498db", "form_etudiant", "display_etudiants")
        # CRUD Page for Enseignants
        self.create_crud_page("crud_enseignants", "Enseignants", "#e74c3c", "form_enseignant", "display_enseignants")
        # CRUD Page for Inscriptions
        self.create_crud_page("crud_inscriptions", "Inscriptions", "#2ecc71", "form_inscription", "display_inscriptions")
        # CRUD Page for Modules
        self.create_crud_page("crud_modules", "Modules", "#9b59b6", "form_module", "display_modules")

    # Create a Generic CRUD Page
    def create_crud_page(self, page_name, title, color, form_page_name, display_page_name):
        page = tk.Frame(self.main_frame, bg="#2c3e50")
        self.pages[page_name] = page

        # Add Title
        title_label = tk.Label(page, text=f"Gestion des {title}", font=self.title_font, bg="#2c3e50", fg="white")
        title_label.pack(pady=20)

        # CRUD Buttons
        crud_frame = tk.Frame(page, bg="#2c3e50")
        crud_frame.pack(pady=20)

        operations = [
            ("➕ Créer", lambda: self.show_page(form_page_name)),
            ("👁️ Lire", lambda: self.show_page(display_page_name)),
            ("✏️ Mettre à jour", lambda: self.update_data(title)),
            ("🗑️ Supprimer", lambda: self.delete_data(title))
        ]

        for i, (text, command) in enumerate(operations):
            button = self.create_rounded_button(crud_frame, text, color, command)
            button.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

        # Back Button
        back_button = self.create_rounded_button(page, "🔙 Retour", "#95a5a6", lambda: self.show_page("main"))
        back_button.pack(pady=20)

        # Configure grid to make buttons the same size
        crud_frame.grid_columnconfigure(0, weight=1)

    # Create Form Pages
    def create_form_pages(self):
        # Form Page for Étudiant
        self.create_form_page("form_etudiant", "Étudiant", [
            ("Appoge", "entry"),
            ("Nom", "entry"),
            ("Prenom", "entry"),
            ("CIN", "entry"),
            ("Date de Naissance", "entry")
        ], "#3498db", "crud_etudiants", self.etudiants)
        # Form Page for Enseignant
        self.create_form_page("form_enseignant", "Enseignant", [
            ("Id", "entry"),
            ("Nom", "entry"),
            ("Prenom", "entry"),
            ("CIN", "entry"),
            ("Département", "entry")
        ], "#e74c3c", "crud_enseignants", self.enseignants)
        # Form Page for Module
        self.create_form_page("form_module", "Module", [
            ("Id", "entry"),
            ("Matière", "entry"),
            ("Semester", "dropdown", list(range(1, 7)))  # Dropdown for semester
        ], "#9b59b6", "crud_modules", self.modules)
        # Form Page for Inscription
        self.create_form_page("form_inscription", "Inscription", [
            ("Id-étudiant", "entry"),
            ("Id-module", "entry"),
            ("Note", "entry"),
            ("Valide", "dropdown", ["V", "Rat", "AC"])  # Dropdown for validation status
        ], "#2ecc71", "crud_inscriptions", self.inscriptions)

    # Create a Generic Form Page
    def create_form_page(self, page_name, title, fields, color, crud_page_name, data_store):
        page = tk.Frame(self.main_frame, bg="#2c3e50")
        self.pages[page_name] = page

        # Add Title
        title_label = tk.Label(page, text=f"Ajouter {title}", font=self.title_font, bg="#2c3e50", fg="white")
        title_label.pack(pady=10)

        # Form Fields
        form_frame = tk.Frame(page, bg="#2c3e50")
        form_frame.pack(pady=20)

        entries = {}
        for i, (label, field_type, *options) in enumerate(fields):
            label_widget = tk.Label(form_frame, text=label, font=self.label_font, bg="#2c3e50", fg="white")
            label_widget.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            if field_type == "entry":
                entry = tk.Entry(form_frame, font=self.label_font)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
                entries[label] = entry
            elif field_type == "dropdown":
                dropdown = ttk.Combobox(form_frame, values=options[0], font=self.label_font, state="readonly")
                dropdown.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
                dropdown.current(0)  # Set default value
                entries[label] = dropdown

        # Submit Button
        submit_button = self.create_rounded_button(form_frame, "✅ Soumettre", color, lambda: self.submit_form(page, fields, entries, data_store, crud_page_name))
        submit_button.grid(row=len(fields), column=0, columnspan=2, pady=20, sticky="ew")

        # Back Button
        back_button = self.create_rounded_button(page, "🔙 Retour", "#95a5a6", lambda: self.show_page(crud_page_name))
        back_button.pack(pady=20)

        # Configure grid to make fields expand
        form_frame.grid_columnconfigure(1, weight=1)

    # Submit Form Data
    def submit_form(self, page, fields, entries, data_store, crud_page_name):
        data = {}
        for label, field_type, *options in fields:
            if field_type == "entry":
                value = entries[label].get()
                if not value:
                    messagebox.showwarning("Erreur", f"Le champ '{label}' est obligatoire.")
                    return
                data[label] = value
            elif field_type == "dropdown":
                data[label] = entries[label].get()

        data_store.append(data)
        messagebox.showinfo("Succès", f"{len(data_store)} entrées enregistrées.")
        self.show_page(crud_page_name)

    # Create Data Display Pages
    def create_data_display_pages(self):
        # Display Page for Étudiants
        self.create_data_display_page("display_etudiants", "Étudiants", self.etudiants)
        # Display Page for Enseignants
        self.create_data_display_page("display_enseignants", "Enseignants", self.enseignants)
        # Display Page for Modules
        self.create_data_display_page("display_modules", "Modules", self.modules)
        # Display Page for Inscriptions
        self.create_data_display_page("display_inscriptions", "Inscriptions", self.inscriptions)

    # Create a Generic Data Display Page
    def create_data_display_page(self, page_name, title, data_store):
        page = tk.Frame(self.main_frame, bg="#2c3e50")
        self.pages[page_name] = page

        # Add Title
        title_label = tk.Label(page, text=f"Liste des {title}", font=self.title_font, bg="#2c3e50", fg="white")
        title_label.pack(pady=20)

        # Data Display Frame
        display_frame = tk.Frame(page, bg="#2c3e50")
        display_frame.pack(pady=20)

        if not data_store:
            no_data_label = tk.Label(display_frame, text="Aucune donnée disponible.", font=self.label_font, bg="#2c3e50", fg="white")
            no_data_label.pack()
        else:
            # Create a Treeview to display data
            columns = list(data_store[0].keys())
            tree = ttk.Treeview(display_frame, columns=columns, show="headings")
            for col in columns:
                tree.heading(col, text=col)
            for item in data_store:
                tree.insert("", "end", values=list(item.values()))
            tree.pack()

        # Back Button
        back_button = self.create_rounded_button(page, "🔙 Retour", "#95a5a6", lambda: self.show_page(f"crud_{title.lower()}"))
        back_button.pack(pady=20)

    # Show a Specific Page
    def show_page(self, page_name):
        for page in self.pages.values():
            page.pack_forget()  # Hide all pages
        self.pages[page_name].pack(fill=tk.BOTH, expand=True)  # Show the requested page

    # Placeholder Methods for CRUD Operations
    def update_data(self, title):
        messagebox.showinfo("Mettre à jour", f"Mettre à jour les données pour {title}")

    def delete_data(self, title):
        messagebox.showinfo("Supprimer", f"Supprimer les données pour {title}")


# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ScolariteApp(root)
    root.mainloop()