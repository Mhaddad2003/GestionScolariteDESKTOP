import sqlite3
from PyQt6.QtWidgets import *

def connect_db():
    return sqlite3.connect("Gestion_Scolarite.db")

class EnseignantApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Enseignants")
        self.setGeometry(300, 300, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Form Layout
        form_layout = QFormLayout()
        self.nom_input = QLineEdit()
        self.prenom_input = QLineEdit()
        self.cin_input = QLineEdit()
        self.departement_input = QLineEdit()

        form_layout.addRow("Nom:", self.nom_input)
        form_layout.addRow("Prénom:", self.prenom_input)
        form_layout.addRow("CIN:", self.cin_input)
        form_layout.addRow("Département:", self.departement_input)
        self.layout.addLayout(form_layout)

        # Buttons Layout
        button_layout = QHBoxLayout()
        self.clear_btn = QPushButton("Effacer les Champs")
        self.clear_btn.clicked.connect(self.clear_inputs)
        button_layout.addWidget(self.clear_btn)

        self.add_btn = QPushButton("Ajouter Enseignant")
        self.add_btn.clicked.connect(self.ajouter_enseignant)
        button_layout.addWidget(self.add_btn)

        self.layout.addLayout(button_layout)

        # Table Widget
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "CIN", "Département", "Supprimer", "Modifier"])
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
                del_btn.clicked.connect(lambda _, id=ens[0]: self.supprimer_enseignant(id))
                self.table.setCellWidget(i, 5, del_btn)

                # Modify Button
                mod_btn = QPushButton("Modifier")
                mod_btn.clicked.connect(lambda _, id=ens[0]: self.modifier_enseignant(id))
                self.table.setCellWidget(i, 6, mod_btn)
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
    connect_db()  # Ensure the database and table are created
    app = QApplication([])
    window = EnseignantApp()
    window.show()
    app.exec()