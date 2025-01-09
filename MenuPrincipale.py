from lxml import etree

class Switch:
    value = None
    def __new__(class_, value):
        class_.value = value
        return value
def case(*args):
    return any((arg == Switch.value) for arg in args)

"""
#########################################################
##################### Inscription #######################
#########################################################
"""
class Inscrire:
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.tree = None
        self.root = None

    def load_xml(self):
        try:
            self.tree = etree.parse(self.filepath)
            self.root = self.tree.getroot()
        except FileNotFoundError:
            print(f"Erreur: Fichier '{self.filepath}' n'est pas trouvé.")
            return False
        return True

    def __call__(self, *args, **kwargs):
        self.load_xml()
        while True:
            print("Espace Inscription : Liste des choix".center(73, "-"))
            print("1: Inscrire un étudiant à un module")
            print("2: Modifier la note d'un étudiant")
            print("3: Supprimer une inscription")
            print("4: Lister les inscriptions")
            print("0: Quitter")
            choix = input("Entrer votre choix : ")
            c = int(choix)

            switch = Switch(c)

            if case(1):
                print("Choix 1: Inscrire un étudiant à un module")
                module_id = input("Entrez l'id du module : ")
                etu_apo = input("Entrez l'apogee d'étudiant : ")
                self.inscrire_etudiant(module_id, etu_apo)
            elif case(2):
                print("Choix 2: Modifier la note d'un étudiant")
                module_id = input("Entrez l'id du module : ")
                etu_apo = input("Entrez l'apogee d'étudiant : ")
                self.modifier_note(module_id, etu_apo)
            elif case(3):
                print("Choix 3: Supprimer une inscription")
                module_id = input("Entrez l'id du module : ")
                etu_apo = input("Entrez l'apogee d'étudiant : ")
                self.supprimer_inscription(module_id, etu_apo)
            elif case(4):
                print("Choix 4: Lister les inscriptions")
                self.lister_inscription()
            elif case(0):
                print("Au revoir!")
                break
            else:
                print("Choix invalide, veuillez réessayer!")

    def inscrire_etudiant(self, module_id, etu_apo):
        insc = self.root.find("Inscrire")
        if insc is None:
            insc = etree.SubElement(self.root, "Inscrire")
        if self.root.find(f".//Module[@id='{module_id}']") is not None and self.root.find(f".//Etudiant[@num_apogee='{etu_apo}']") is not None:
            note = input("Entrez la note de l'étudiant : ")
            valide = input("Validation (V:validé / NV:non valide / AS:componsé) : ")
            inscription = etree.Element("Inscription")
            inscription.set("module-id", module_id)
            inscription.set("etudiant-apogee", etu_apo)
            etree.SubElement(inscription, "note").text = note
            etree.SubElement(inscription, "valide").text = valide
            insc.append(inscription)
            self.tree.write(self.filepath, encoding='UTF-8', xml_declaration=True)
            print("Inscription réussie!")
        else:
            print("Le numéro d'apogee ou l'id de module est incorrect!")

    def modifier_note(self, module_id, etu_apo):
        for ins in self.root.findall("Inscrire/Inscription"):
            if ins.get("module-id") == module_id and ins.get("etudiant-apogee") == etu_apo:
                note = input("Entrez la nouvelle note de l'étudiant : ") or ins.find("note").text
                ins.find("note").text = note
                if int(note) < 10:
                    ins.find("valide").text = "NV"
                else:
                    ins.find("valide").text = "V"
                self.tree.write(self.filepath, encoding='UTF-8', xml_declaration=True)
                print("Note modifiée avec succès!")
                return
        print("Le numéro d'apogee ou l'id de module est incorrect!")

    def supprimer_inscription(self, module_id, etu_apo):
        for ins in self.root.findall("Inscrire/Inscription"):
            if ins.get("module-id") == module_id and ins.get("etudiant-apogee") == etu_apo:
                self.root.find("Inscrire").remove(ins)
                self.tree.write(self.filepath, encoding='UTF-8', xml_declaration=True)
                print("Inscription supprimée avec succès!")
                return
        print("Le numéro d'apogee ou l'id de module est incorrect!")

    def lister_inscription(self):
        inscriptions = self.root.findall("Inscrire/Inscription")
        if not inscriptions:
            print("Aucune inscription trouvée.")
            return
        print("Liste des inscriptions :")
        print(f"{'Module ID':<10} {'Étudiant Apogée':<15} {'Note':<6} {'Valide':<10}")
        print("-" * 40)
        for ins in inscriptions:
            print(f"{ins.get('module-id'):<10} {ins.get('etudiant-apogee'):<15} {ins.find('note').text:<6} {ins.find('valide').text:<10}")
        print("-" * 40)

"""
#########################################################
###################### Etudiant #########################
#########################################################
"""
class Etudiant:

    def __init__(self, filepath):
        self.filepath = filepath
        try:
            self.tree = etree.parse(filepath)
            self.root = self.tree.getroot()
        except (FileNotFoundError, OSError):
            print(f"Erreur: Le fichier '{filepath}' n'est pas trouvé. Création d'un nouveau fichier.")
            self.root = etree.Element("Scolarite")
            etudiants = etree.SubElement(self.root, "Etudiants")
            self.tree = etree.ElementTree(self.root)
            self.tree.write(filepath, encoding='UTF-8', xml_declaration=True, doctype='<!DOCTYPE Scolarite SYSTEM "./scolarite.dtd">')

    def load_xml(self):
        try:
            self.tree = etree.parse(self.filepath)
            self.root = self.tree.getroot()
        except FileNotFoundError:
            print(f"Erreur: Fichier '{self.filepath}' n'est pas trouvé.")
            return False
        return True
    
    def __call__(self):
        self.load_xml()
        while True:
            print("Espace Étudiant : Liste des choix".center(73, "-"))
            print("1: Ajouter un étudiant")
            print("2: Modifier un étudiant")
            print("3: Supprimer un étudiant")
            print("4: Lister l'ensemble des étudiants")
            print("0: Quitter")
            choix = input("Entrer votre choix : ")
            try:
                c = int(choix)
            except ValueError:
                print("Choix invalide, veuillez entrer un chiffre!")
                continue

            if c == 1:
                self.ajouter_etudiant()
            elif c == 2:
                num_apogee = input("Entrez le numéro Apogée de l'étudiant : ")
                self.modifier_etudiant(num_apogee)
            elif c == 3:
                num_apogee = input("Entrez le numéro Apogée de l'étudiant : ")
                self.supprimer_etudiant(num_apogee)
            elif c == 4:
                self.lister_etudiants()
            elif c == 0:
                print("Au revoir!")
                break
            else:
                print("Choix invalide, veuillez réessayer!")
    
    def ajouter_etudiant(self):
        num_apogee = input("Entrez le numéro Apogée : ")

        # Check if student with the same num_apogee already exists in the current file
        if self.root.find(f".//Etudiant[@num_apogee='{num_apogee}']") is not None:
            print(f"Erreur: Un étudiant avec le numéro Apogée {num_apogee} existe déjà.")
            return

        nom = input("Entrez le nom de l'étudiant : ")
        prenom = input("Entrez le prénom de l'étudiant : ")
        cin = input("Entrez le CIN de l'étudiant : ")
        date_naiss = input("Entrez la date de naissance de l'étudiant (AAAA-MM-JJ) : ")

        # Add the new student
        etudiants = self.root.find("Etudiants")
        etud = etree.SubElement(etudiants, "Etudiant", num_apogee=num_apogee)
        nom_complet = etree.SubElement(etud, "nom-complet", nom=nom, prenom=prenom)
        cin_element = etree.SubElement(etud, "cin")
        cin_element.text = cin
        date_naiss_element = etree.SubElement(etud, "date-naiss")
        date_naiss_element.text = date_naiss

        self.tree.write(self.filepath, encoding='UTF-8', xml_declaration=True)
        print("Étudiant ajouté avec succès!")


    def modifier_etudiant(self, num_apogee):
        etud = self.root.find(f".//Etudiant[@num_apogee='{num_apogee}']")
        if etud is not None:
            print(f"Modification de l'étudiant avec le numéro Apogée {num_apogee}:")
            nom = input(f"Nom actuel ({etud.find('nom-complet').get('nom')}): ") or etud.find('nom-complet').get('nom')
            prenom = input(f"Prénom actuel ({etud.find('nom-complet').get('prenom')}): ") or etud.find('nom-complet').get('prenom')
            cin = input(f"CIN actuel ({etud.find('cin').text}): ") or etud.find('cin').text
            date_naiss = input(f"Date de naissance actuelle ({etud.find('date-naiss').text}): ") or etud.find('date-naiss').text

            etud.find('nom-complet').set('nom', nom)
            etud.find('nom-complet').set('prenom', prenom)
            etud.find('cin').text = cin
            etud.find('date-naiss').text = date_naiss

            self.tree.write(self.filepath, encoding='UTF-8', xml_declaration=True)
            print("Étudiant modifié avec succès!")
        else:
            print("Aucun étudiant trouvé avec ce numéro Apogée!")

    def supprimer_etudiant(self, num_apogee):
        etud = self.root.find(f".//Etudiant[@num_apogee='{num_apogee}']")
        if etud is not None:
            etud.getparent().remove(etud)
            print(f"Étudiant avec le numéro Apogée {num_apogee} supprimé!")
            self.tree.write(self.filepath, encoding='UTF-8', xml_declaration=True)
        else:
            print("Aucun étudiant trouvé avec ce numéro Apogée!")

    def lister_etudiants(self):
        etudiants = self.root.findall(".//Etudiant")
        if not etudiants:
            print("Aucun étudiant trouvé dans la base de données.")
            return

        print("La liste des étudiants :")
        print(f"{'Num Apogée':<12} {'Nom':<15} {'Prénom':<15} {'CIN':<10} {'Date de Naissance':<15}")
        print("-" * 73)
        for etud in etudiants:
            print(f"{etud.get('num_apogee'):<12} {etud.find('nom-complet').get('nom'):<15} {etud.find('nom-complet').get('prenom'):<15} {etud.find('cin').text:<10} {etud.find('date-naiss').text:<15}")
        print("-" * 73)

"""
#########################################################
##################### Enseignant ########################
#########################################################
"""
class Enseignant:

    def __init__(self, filepath):
        self.filepath = filepath
        self.tree = None
        self.root = None

    def load_xml(self):
        try:
            self.tree = etree.parse(self.filepath)
            self.root = self.tree.getroot()
        except FileNotFoundError:
            print(f"Erreur: Fichier '{self.filepath}' n'est pas trouvé.")
            return False
        return True

    def __call__(self, *args, **kwargs):
        self.load_xml()
        while True:

            print("Espace Enseignant : Liste des choix".center(73, "-"))
            print("1: Ajouter un enseignant")
            print("2: Modifier un enseignant")
            print("3: Supprimer un enseignant")
            print("4: Lister l'ensemble des enseignants")
            print("0: Quitter")
            choix = input("Entrer votre choix : ")
            c = int(choix)

            switch = Switch(c)

            if case(1):
                print("Choix 1: Ajouter un enseignant")
                id = input("Entrez l'id de l'enseignant : ")
                nom = input("Entrez le nom de l'enseignant : ")
                prenom = input("Entrez le prénom de l'enseignant : ")
                cin = input("Entrez le cin de l'enseignant : ")
                dept = input("Entrez le departement de l'enseignant : ")
                self.ajouter_enseignant(id, nom, prenom, cin, dept)
            elif case(2):
                print("Choix 2: Modifier un enseignant")
                ens_id = input("Entrez l'id de l'enseignant : ")
                self.modifier_enseignant(ens_id)
            elif case(3):
                print("Choix 3: Supprimer un enseignant")
                ens_id = input("Entrez l'id de l'enseignant : ")
                self.supprimer_enseignant(ens_id)
            elif case(4):
                print("Choix 4: Lister les enseignants")
                self.lister_enseignants()
            elif case(0):
                print("Au revoir!")
                break
            else:
                print("Choix invalide, veuillez réessayer!")
                
    def exist(self, id):
        enseignants = self.root.findall("Enseignants/Enseignant")
        for ens in enseignants:
            if id == ens.get("id"):
                return True
        return False

    def ajouter_enseignant(self, id, nom, prenom, cin, dept):
        if not self.exist(id):
            enseignants = self.root.find("Enseignants")
            if enseignants is None:
                enseignants = etree.SubElement(self.root, "Enseignants")

        if not self.exist(id):
            ensg = etree.Element("Enseignant", id=id)
            nom_complet = etree.SubElement(ensg, "nom-complet", nom=nom, prenom=prenom)
            cin_element = etree.SubElement(ensg, "cin")
            cin_element.text = cin
            departement = etree.SubElement(ensg, "departement")
            departement.text = dept
            enseignants.append(ensg)
            self.tree.write(self.filepath, encoding='UTF-8', xml_declaration=True)
            print("Enseignant ajouté avec succès!")
        else :
            print("Il existe déjà un enseignant avec cet id.")
    
    def modifier_enseignant(self, id):
        for ens in self.root.findall("Enseignants/Enseignant"):
            if ens.get("id") == id:
                print(f"Modification de l'enseignant avec l'id {id}:")
                nom = input(f"Nom actuel ({ens.find('nom-complet').get('nom')}): ") or ens.find('nom-complet').get('nom')
                prenom = input(f"Prénom actuel ({ens.find('nom-complet').get('prenom')}): ") or ens.find('nom-complet').get('prenom')
                cin = input(f"CIN actuel ({ens.find('cin').text}): ") or ens.find('cin').text
                dept = input(f"Département actuel ({ens.find('departement').text}): ") or ens.find('departement').text

                ens.find('nom-complet').set('nom', nom)
                ens.find('nom-complet').set('prenom', prenom)
                ens.find('cin').text = cin
                ens.find('departement').text = dept

                self.tree.write(self.filepath, encoding='UTF-8', xml_declaration=True)
                print("Enseignant modifié avec succès!")
                return
        print("L'id de l'enseignant entré est incorrect!")

    def supprimer_enseignant(self, id):
        for ens in self.root.findall("Enseignants/Enseignant"):
            if ens.get("id") == id:
                self.root.find("Enseignants").remove(ens)
                print(f"Enseignant avec l'id {id} supprimé!")
                break
        else:
            print("Aucun enseignant trouvé avec cet id.")

        self.tree.write(self.filepath, encoding='UTF-8', xml_declaration=True)

        self.tree.write(self.filepath, encoding='UTF-8', xml_declaration=True)

    def lister_enseignants(self):
        enseignants = self.root.findall("Enseignants/Enseignant")
        if not enseignants:
            print("Aucun enseignant trouvé dans la base de données.")
            return

        print("La liste des enseignants :")
        print(f"{'ID':<6} {'Nom':<15} {'Prénom':<15} {'CIN':<10} {'Département':<20}")
        print("-" * 73)
        for ens in enseignants:
            print(f"{ens.get('id'):<6} {ens.find('nom-complet').get('nom'):<15} {ens.find('nom-complet').get('prenom'):<15} {ens.find('cin').text:<10} {ens.find('departement').text:<20}")
        print("-" * 73)

"""
#########################################################
######################## Module #########################
#########################################################
"""
class Module:

    def __init__(self, filepath):
        self.filepath = filepath
        try:
            self.tree = etree.parse(filepath)
            self.root = self.tree.getroot()
        except (FileNotFoundError, OSError):
            print(f"Erreur: Le fichier '{filepath}' n'est pas trouvé. Création d'un nouveau fichier.")
            self.root = etree.Element("Scolarite")
            modules = etree.SubElement(self.root, "Modules")
            self.tree = etree.ElementTree(self.root)
            self.tree.write(filepath, encoding='UTF-8', xml_declaration=True, doctype='<!DOCTYPE Scolarite SYSTEM "./scolarite.dtd">')

    def load_xml(self):
        try:
            self.tree = etree.parse(self.filepath)
            self.root = self.tree.getroot()
        except FileNotFoundError:
            print(f"Erreur: Fichier '{self.filepath}' n'est pas trouvé.")
            return False
        return True
    
    def __call__(self):
        self.load_xml()
        while True:
            print("Espace Module : Liste des choix".center(73, "-"))
            print("1: Ajouter un module")
            print("2: Modifier un module")
            print("3: Supprimer un module")
            print("4: Lister l'ensemble des modules")
            print("0: Quitter")
            choix = input("Entrer votre choix : ")
            try:
                c = int(choix)
            except ValueError:
                print("Choix invalide, veuillez entrer un chiffre!")
                continue

            if c == 1:
                self.ajouter_module()
            elif c == 2:
                id = input("Entrez l'id du module : ")
                self.modifier_module(id)
            elif c == 3:
                id = input("Entrez l'id du module : ")
                self.supprimer_module(id)
            elif c == 4:
                self.lister_modules()
            elif c == 0:
                print("Au revoir!")
                break
            else:
                print("Choix invalide, veuillez réessayer!")

    def ajouter_module(self):
        id = input("Entrez l'id du module : ")

        # Check if module with the same id already exists in the current file
        if self.root.find(f".//Module[@id='{id}']") is not None:
            print(f"Erreur: Un module avec l'id {id} existe déjà.")
            return

        matiere = input("Entrez la matière du module : ")
        semestre = input("Entrez le semestre du module : ")
        enseignant_id = input("Entrez l'id de l'enseignant responsable : ")

        # Check if enseignant-id exists in the same file
        if self.root.find(f".//Enseignant[@id='{enseignant_id}']") is None:
            print(f"Erreur: Aucun enseignant trouvé avec l'id {enseignant_id}.")
            return

        # Add the new module
        modules = self.root.find("Modules")
        module = etree.SubElement(modules, "Module", id=id)
        matiere_elem = etree.SubElement(module, "matiere")
        matiere_elem.text = matiere
        semestre_elem = etree.SubElement(module, "semestre")
        semestre_elem.text = semestre
        module.set("enseignant-id", enseignant_id)

        self.tree.write(self.filepath, encoding='UTF-8', xml_declaration=True)
        print("Module ajouté avec succès!")

    def modifier_module(self, id):
        module = self.root.find(f".//Module[@id='{id}']")
        if module is not None:
            print(f"Modification du module avec l'id {id}:")
            matiere = input(f"Matière actuelle ({module.find('matiere').text}): ") or module.find('matiere').text
            semestre = input(f"Semestre actuel ({module.find('semestre').text}): ") or module.find('semestre').text
            enseignant_id = input(f"ID enseignant actuel ({module.get('enseignant-id')}): ") or module.get('enseignant-id')

            module.find('matiere').text = matiere
            module.find('semestre').text = semestre
            module.set('enseignant-id', enseignant_id)

            self.tree.write(self.filepath, encoding='UTF-8', xml_declaration=True)
            print("Module modifié avec succès!")
        else:
            print("Aucun module trouvé avec ce id!")

    def supprimer_module(self, id):
        module = self.root.find(f".//Module[@id='{id}']")
        if module is not None:
            module.getparent().remove(module)
            print(f"Module avec l'id {id} supprimé!")
            self.tree.write(self.filepath, encoding='UTF-8', xml_declaration=True)
        else:
            print("Aucun module trouvé avec ce id!")

    def lister_modules(self):
        modules = self.root.findall(".//Module")
        if not modules:
            print("Aucun module trouvé dans la base de données.")
            return

        print("La liste des modules :")
        print(f"{'ID':<6} {'Matière':<20} {'Semestre':<10} {'ID Enseignant':<15}")
        print("-" * 73)
        for module in modules:
            print(f"{module.get('id'):<6} {module.find('matiere').text:<20} {module.find('semestre').text:<10} {module.get('enseignant-id'):<15}")
        print("-" * 73)

"""
#########################################################
######################### Menu ##########################
#########################################################
"""

def menu_principal():
    
    filepath = "scolarite.xml"
    while True:
        print("Espace Scolarité : Liste des choix".center(50, "-"))
        print("1: Espace étudiant")
        print("2: Espace enseignant")
        print("3: Espace module")
        print("4: Espace inscription")
        print("0: Quitter")
        
        choix = input("Entrer votre choix : ")
        try:
            c = int(choix)
        except ValueError:
            print("Choix invalide, veuillez entrer un chiffre!")
            continue
        
        if c == 1:
            etudiant = Etudiant(filepath)
            etudiant()
        elif c == 2:
            enseignant = Enseignant(filepath)
            enseignant()
        elif c == 3:
            module = Module(filepath)
            module()
        elif c == 4:
            inscrire = Inscrire(filepath)
            inscrire()
        elif c == 0:
            print("Au revoir!")
            break
        else:
            print("Choix invalide, veuillez réessayer!")

menu_principal()