class Contact:
    def __init__(self, nom, prenom, email, telephone):
        self._nom = nom
        self._prenom = prenom
        self._email = email
        self._telephone = telephone

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, value):
        self._nom = value

    @property
    def prenom(self):
        return self._prenom

    @prenom.setter
    def prenom(self, value):
        self._prenom = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    @property
    def telephone(self):
        return self._telephone

    @telephone.setter
    def telephone(self, value):
        self._telephone = value

    def __str__(self):
        return f"{self.nom}, {self.prenom}, {self.email}, {self.telephone}"
    
class GestionnaireContact:
    def __init__(self):
        self.contacts = []
        # Contact("Gueye", "Abdou","gueyeabd@gmail.com", "0945647")

    def ajouter_contact(self, contact):
        self.contacts.append(contact)
        print(f"Contact ajouté avec succès: {contact}")

    def afficher_contacts(self):
        if len(self.contacts) == 0:
            print("Aucun contact enregistré.")
        else:
            print('********************** Affichage contacts ************************* \n')
            for contact in range(len(self.contacts)):
                print(self.contacts[contact])

    def rechercher_contact(self, nom):
        resultats = [contact for contact in self.contacts if contact.nom.lower() == nom.lower()]
        return resultats

    def modifier_contact(self, nom, nouveau_contact):
        for index, contact in enumerate(self.contacts):
            if contact.nom.lower() == nom.lower():
                self.contacts[index] = nouveau_contact
                print("Contact modifié avec succès.")
                return
        print("Contact non trouvé.")

    def supprimer_contact(self, nom):
        for contact in self.contacts:
            if contact.nom.lower() == nom.lower():
                self.contacts.remove(contact)
                print("Contact supprimé avec succès.")
                return
        print("Contact non trouvé.")

    def sauvegarder_contacts(self, fichier):
        with open(fichier, "w") as f:
            for contact in self.contacts:
                f.write(f"{contact.nom},{contact.prenom},{contact.email},{contact.telephone}\n")
        print("Contacts sauvegardés avec succès.")

    def charger_contacts(self, fichier):
        try:
            with open(fichier, "r") as f:
                for ligne in f:
                    nom, prenom, email, telephone = ligne.strip().split(",")
                    self.contacts.append(Contact(nom, prenom, email, telephone))
            print("Contacts chargés avec succès.")
        except FileNotFoundError:
            print("Fichier non trouvé. Aucun contact chargé.")

class Main:
    @staticmethod
    def main():
        gestionnaire = GestionnaireContact()
        print(gestionnaire.contacts)
        fichier = "contacts.txt"
        # gestionnaire.charger_contacts(fichier)
       
        while True : 
            print("\nMenu :")
            print("1. Ajouter un contact")
            print("2. Afficher tous les contacts")
            print("3. Rechercher un contact")
            print("4. Modifier un contact")
            print("5. Supprimer un contact")
            print("6. Sauvegarder les contacts")
            print("7. Quitter")

            choix = input("Entrez votre choix : ")

            if choix == '1':
                nom = input("Nom : ")
                prenom = input("Prénom : ")
                email = input("Email : ")
                telephone = input("Téléphone : ")
                contact = Contact(nom, prenom, email, telephone)
                gestionnaire.ajouter_contact(contact)

            elif choix == '2':
                gestionnaire.afficher_contacts()

            elif choix == '3':
                nom = input("Nom à rechercher : ")
                resultats = gestionnaire.rechercher_contact(nom)
                if resultats:
                    for contact in resultats:
                        print(contact)
                else:
                    print("Aucun contact trouvé.")

            elif choix == '4':
                nom = input("Nom du contact à modifier : ")
                prenom = input("Nouveau prénom : ")
                email = input("Nouvel email : ")
                telephone = input("Nouveau téléphone : ")
                nouveau_contact = Contact(nom, prenom, email, telephone)
                gestionnaire.modifier_contact(nom, nouveau_contact)

            elif choix == '5':
                nom = input("Nom du contact à supprimer : ")
                gestionnaire.supprimer_contact(nom)

            elif choix == '6':
                gestionnaire.sauvegarder_contacts(fichier)

            elif choix == '7':
                gestionnaire.sauvegarder_contacts(fichier)
                print("Au revoir !")
                break                
            else:
                print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    Main.main()