import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QSize

# Database Connection
def connect_db():
    return sqlite3.connect("Gestion_Scolarite.db")

# Main Application Window
class GestionScolariteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion Scolarité")
        self.setGeometry(300, 300, 1200, 800)
        self.central_widget = QTabWidget()
        self.setCentralWidget(self.central_widget)

        # Add tabs for each table
        self.central_widget.addTab(EnseignantTab(), "Enseignants")
        self.central_widget.addTab(EtudiantTab(), "Étudiants")
        self.central_widget.addTab(ModuleTab(), "Modules")
        self.central_widget.addTab(InscrireTab(), "Inscriptions")

# Enseignant Tab
class EnseignantTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title Label
        title_label = QLabel("Gestion des Enseignants")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 30px;")
        self.layout.addWidget(title_label)

        # Form Layout
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(50, 20, 50, 20)

        # Input Fields
        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()
        self.cin_input = QLineEdit()
        self.departement_input = QLineEdit()

        # Set placeholder text for inputs
        self.nom_input.setPlaceholderText("Entrez le nom")
        self.prenom_input.setPlaceholderText("Entrez le prénom")
        self.cin_input.setPlaceholderText("Entrez le CIN")
        self.departement_input.setPlaceholderText("Entrez le département")

        # Style Input Fields
        input_style = """
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """
        self.nom_input.setStyleSheet(input_style)
        self.prenom_input.setStyleSheet(input_style)
        self.cin_input.setStyleSheet(input_style)
        self.departement_input.setStyleSheet(input_style)

        # Add fields to form layout
        form_layout.addRow("Nom:", self.nom_input)
        form_layout.addRow("Prénom:", self.prenom_input)
        form_layout.addRow("CIN:", self.cin_input)
        form_layout.addRow("Département:", self.departement_input)
        self.layout.addLayout(form_layout)

        # Buttons Layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(50, 0, 50, 0)

        # Clear Button
        self.clear_btn = QPushButton("Effacer les Champs")
        self.clear_btn.setFixedWidth(180)
        self.clear_btn.setIcon(QIcon("clear_icon.png"))
        self.clear_btn.setIconSize(QSize(20, 20))
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_inputs)
        button_layout.addWidget(self.clear_btn)

        # Add/Update Button
        self.add_btn = QPushButton("Ajouter Enseignant")
        self.add_btn.setFixedWidth(180)
        self.add_btn.setIcon(QIcon("add_icon.png"))
        self.add_btn.setIconSize(QSize(20, 20))
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.add_btn.clicked.connect(self.ajouter_enseignant)
        button_layout.addWidget(self.add_btn)

        self.layout.addLayout(button_layout)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "CIN", "Département", "Actions"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f5f6fa;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.layout.addWidget(self.table)

        # Load data into the table
        self.lister_enseignants()

    def ajouter_enseignant(self):
        """Add a new Enseignant to the database."""
        nom = self.nom_input.text()
        prenom = self.prenom_input.text()
        cin = self.cin_input.text()
        departement = self.departement_input.text()

        if not nom or not prenom or not cin or not departement:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis!")
            return

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("""
            INSERT INTO Enseignant (nom, prenom, cin, departement) 
            VALUES (?, ?, ?, ?);
            """, (nom, prenom, cin, departement))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", "Enseignant ajouté avec succès!")
            self.clear_inputs()
            self.lister_enseignants()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def lister_enseignants(self):
        """List all Enseignants in the table."""
        self.table.setRowCount(0)

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("SELECT * FROM Enseignant;")
            enseignants = curs.fetchall()
            conn.close()

            self.table.setRowCount(len(enseignants))
            for i, ens in enumerate(enseignants):
                for j, data in enumerate(ens):
                    self.table.setItem(i, j, QTableWidgetItem(str(data)))

                # Delete Button
                del_btn = QPushButton("Supprimer")
                del_btn.setIcon(QIcon("delete_icon.png"))
                del_btn.setIconSize(QSize(20, 20))
                del_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        border: none;
                        padding: 5px;
                        border-radius: 3px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                """)
                del_btn.clicked.connect(lambda _, id=ens[0]: self.supprimer_enseignant(id))
                self.table.setCellWidget(i, 5, del_btn)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def supprimer_enseignant(self, ens_id):
        """Delete an Enseignant from the database."""
        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("DELETE FROM Enseignant WHERE id = ?", (ens_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", f"Enseignant avec l'id {ens_id} supprimé!")
            self.lister_enseignants()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def clear_inputs(self):
        """Clear all input fields."""
        self.nom_input.clear()
        self.prenom_input.clear()
        self.cin_input.clear()
        self.departement_input.clear()

    def modifier_enseignant(self, ens_id):
        """Load Enseignant data into the form for editing."""
        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("SELECT nom, prenom, cin, departement FROM Enseignant WHERE id = ?", (ens_id,))
            enseignant = curs.fetchone()
            conn.close()

            if enseignant:
                self.nom_input.setText(enseignant[0])
                self.prenom_input.setText(enseignant[1])
                self.cin_input.setText(enseignant[2])
                self.departement_input.setText(enseignant[3])

                self.add_btn.setText("Modifier Enseignant")
                self.add_btn.clicked.disconnect()
                self.add_btn.clicked.connect(lambda: self.applique_Modification(ens_id))
            else:
                QMessageBox.critical(self, "Erreur", f"Aucun enseignant trouvé avec l'id {ens_id}!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def applique_Modification(self, ens_id):
        """Update an Enseignant in the database."""
        nom = self.nom_input.text()
        prenom = self.prenom_input.text()
        cin = self.cin_input.text()
        departement = self.departement_input.text()

        if not nom or not prenom or not cin or not departement:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis!")
            return

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute(""" UPDATE Enseignant 
               SET nom = ?, prenom = ?, cin = ?, departement = ? 
               WHERE id = ?;""", (nom, prenom, cin, departement, ens_id))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", "Enseignant modifié avec succès!")
            self.clear_inputs()
            self.lister_enseignants()

            self.add_btn.setText("Ajouter Enseignant")
            self.add_btn.clicked.disconnect()
            self.add_btn.clicked.connect(self.ajouter_enseignant)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

# Etudiant Tab
class EtudiantTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title Label
        title_label = QLabel("Gestion des Étudiants")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 30px;")
        self.layout.addWidget(title_label)

        # Form Layout
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(50, 20, 50, 20)

        # Input Fields
        self.num_apogee_input = QLineEdit()
        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()
        self.cin_input = QLineEdit()
        self.date_naiss_input = QDateEdit()
        self.date_naiss_input.setCalendarPopup(True)

        # Set placeholder text for inputs
        self.num_apogee_input.setPlaceholderText("Entrez le numéro d'apogée")
        self.nom_input.setPlaceholderText("Entrez le nom")
        self.prenom_input.setPlaceholderText("Entrez le prénom")
        self.cin_input.setPlaceholderText("Entrez le CIN")

        # Style Input Fields
        input_style = """
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
            QDateEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QDateEdit:focus {
                border-color: #3498db;
            }
        """
        self.num_apogee_input.setStyleSheet(input_style)
        self.nom_input.setStyleSheet(input_style)
        self.prenom_input.setStyleSheet(input_style)
        self.cin_input.setStyleSheet(input_style)
        self.date_naiss_input.setStyleSheet(input_style)

        # Add fields to form layout
        form_layout.addRow("Numéro Apogée:", self.num_apogee_input)
        form_layout.addRow("Nom:", self.nom_input)
        form_layout.addRow("Prénom:", self.prenom_input)
        form_layout.addRow("CIN:", self.cin_input)
        form_layout.addRow("Date de Naissance:", self.date_naiss_input)
        self.layout.addLayout(form_layout)

        # Buttons Layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(50, 0, 50, 0)

        # Clear Button
        self.clear_btn = QPushButton("Effacer les Champs")
        self.clear_btn.setFixedWidth(180)
        self.clear_btn.setIcon(QIcon("clear_icon.png"))
        self.clear_btn.setIconSize(QSize(20, 20))
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_inputs)
        button_layout.addWidget(self.clear_btn)

        # Add/Update Button
        self.add_btn = QPushButton("Ajouter Étudiant")
        self.add_btn.setFixedWidth(180)
        self.add_btn.setIcon(QIcon("add_icon.png"))
        self.add_btn.setIconSize(QSize(20, 20))
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.add_btn.clicked.connect(self.ajouter_etudiant)
        button_layout.addWidget(self.add_btn)

        self.layout.addLayout(button_layout)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Numéro Apogée", "Nom", "Prénom", "CIN", "Date de Naissance", "Actions"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f5f6fa;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.layout.addWidget(self.table)

        # Load data into the table
        self.lister_etudiants()

    def ajouter_etudiant(self):
        """Add a new Étudiant to the database."""
        num_apogee = self.num_apogee_input.text()
        nom = self.nom_input.text()
        prenom = self.prenom_input.text()
        cin = self.cin_input.text()
        date_naiss = self.date_naiss_input.date().toString("yyyy-MM-dd")

        if not num_apogee or not nom or not prenom or not cin:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis!")
            return

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("""
            INSERT INTO Etudiant (num_apogee, nom, prenom, cin, date_naiss) 
            VALUES (?, ?, ?, ?, ?);
            """, (num_apogee, nom, prenom, cin, date_naiss))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", "Étudiant ajouté avec succès!")
            self.clear_inputs()
            self.lister_etudiants()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def lister_etudiants(self):
        """List all Étudiants in the table."""
        self.table.setRowCount(0)

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("SELECT * FROM Etudiant;")
            etudiants = curs.fetchall()
            conn.close()

            self.table.setRowCount(len(etudiants))
            for i, etud in enumerate(etudiants):
                for j, data in enumerate(etud):
                    self.table.setItem(i, j, QTableWidgetItem(str(data)))

                # Delete Button
                del_btn = QPushButton("Supprimer")
                del_btn.setIcon(QIcon("delete_icon.png"))
                del_btn.setIconSize(QSize(20, 20))
                del_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        border: none;
                        padding: 5px;
                        border-radius: 3px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                """)
                del_btn.clicked.connect(lambda _, num_apogee=etud[0]: self.supprimer_etudiant(num_apogee))
                self.table.setCellWidget(i, 5, del_btn)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def supprimer_etudiant(self, num_apogee):
        """Delete an Étudiant from the database."""
        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("DELETE FROM Etudiant WHERE num_apogee = ?", (num_apogee,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", f"Étudiant avec le numéro d'apogée {num_apogee} supprimé!")
            self.lister_etudiants()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def clear_inputs(self):
        """Clear all input fields."""
        self.num_apogee_input.clear()
        self.nom_input.clear()
        self.prenom_input.clear()
        self.cin_input.clear()
        self.date_naiss_input.setDate(self.date_naiss_input.minimumDate())

    def modifier_etudiant(self, num_apogee):
        """Load Étudiant data into the form for editing."""
        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("SELECT nom, prenom, cin, date_naiss FROM Etudiant WHERE num_apogee = ?", (num_apogee,))
            etudiant = curs.fetchone()
            conn.close()

            if etudiant:
                self.nom_input.setText(etudiant[0])
                self.prenom_input.setText(etudiant[1])
                self.cin_input.setText(etudiant[2])
                self.date_naiss_input.setDate(etudiant[3])

                self.add_btn.setText("Modifier Étudiant")
                self.add_btn.clicked.disconnect()
                self.add_btn.clicked.connect(lambda: self.applique_Modification(num_apogee))
            else:
                QMessageBox.critical(self, "Erreur", f"Aucun étudiant trouvé avec le numéro d'apogée {num_apogee}!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def applique_Modification(self, num_apogee):
        """Update an Étudiant in the database."""
        nom = self.nom_input.text()
        prenom = self.prenom_input.text()
        cin = self.cin_input.text()
        date_naiss = self.date_naiss_input.date().toString("yyyy-MM-dd")

        if not nom or not prenom or not cin:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis!")
            return

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute(""" UPDATE Etudiant 
               SET nom = ?, prenom = ?, cin = ?, date_naiss = ? 
               WHERE num_apogee = ?;""", (nom, prenom, cin, date_naiss, num_apogee))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", "Étudiant modifié avec succès!")
            self.clear_inputs()
            self.lister_etudiants()

            self.add_btn.setText("Ajouter Étudiant")
            self.add_btn.clicked.disconnect()
            self.add_btn.clicked.connect(self.ajouter_etudiant)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

# Module Tab
class ModuleTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title Label
        title_label = QLabel("Gestion des Modules")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 30px;")
        self.layout.addWidget(title_label)

        # Form Layout
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(50, 20, 50, 20)

        # Input Fields
        self.enseignant_id_input = QLineEdit()
        self.matiere_input = QLineEdit()
        self.semestre_input = QLineEdit()

        # Set placeholder text for inputs
        self.enseignant_id_input.setPlaceholderText("Entrez l'ID de l'enseignant")
        self.matiere_input.setPlaceholderText("Entrez la matière")
        self.semestre_input.setPlaceholderText("Entrez le semestre")

        # Style Input Fields
        input_style = """
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """
        self.enseignant_id_input.setStyleSheet(input_style)
        self.matiere_input.setStyleSheet(input_style)
        self.semestre_input.setStyleSheet(input_style)

        # Add fields to form layout
        form_layout.addRow("ID Enseignant:", self.enseignant_id_input)
        form_layout.addRow("Matière:", self.matiere_input)
        form_layout.addRow("Semestre:", self.semestre_input)
        self.layout.addLayout(form_layout)

        # Buttons Layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(50, 0, 50, 0)

        # Clear Button
        self.clear_btn = QPushButton("Effacer les Champs")
        self.clear_btn.setFixedWidth(180)
        self.clear_btn.setIcon(QIcon("clear_icon.png"))
        self.clear_btn.setIconSize(QSize(20, 20))
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_inputs)
        button_layout.addWidget(self.clear_btn)

        # Add/Update Button
        self.add_btn = QPushButton("Ajouter Module")
        self.add_btn.setFixedWidth(180)
        self.add_btn.setIcon(QIcon("add_icon.png"))
        self.add_btn.setIconSize(QSize(20, 20))
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.add_btn.clicked.connect(self.ajouter_module)
        button_layout.addWidget(self.add_btn)

        self.layout.addLayout(button_layout)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "ID Enseignant", "Matière", "Semestre", "Actions"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f5f6fa;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.layout.addWidget(self.table)

        # Load data into the table
        self.lister_modules()

    def ajouter_module(self):
        """Add a new Module to the database."""
        enseignant_id = self.enseignant_id_input.text()
        matiere = self.matiere_input.text()
        semestre = self.semestre_input.text()

        if not enseignant_id or not matiere or not semestre:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis!")
            return

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("""
            INSERT INTO Module (Enseignant_id, matiere, semestre) 
            VALUES (?, ?, ?);
            """, (enseignant_id, matiere, semestre))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", "Module ajouté avec succès!")
            self.clear_inputs()
            self.lister_modules()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def lister_modules(self):
        """List all Modules in the table."""
        self.table.setRowCount(0)

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("SELECT * FROM Module;")
            modules = curs.fetchall()
            conn.close()

            self.table.setRowCount(len(modules))
            for i, mod in enumerate(modules):
                for j, data in enumerate(mod):
                    self.table.setItem(i, j, QTableWidgetItem(str(data)))

                # Delete Button
                del_btn = QPushButton("Supprimer")
                del_btn.setIcon(QIcon("delete_icon.png"))
                del_btn.setIconSize(QSize(20, 20))
                del_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        border: none;
                        padding: 5px;
                        border-radius: 3px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                """)
                del_btn.clicked.connect(lambda _, id=mod[0]: self.supprimer_module(id))
                self.table.setCellWidget(i, 4, del_btn)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def supprimer_module(self, mod_id):
        """Delete a Module from the database."""
        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("DELETE FROM Module WHERE id = ?", (mod_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", f"Module avec l'id {mod_id} supprimé!")
            self.lister_modules()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def clear_inputs(self):
        """Clear all input fields."""
        self.enseignant_id_input.clear()
        self.matiere_input.clear()
        self.semestre_input.clear()

    def modifier_module(self, mod_id):
        """Load Module data into the form for editing."""
        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("SELECT Enseignant_id, matiere, semestre FROM Module WHERE id = ?", (mod_id,))
            module = curs.fetchone()
            conn.close()

            if module:
                self.enseignant_id_input.setText(str(module[0]))
                self.matiere_input.setText(module[1])
                self.semestre_input.setText(module[2])

                self.add_btn.setText("Modifier Module")
                self.add_btn.clicked.disconnect()
                self.add_btn.clicked.connect(lambda: self.applique_Modification(mod_id))
            else:
                QMessageBox.critical(self, "Erreur", f"Aucun module trouvé avec l'id {mod_id}!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def applique_Modification(self, mod_id):
        """Update a Module in the database."""
        enseignant_id = self.enseignant_id_input.text()
        matiere = self.matiere_input.text()
        semestre = self.semestre_input.text()

        if not enseignant_id or not matiere or not semestre:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis!")
            return

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute(""" UPDATE Module 
               SET Enseignant_id = ?, matiere = ?, semestre = ? 
               WHERE id = ?;""", (enseignant_id, matiere, semestre, mod_id))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", "Module modifié avec succès!")
            self.clear_inputs()
            self.lister_modules()

            self.add_btn.setText("Ajouter Module")
            self.add_btn.clicked.disconnect()
            self.add_btn.clicked.connect(self.ajouter_module)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

# Inscrire Tab
class InscrireTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title Label
        title_label = QLabel("Gestion des Inscriptions")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 30px;")
        self.layout.addWidget(title_label)

        # Form Layout
        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(50, 20, 50, 20)

        # Input Fields
        self.module_id_input = QLineEdit()
        self.etudiant_apogee_input = QLineEdit()
        self.note_input = QLineEdit()
        self.valide_input = QLineEdit()

        # Set placeholder text for inputs
        self.module_id_input.setPlaceholderText("Entrez l'ID du module")
        self.etudiant_apogee_input.setPlaceholderText("Entrez le numéro d'apogée")
        self.note_input.setPlaceholderText("Entrez la note")
        self.valide_input.setPlaceholderText("Entrez 'Oui' ou 'Non'")

        # Style Input Fields
        input_style = """
            QLineEdit {
                padding: 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """
        self.module_id_input.setStyleSheet(input_style)
        self.etudiant_apogee_input.setStyleSheet(input_style)
        self.note_input.setStyleSheet(input_style)
        self.valide_input.setStyleSheet(input_style)

        # Add fields to form layout
        form_layout.addRow("ID Module:", self.module_id_input)
        form_layout.addRow("Numéro Apogée:", self.etudiant_apogee_input)
        form_layout.addRow("Note:", self.note_input)
        form_layout.addRow("Validé:", self.valide_input)
        self.layout.addLayout(form_layout)

        # Buttons Layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(50, 0, 50, 0)

        # Clear Button
        self.clear_btn = QPushButton("Effacer les Champs")
        self.clear_btn.setFixedWidth(180)
        self.clear_btn.setIcon(QIcon("clear_icon.png"))
        self.clear_btn.setIconSize(QSize(20, 20))
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.clear_btn.clicked.connect(self.clear_inputs)
        button_layout.addWidget(self.clear_btn)

        # Add/Update Button
        self.add_btn = QPushButton("Ajouter Inscription")
        self.add_btn.setFixedWidth(180)
        self.add_btn.setIcon(QIcon("add_icon.png"))
        self.add_btn.setIconSize(QSize(20, 20))
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        self.add_btn.clicked.connect(self.ajouter_inscription)
        button_layout.addWidget(self.add_btn)

        self.layout.addLayout(button_layout)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID Module", "Numéro Apogée", "Note", "Validé", "Actions"])
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #f5f6fa;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #34495e;
                color: white;
                padding: 10px;
                border: none;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.layout.addWidget(self.table)

        # Load data into the table
        self.lister_inscriptions()

    def ajouter_inscription(self):
        """Add a new Inscription to the database."""
        module_id = self.module_id_input.text()
        etudiant_apogee = self.etudiant_apogee_input.text()
        note = self.note_input.text()
        valide = self.valide_input.text()

        if not module_id or not etudiant_apogee or not valide:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis!")
            return

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("""
            INSERT INTO Inscrire (module_id, etudiant_apogee, note, valide) 
            VALUES (?, ?, ?, ?);
            """, (module_id, etudiant_apogee, note, valide))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", "Inscription ajoutée avec succès!")
            self.clear_inputs()
            self.lister_inscriptions()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def lister_inscriptions(self):
        """List all Inscriptions in the table."""
        self.table.setRowCount(0)

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("SELECT * FROM Inscrire;")
            inscriptions = curs.fetchall()
            conn.close()

            self.table.setRowCount(len(inscriptions))
            for i, insc in enumerate(inscriptions):
                for j, data in enumerate(insc):
                    self.table.setItem(i, j, QTableWidgetItem(str(data)))

                # Delete Button
                del_btn = QPushButton("Supprimer")
                del_btn.setIcon(QIcon("delete_icon.png"))
                del_btn.setIconSize(QSize(20, 20))
                del_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e74c3c;
                        color: white;
                        border: none;
                        padding: 5px;
                        border-radius: 3px;
                        font-size: 12px;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                """)
                del_btn.clicked.connect(lambda _, module_id=insc[0], etudiant_apogee=insc[1]: self.supprimer_inscription(module_id, etudiant_apogee))
                self.table.setCellWidget(i, 4, del_btn)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def supprimer_inscription(self, module_id, etudiant_apogee):
        """Delete an Inscription from the database."""
        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("DELETE FROM Inscrire WHERE module_id = ? AND etudiant_apogee = ?", (module_id, etudiant_apogee))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", f"Inscription supprimée!")
            self.lister_inscriptions()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def clear_inputs(self):
        """Clear all input fields."""
        self.module_id_input.clear()
        self.etudiant_apogee_input.clear()
        self.note_input.clear()
        self.valide_input.clear()

    def modifier_inscription(self, module_id, etudiant_apogee):
        """Load Inscription data into the form for editing."""
        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("SELECT note, valide FROM Inscrire WHERE module_id = ? AND etudiant_apogee = ?", (module_id, etudiant_apogee))
            inscription = curs.fetchone()
            conn.close()

            if inscription:
                self.note_input.setText(str(inscription[0]))
                self.valide_input.setText(inscription[1])

                self.add_btn.setText("Modifier Inscription")
                self.add_btn.clicked.disconnect()
                self.add_btn.clicked.connect(lambda: self.applique_Modification(module_id, etudiant_apogee))
            else:
                QMessageBox.critical(self, "Erreur", f"Aucune inscription trouvée!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def applique_Modification(self, module_id, etudiant_apogee):
        """Update an Inscription in the database."""
        note = self.note_input.text()
        valide = self.valide_input.text()

        if not valide:
            QMessageBox.warning(self, "Erreur", "Le champ 'Validé' doit être rempli!")
            return

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute(""" UPDATE Inscrire 
               SET note = ?, valide = ? 
               WHERE module_id = ? AND etudiant_apogee = ?;""", (note, valide, module_id, etudiant_apogee))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", "Inscription modifiée avec succès!")
            self.clear_inputs()
            self.lister_inscriptions()

            self.add_btn.setText("Ajouter Inscription")
            self.add_btn.clicked.disconnect()
            self.add_btn.clicked.connect(self.ajouter_inscription)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = GestionScolariteApp()
    window.show()
    app.exec()