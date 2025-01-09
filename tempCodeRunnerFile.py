import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import QSize


# Database Connection
def connect_db():
    return sqlite3.connect("Gestion_Scolarite.db")


# Create Database and Table if Not Exists
def initialize_db():
    conn = connect_db()
    curs = conn.cursor()
    curs.execute("""
    CREATE TABLE IF NOT EXISTS Enseignant (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        cin TEXT NOT NULL,
        departement TEXT NOT NULL
    );
    """)
    conn.commit()
    conn.close()


# Main Application Window
class EnseignantApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Enseignants")
        self.setGeometry(300, 300, 1200, 800)  # Adjusted window size
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Title Label
        title_label = QLabel("Gestion des Enseignants")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 30px;")
        self.layout.addWidget(title_label)

        # Form Layout
        form_layout = QFormLayout()
        form_layout.setSpacing(20)  # Add spacing between form rows
        form_layout.setContentsMargins(50, 20, 50, 20)  # Add margins

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
        button_layout.setSpacing(20)  # Add spacing between buttons
        button_layout.setContentsMargins(50, 0, 50, 0)  # Add margins

        # Clear Button
        self.clear_btn = QPushButton("Effacer les Champs")
        self.clear_btn.setFixedWidth(180)
        self.clear_btn.setIcon(QIcon("clear_icon.png"))  # Add an icon
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
        self.add_btn.setIcon(QIcon("add_icon.png"))  # Add an icon
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
                del_btn.setIcon(QIcon("delete_icon.png"))  # Add an icon
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


# Run the application
if __name__ == "__main__":
    initialize_db()  # Ensure the database and table are created
    app = QApplication([])
    window = EnseignantApp()
    window.show()
    app.exec()