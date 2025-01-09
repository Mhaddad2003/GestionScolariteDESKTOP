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

        self.clear_btn = QPushButton("Effacer les Champs")
        self.clear_btn.setFixedWidth(150)
        self.clear_btn.clicked.connect(self.clear_inputs)

        button_layout = QHBoxLayout()
        button_layout.addSpacing(20)

        self.add_btn = QPushButton("Ajouter Enseignant")
        self.add_btn.setFixedWidth(150)
        self.add_btn.clicked.connect(self.ajouter_enseignant)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.add_btn)
        self.layout.addLayout(button_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Nom", "Prénom", "CIN", "Département", "Supprimer", "Modifier"])
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

                update_btn = QPushButton("Modifier")
                update_btn.clicked.connect(lambda _, id=enseignants[i][0]: self.modifier_enseignant(id))
                self.table.setCellWidget(i, 5, update_btn)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def supprimer_enseignant(self, ens_id):
        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("DELETE FROM Enseignant WHERE id = ?", (ens_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", f"Enseignant avec l'id {ens_id} supprimé!")
            self.lister_enseignant()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")
    def clear_inputs(self):
        self.nom_input.clear()
        self.prenom_input.clear()
        self.cin_input.clear()
        self.departement_input.clear()

        self.switch_ajout()

    def modifier_enseignant(self, ens_id):
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
            self.lister_enseignant()

            self.switch_ajout()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def switch_ajout(self):
        self.add_btn.setText("Ajouter Enseignant")
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.ajouter_enseignant)

class Module(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestion des Modules")
        self.setGeometry(300, 300, 700, 500)
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

        # Main Layout
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)

        # Form Layout
        form_layout = QFormLayout()
        self.ens_id = QLineEdit()
        self.matiere = QLineEdit()
        self.semestre = QLineEdit()

        form_layout.addRow("Enseignant ID:", self.ens_id)
        form_layout.addRow("Matière:", self.matiere)
        form_layout.addRow("Semestre:", self.semestre)
        self.layout.addLayout(form_layout)

        # Buttons Layout
        self.clear_btn = QPushButton("Effacer les Champs")
        self.clear_btn.setFixedWidth(150)
        self.clear_btn.clicked.connect(self.clear_inputs)

        self.add_btn = QPushButton("Ajouter Module")
        self.add_btn.setFixedWidth(150)
        self.add_btn.clicked.connect(self.Ajouter_Module)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.add_btn)
        self.layout.addLayout(button_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Enseignant ID", "Matière", "Semestre", "Supprimer", "Modifier"])
        self.layout.addWidget(self.table)

        self.Lister_Module()

    def Ajouter_Module(self):
        ens_id = self.ens_id.text()
        matiere = self.matiere.text()
        semestre = self.semestre.text()

        try:
            conn = connect_db()
            curs = conn.cursor()

            if not ens_id or not matiere or not semestre:
                QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis!")
                return

            curs.execute("SELECT 1 FROM Enseignant WHERE id = ?", (ens_id,))
            if not curs.fetchone():
                QMessageBox.warning(self, "Erreur", "L'enseignant avec cet ID n'existe pas!")
                return

            curs.execute("""
                            INSERT INTO Module (Enseignant_id, matiere, semestre) 
                            VALUES (?, ?, ?);
                            """, (ens_id, matiere, semestre))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", "Module ajouté avec succès!")
            self.clear_inputs()
            self.Lister_Module()

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def Lister_Module(self):
        self.table.setRowCount(0)

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("SELECT * FROM Module;")
            modules = curs.fetchall()
            conn.close()

            self.table.setRowCount(len(modules))
            for i, module in enumerate(modules):
                for j, data in enumerate(module):
                    self.table.setItem(i, j, QTableWidgetItem(str(data)))

                # Delete Button
                del_btn = QPushButton("Supprimer")
                del_btn.clicked.connect(lambda _, id=module[0]: self.Sup_Module(id))
                self.table.setCellWidget(i, 4, del_btn)

                update_btn = QPushButton("Modifier")
                update_btn.clicked.connect(lambda _, id=module[0]: self.Modifier_Module(id))
                self.table.setCellWidget(i, 5, update_btn)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def Sup_Module(self, module_id):
        try:
            print(module_id)
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("DELETE FROM Module WHERE id = ?", (module_id,))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", f"Module avec l'id {module_id} supprimé!")
            self.Lister_Module()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def clear_inputs(self):
        self.ens_id.clear()
        self.matiere.clear()
        self.semestre.clear()
        self.switch_ajout()

    def Modifier_Module(self, module_id):
        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute("SELECT Enseignant_id, matiere, semestre FROM Module WHERE id = ?", (module_id,))
            module = curs.fetchone()
            print("hi")
            conn.close()

            if module:
                print(module)
                self.ens_id.setText(str(module[0]))
                self.matiere.setText(module[1])
                self.semestre.setText(module[2])

                self.add_btn.setText("Modifier module")
                self.add_btn.clicked.disconnect()
                self.add_btn.clicked.connect(lambda: self.Applique_Modification(module_id))
            else:
                QMessageBox.critical(self, "Erreur", f"Aucun module trouvé avec l'id {module_id}!")
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")
        except Exception as e:
            print(f"Error: {e}")

    def Applique_Modification(self, module_id):
        ens_id = self.ens_id.text()
        matiere = self.matiere.text()
        semestre = self.semestre.text()

        if not ens_id or not matiere or not semestre:
            QMessageBox.warning(self, "Erreur", "Tous les champs doivent être remplis!")
            return

        try:
            conn = connect_db()
            curs = conn.cursor()
            curs.execute(""" UPDATE Module 
               SET Enseignant_id = ?, matiere = ?, semestre = ? 
               WHERE id = ?;""", (ens_id, matiere, semestre, module_id))
            conn.commit()
            conn.close()

            QMessageBox.information(self, "Succès", "Module modifié avec succès!")
            self.clear_inputs()
            self.Lister_Module()
            self.switch_ajout()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue: {e}")

    def switch_ajout(self):
        self.add_btn.setText("Ajouter Module")
        self.add_btn.clicked.disconnect()
        self.add_btn.clicked.connect(self.Ajouter_Module)


# Run the application
app = QApplication([])
window = Module()
window.show()
app.exec()
