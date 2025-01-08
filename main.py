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

        # Main Container for Pages
        self.main_frame = tk.Frame(self.root, bg="#2c3e50")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Dictionary to hold all pages
        self.pages = {}

        # Create Pages
        self.create_main_page()
        self.create_crud_pages()
        self.create_form_pages()

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
            ("Gérer Étudiants", "#3498db", lambda: self.show_page("crud_etudiants")),
            ("Gérer Enseignants", "#e74c3c", lambda: self.show_page("crud_enseignants")),
            ("Gérer Inscriptions", "#2ecc71", lambda: self.show_page("crud_inscriptions")),
            ("Gérer Modules", "#9b59b6", lambda: self.show_page("crud_modules"))
        ]

        for i, (text, color, command) in enumerate(buttons):
            button = tk.Button(button_frame, text=text, font=self.button_font, bg=color, fg="white",
                               activebackground=color, activeforeground="white", bd=0, padx=20, pady=10,
                               command=command)
            button.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

        # Configure grid to make buttons the same size
        button_frame.grid_columnconfigure(0, weight=1)

        # Add Footer
        footer = tk.Label(page, text="© 2023 Scolarité App. Tous droits réservés.", font=("Arial", 10), bg="#2c3e50", fg="white")
        footer.pack(side=tk.BOTTOM, pady=10)

    # Create CRUD Pages
    def create_crud_pages(self):
        # CRUD Page for Étudiants
        self.create_crud_page("crud_etudiants", "Étudiants", "#3498db", "form_etudiant")
        # CRUD Page for Enseignants
        self.create_crud_page("crud_enseignants", "Enseignants", "#e74c3c", "form_enseignant")
        # CRUD Page for Inscriptions
        self.create_crud_page("crud_inscriptions", "Inscriptions", "#2ecc71", "form_inscription")
        # CRUD Page for Modules
        self.create_crud_page("crud_modules", "Modules", "#9b59b6", "form_module")

    # Create a Generic CRUD Page
    def create_crud_page(self, page_name, title, color, form_page_name):
        page = tk.Frame(self.main_frame, bg="#2c3e50")
        self.pages[page_name] = page

        # Add Title
        title_label = tk.Label(page, text=f"Gestion des {title}", font=self.title_font, bg="#2c3e50", fg="white")
        title_label.pack(pady=20)

        # CRUD Buttons
        crud_frame = tk.Frame(page, bg="#2c3e50")
        crud_frame.pack(pady=20)

        operations = [
            ("Créer", lambda: self.show_page(form_page_name)),
            ("Lire", lambda: self.show_data(title)),
            ("Mettre à jour", lambda: self.update_data(title)),
            ("Supprimer", lambda: self.delete_data(title))
        ]

        for i, (text, command) in enumerate(operations):
            button = tk.Button(crud_frame, text=text, font=self.button_font, bg=color, fg="white",
                               activebackground=color, activeforeground="white", bd=0, padx=20, pady=10,
                               command=command)
            button.grid(row=i, column=0, padx=10, pady=10, sticky="ew")

        # Back Button
        back_button = tk.Button(page, text="Retour", font=self.button_font, bg="#95a5a6", fg="white",
                                activebackground="#7f8c8d", activeforeground="white", bd=0, padx=20, pady=10,
                                command=lambda: self.show_page("main"))
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
        ], "#3498db", "crud_etudiants")
        # Form Page for Enseignant
        self.create_form_page("form_enseignant", "Enseignant", [
            ("Id", "entry"),
            ("Nom", "entry"),
            ("Prenom", "entry"),
            ("CIN", "entry"),
            ("Département", "entry")
        ], "#e74c3c", "crud_enseignants")
        # Form Page for Module
        self.create_form_page("form_module", "Module", [
            ("Id", "entry"),
            ("Matière", "entry"),
            ("Semester", "dropdown", list(range(1, 7)))  # Dropdown for semester
        ], "#9b59b6", "crud_modules")
        # Form Page for Inscription
        self.create_form_page("form_inscription", "Inscription", [
            ("Id-étudiant", "entry"),
            ("Id-module", "entry"),
            ("Note", "entry"),
            ("Valide", "dropdown", ["V", "Rat", "AC"])  # Dropdown for validation status
        ], "#2ecc71", "crud_inscriptions")

    # Create a Generic Form Page
    def create_form_page(self, page_name, title, fields, color, crud_page_name):
        page = tk.Frame(self.main_frame, bg="#2c3e50")
        self.pages[page_name] = page

        # Add Title
        title_label = tk.Label(page, text=f"Ajouter {title}", font=self.title_font, bg="#2c3e50", fg="white")
        title_label.pack(pady=10)

        # Form Fields
        form_frame = tk.Frame(page, bg="#2c3e50")
        form_frame.pack(pady=20)

        for i, (label, field_type, *options) in enumerate(fields):
            label_widget = tk.Label(form_frame, text=label, font=self.label_font, bg="#2c3e50", fg="white")
            label_widget.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            if field_type == "entry":
                entry = tk.Entry(form_frame, font=self.label_font)
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            elif field_type == "dropdown":
                dropdown = ttk.Combobox(form_frame, values=options[0], font=self.label_font, state="readonly")
                dropdown.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
                dropdown.current(0)  # Set default value

        # Submit Button
        submit_button = tk.Button(form_frame, text="Soumettre", font=self.button_font, bg=color, fg="white",
                                  activebackground=color, activeforeground="white", bd=0, padx=20, pady=10,
                                  command=lambda: self.submit_form(page, fields))
        submit_button.grid(row=len(fields), column=0, columnspan=2, pady=20, sticky="ew")

        # Back Button
        back_button = tk.Button(page, text="Retour", font=self.button_font, bg="#95a5a6", fg="white",
                                activebackground="#7f8c8d", activeforeground="white", bd=0, padx=20, pady=10,
                                command=lambda: self.show_page(crud_page_name))
        back_button.pack(pady=20)

        # Configure grid to make fields expand
        form_frame.grid_columnconfigure(1, weight=1)

    # Show a Specific Page
    def show_page(self, page_name):
        for page in self.pages.values():
            page.pack_forget()  # Hide all pages
        self.pages[page_name].pack(fill=tk.BOTH, expand=True)  # Show the requested page

    # Submit Form Data
    def submit_form(self, page, fields):
        data = {}
        for i, (label, field_type, *options) in enumerate(fields):
            if field_type == "entry":
                entry = page.grid_slaves(row=i, column=1)[0]
                data[label] = entry.get()
            elif field_type == "dropdown":
                dropdown = page.grid_slaves(row=i, column=1)[0]
                data[label] = dropdown.get()

        messagebox.showinfo("Données Soumises", f"Données: {data}")

    # Placeholder Methods for CRUD Operations
    def show_data(self, title):
        messagebox.showinfo("Lire", f"Afficher les données pour {title}")

    def update_data(self, title):
        messagebox.showinfo("Mettre à jour", f"Mettre à jour les données pour {title}")

    def delete_data(self, title):
        messagebox.showinfo("Supprimer", f"Supprimer les données pour {title}")


# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ScolariteApp(root)
    root.mainloop()