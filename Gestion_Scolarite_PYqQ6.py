import sqlite3
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *


def connect_db():
    return sqlite3.connect("Gestion_Scolarite.db")


class Enseignant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Enseignants")
        self.setGeometry(300, 300, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

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

        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Ajouter Enseignant")
        self.add_btn.setFixedWidth(200)
        self.add_btn.clicked.connect(self.ajouter_enseignant)
        button_layout.addWidget(self.add_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addLayout(button_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Nom", "Prénom", "CIN", "Département", "Supprimer"])
        self.layout.addWidget(self.table)

        self.lister_enseignant()

    def ajouter_enseignant(self):
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
            self.lister_enseignant()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def lister_enseignant(self):
        self.table.setRowCount(0)

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("SELECT id, nom, prenom, cin, departement FROM Enseignant;")
            enseignants = curs.fetchall()
            conn.close()

            self.table.setRowCount(len(enseignants))
            for i, ens in enumerate(enseignants):
                for j, data in enumerate(ens[1:]):
                    self.table.setItem(i, j, QTableWidgetItem(str(data)))

                del_btn = QPushButton("Supprimer")
                del_btn.clicked.connect(lambda _, id=enseignants[i][0]: self.supprimer_enseignant(id))
                self.table.setCellWidget(i, 4, del_btn)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def supprimer_enseignant(self, ens_id):
        try:
            print(ens_id)
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("DELETE FROM Enseignant WHERE id = ?", (ens_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", "Enseignant supprimé avec succès!")
            self.lister_enseignant()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")
    def clear_inputs(self):
        self.nom_input.clear()
        self.prenom_input.clear()
        self.cin_input.clear()
        self.departement_input.clear()

    def existe(self, id):
        conn = connect_db()
        curs = conn.cursor()

        curs.execute("SELECT * FROM Enseignant WHERE id = ?", (id,))
        res = curs.fetchone()

        conn.close()

        return res is not None


# Run the application
app = QApplication([])
window = Enseignant()
window.show()
app.exec()
