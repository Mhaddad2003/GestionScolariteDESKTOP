import sqlite3
from PyQt6.QtWidgets import *

def connect_db():
    return sqlite3.connect("Gestion_Scolarite.db")

class InscriptionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Inscriptions")
        self.setGeometry(300, 300, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Form Layout
        form_layout = QFormLayout()
        self.module_id_input = QLineEdit()
        self.etudiant_apogee_input = QLineEdit()
        self.note_input = QLineEdit()
        self.valide_input = QLineEdit()

        form_layout.addRow("ID Module:", self.module_id_input)
        form_layout.addRow("Numéro Apogée:", self.etudiant_apogee_input)
        form_layout.addRow("Note:", self.note_input)
        form_layout.addRow("Validé:", self.valide_input)
        self.layout.addLayout(form_layout)

        # Buttons Layout
        button_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Effacer les Champs")
        self.clear_btn.clicked.connect(self.clear_inputs)
        button_layout.addWidget(self.clear_btn)

        self.add_btn = QPushButton("Ajouter Inscription")
        self.add_btn.clicked.connect(self.ajouter_inscription)
        button_layout.addWidget(self.add_btn)

        self.layout.addLayout(button_layout)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID Module", "Numéro Apogée", "Note", "Validé", "Actions"])
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

        # Check if module_id exists
        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("SELECT 1 FROM Module WHERE id = ?", (module_id,))
            if not curs.fetchone():
                QMessageBox.warning(self, "Erreur", "Le module avec cet ID n'existe pas!")
                return

            # Check if etudiant_apogee exists
            curs.execute("SELECT 1 FROM Etudiant WHERE num_apogee = ?", (etudiant_apogee,))
            if not curs.fetchone():
                QMessageBox.warning(self, "Erreur", "L'étudiant avec ce numéro d'apogée n'existe pas!")
                return

            # Insert the inscription
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

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = InscriptionApp()
    window.show()
    app.exec()