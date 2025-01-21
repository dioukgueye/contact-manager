import pyodbc
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

# Classe GestionnaireContact (liaison avec SQL Server)
class GestionnaireContact:
    def __init__(self, server="localhost\\SQLEXPRESS", database="ContactsDB"):
        try:
            # Connexion à SQL Server via pyodbc
            self.conn = pyodbc.connect(
                f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"
            )
            self.cur = self.conn.cursor()
            self.creer_table()
        except Exception as e:
            print(f"Erreur de connexion à SQL Server : {e}")

    def creer_table(self):
        """Créer la table 'contacts' si elle n'existe pas."""
        self.cur.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='contacts' AND xtype='U')
            CREATE TABLE contacts (
                id INT PRIMARY KEY IDENTITY(1,1),
                nom VARCHAR(100),
                prenom VARCHAR(100),
                email VARCHAR(100),
                telephone VARCHAR(15)
            )
        ''')
        self.conn.commit()

    def ajouter_contact(self, contact):
        """Ajouter un contact à la base de données."""
        try:
            self.cur.execute(
                "INSERT INTO contacts (nom, prenom, email, telephone) VALUES (?, ?, ?, ?)",
                (contact.nom, contact.prenom, contact.email, contact.telephone)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de l'ajout d'un contact : {e}")

    def afficher_contacts(self):
        """Récupérer tous les contacts."""
        try:
            self.cur.execute("SELECT * FROM contacts")
            return self.cur.fetchall()
        except Exception as e:
            print(f"Erreur lors de la récupération des contacts : {e}")
            return []

    def rechercher_contact(self, nom):
        """Rechercher un contact par nom."""
        try:
            self.cur.execute("SELECT * FROM contacts WHERE nom = ?", (nom,))
            return self.cur.fetchall()
        except Exception as e:
            print(f"Erreur lors de la recherche : {e}")
            return []

    def modifier_contact(self, contact_id, nouveau_contact):
        """Modifier un contact existant."""
        try:
            self.cur.execute(
                """
                UPDATE contacts
                SET nom = ?, prenom = ?, email = ?, telephone = ?
                WHERE id = ?
                """,
                (nouveau_contact.nom, nouveau_contact.prenom, nouveau_contact.email, nouveau_contact.telephone, contact_id)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de la modification d'un contact : {e}")

    def supprimer_contact(self, contact_id):
        """Supprimer un contact par ID."""
        try:
            self.cur.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Erreur lors de la suppression : {e}")

    def __del__(self):
        """Fermer la connexion à la base de données."""
        if self.conn:
            self.conn.close()

# Classe de l'interface Tkinter
class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de Contacts")

        # Initialisation du gestionnaire avec connexion à SQL Server
        self.gestionnaire = GestionnaireContact(server="localhost", database="ContactsDB")

        # Champs de saisie
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

        # Boutons
        tk.Button(root, text="Ajouter", command=self.ajouter_contact).grid(row=4, column=0)
        tk.Button(root, text="Afficher", command=self.afficher_contacts).grid(row=4, column=1)
        tk.Button(root, text="Rechercher", command=self.rechercher_contact).grid(row=5, column=0)
        tk.Button(root, text="Modifier", command=self.modifier_contact).grid(row=5, column=1)
        tk.Button(root, text="Supprimer", command=self.supprimer_contact).grid(row=6, column=0)

        # Liste des contacts
        self.contacts_listbox = tk.Listbox(root, width=50, height=15)
        self.contacts_listbox.grid(row=7, column=0, columnspan=2)

    def ajouter_contact(self):
        """Ajouter un contact à la base de données."""
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
        """Afficher tous les contacts dans la liste."""
        self.contacts_listbox.delete(0, tk.END)
        contacts = self.gestionnaire.afficher_contacts()
        for contact in contacts:
            self.contacts_listbox.insert(tk.END, f"{contact[0]}: {contact[1]} {contact[2]}, {contact[3]}, {contact[4]}")

    def rechercher_contact(self):
        """Rechercher un contact par nom."""
        nom = self.nom_entry.get()
        if nom:
            contacts = self.gestionnaire.rechercher_contact(nom)
            self.contacts_listbox.delete(0, tk.END)
            for contact in contacts:
                self.contacts_listbox.insert(tk.END, f"{contact[0]}: {contact[1]} {contact[2]}, {contact[3]}, {contact[4]}")
        else:
            messagebox.showwarning("Erreur", "Veuillez entrer un nom à rechercher.")

    def modifier_contact(self):
        """Modifier un contact sélectionné."""
        try:
            selection = self.contacts_listbox.curselection()
            if selection:
                contact_id = int(self.contacts_listbox.get(selection[0]).split(":")[0])
                nom = self.nom_entry.get()
                prenom = self.prenom_entry.get()
                email = self.email_entry.get()
                telephone = self.telephone_entry.get()

                if nom and prenom and email and telephone:
                    nouveau_contact = Contact(nom, prenom, email, telephone)
                    self.gestionnaire.modifier_contact(contact_id, nouveau_contact)
                    messagebox.showinfo("Succès", "Contact modifié avec succès !")
                    self.afficher_contacts()
                else:
                    messagebox.showwarning("Erreur", "Veuillez remplir tous les champs.")
            else:
                messagebox.showwarning("Erreur", "Veuillez sélectionner un contact à modifier.")
        except IndexError:
            messagebox.showwarning("Erreur", "Aucune sélection valide.")

    def supprimer_contact(self):
        """Supprimer un contact sélectionné."""
        try:
            selection = self.contacts_listbox.curselection()
            if selection:
                contact_id = int(self.contacts_listbox.get(selection[0]).split(":")[0])
                self.gestionnaire.supprimer_contact(contact_id)
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
