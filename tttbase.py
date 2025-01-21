import tkinter as tk
from tkinter import messagebox


# Classe Contact
class Contact:
    def __init__(self, nom, prenom, email, telephone):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.telephone = telephone

    def __str__(self):
        return f"{self.nom}, {self.prenom}, {self.email}, {self.telephone}"


# Classe GestionnaireContact avec stockage local
class GestionnaireContact:
    def __init__(self):
        self.contacts = []

    def ajouter_contact(self, contact):
        self.contacts.append(contact)

    def afficher_contacts(self):
        return self.contacts

    def rechercher_contact(self, nom):
        return [contact for contact in self.contacts if contact.nom.lower() == nom.lower()]

    def modifier_contact(self, index, nouveau_contact):
        if 0 <= index < len(self.contacts):
            self.contacts[index] = nouveau_contact
            return True
        return False

    def supprimer_contact(self, index):
        if 0 <= index < len(self.contacts):
            del self.contacts[index]
            return True
        return False


# Interface graphique avec Tkinter
class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Contacts")

        self.gestionnaire = GestionnaireContact()

        # Widgets pour les champs de saisie
        tk.Label(root, text="Nom:").grid(row=0, column=0)
        self.nom_entry = tk.Entry(root)
        self.nom_entry.grid(row=0, column=1)

        tk.Label(root, text="Prénom:").grid(row=1, column=0)
        self.prenom_entry = tk.Entry(root)
        self.prenom_entry.grid(row=1, column=1)

        tk.Label(root, text="Email:").grid(row=2, column=0)
        self.email_entry = tk.Entry(root)
        self.email_entry.grid(row=2, column=1)

        tk.Label(root, text="Téléphone:").grid(row=3, column=0)
        self.telephone_entry = tk.Entry(root)
        self.telephone_entry.grid(row=3, column=1)

        # Boutons d'actions
        tk.Button(root, text="Ajouter", command=self.ajouter_contact).grid(row=4, column=0)
        tk.Button(root, text="Afficher", command=self.afficher_contacts).grid(row=4, column=1)
        tk.Button(root, text="Rechercher", command=self.rechercher_contact).grid(row=5, column=0)
        tk.Button(root, text="Modifier", command=self.modifier_contact).grid(row=5, column=1)
        tk.Button(root, text="Supprimer", command=self.supprimer_contact).grid(row=6, column=0)

        # Liste pour afficher les contacts
        self.contacts_listbox = tk.Listbox(root, width=50, height=15)
        self.contacts_listbox.grid(row=7, column=0, columnspan=2)

    def ajouter_contact(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        email = self.email_entry.get()
        telephone = self.telephone_entry.get()

        if nom and prenom and email and telephone:
            contact = Contact(nom, prenom, email, telephone)
            self.gestionnaire.ajouter_contact(contact)
            messagebox.showinfo("Succès", "Contact ajouté avec succès !")
            self.afficher_contacts()
        else:
            messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")

    def afficher_contacts(self):
        self.contacts_listbox.delete(0, tk.END)
        contacts = self.gestionnaire.afficher_contacts()
        for index, contact in enumerate(contacts):
            self.contacts_listbox.insert(tk.END, f"{index}: {contact}")

    def rechercher_contact(self):
        nom = self.nom_entry.get()
        if nom:
            contacts = self.gestionnaire.rechercher_contact(nom)
            self.contacts_listbox.delete(0, tk.END)
            for index, contact in enumerate(contacts):
                self.contacts_listbox.insert(tk.END, f"{index}: {contact}")
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un nom à rechercher.")

    def modifier_contact(self):
        try:
            selection = self.contacts_listbox.curselection()
            if selection:
                index = int(self.contacts_listbox.get(selection[0]).split(":")[0])
                nom = self.nom_entry.get()
                prenom = self.prenom_entry.get()
                email = self.email_entry.get()
                telephone = self.telephone_entry.get()

                if nom and prenom and email and telephone:
                    nouveau_contact = Contact(nom, prenom, email, telephone)
                    if self.gestionnaire.modifier_contact(index, nouveau_contact):
                        messagebox.showinfo("Succès", "Contact modifié avec succès !")
                        self.afficher_contacts()
                else:
                    messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            else:
                messagebox.showwarning("Erreur", "Veuillez sélectionner un contact à modifier.")
        except IndexError:
            messagebox.showwarning("Erreur", "Aucune sélection valide.")

    def supprimer_contact(self):
        try:
            selection = self.contacts_listbox.curselection()
            if selection:
                index = int(self.contacts_listbox.get(selection[0]).split(":")[0])
                if self.gestionnaire.supprimer_contact(index):
                    messagebox.showinfo("Succès", "Contact supprimé avec succès !")
                    self.afficher_contacts()
            else:
                messagebox.showwarning("Erreur", "Veuillez sélectionner un contact à supprimer.")
        except IndexError:
            messagebox.showwarning("Erreur", "Aucune sélection valide.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
