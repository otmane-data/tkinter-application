from tkinter import *
from tkinter import ttk, messagebox
import pymysql
from PIL import ImageTk, Image
import login
class FIT:
    def __init__(self, root):
        self.user = login.user
        self.root = root
        self.root.title("Connexion")
        self.root.geometry("700x550")
        self.bg_image = Image.open(r"C:\Users\DELL 5410\Documents\fit.png")
        self.bg_image = self.bg_image.resize((750, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Set the background image as the window background
        self.background_label = Label(self.root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.focus_force()


        login_frame = Frame(self.root, bg="#1a4f76")
        login_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=450)  # Adjust width of the login_frame

        # Store email for later use


        poids_label = Label(login_frame, text="Poids:", font=("Arial", 14), bg="#1a4f76", fg="black")
        poids_label.grid(row=1, column=0, padx=10, pady=10)
        self.poids_entry = Entry(login_frame, font=("Arial", 12), bg="#d3d3d3")
        self.poids_entry.grid(row=1, column=1, padx=10, pady=10)

        taille_label = Label(login_frame, text="Taille:", font=("Arial", 14), bg="#1a4f76", fg="black")
        taille_label.grid(row=2, column=0, padx=10, pady=10)
        self.taille_entry = Entry(login_frame, font=("Arial", 12), bg="#d3d3d3")
        self.taille_entry.grid(row=2, column=1, padx=10, pady=10)

        goal_label = Label(login_frame, text="Objectif:", font=("Arial", 14), bg="#1a4f76", fg="black")
        goal_label.grid(row=3, column=0, padx=10, pady=10)
        self.goal_entry = Entry(login_frame, font=("Arial", 12), bg="#d3d3d3")
        self.goal_entry.grid(row=3, column=1, padx=10, pady=10)

        # Buttons for Suivi de santé, Suivi de physique, and Enregistrer
        suivisante_button = Button(login_frame, text="Enregistrer", command=self.save_infos, font=("Arial", 12), bg="cyan", fg="black")
        suivisante_button.grid(row=4, column=0, pady=20)
        suiviphysique_button = Button(login_frame, text="Suivi de physique",command=self.fenetre_physic, font=("Arial", 12), bg="cyan", fg="black")
        suiviphysique_button.grid(row=4, column=1, pady=20)
        enregistrer_button = Button(login_frame, text="Suivi de santé",command=self.fenetre_sante, font=("Arial", 12), bg="cyan", fg="black")
        enregistrer_button.grid(row=4, column=3, pady=20)

    def save_infos(self):
        poids = float(self.poids_entry.get())
        taille = float(self.taille_entry.get())
        goal = float(self.goal_entry.get())
        imc = poids / (taille * 10 ** -2) ** 2
        id = self.user[0]
        conditions =""
        if imc < 18.5:
            conditions += "Vous êtes en insuffisance pondérale."
        elif 18.5 <= imc < 24.9:
            conditions += "Votre poids est normal."
        elif 25 <= imc < 29.9:
            conditions += "Vous êtes en surpoids."
        else:
            conditions += "Vous êtes obèse."
        if poids and taille and goal:
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="ensah")
                cur = con.cursor()
                cur.execute("SELECT * FROM info WHERE id=%s",id)
                row = cur.fetchone()

                if row is not None:

                    cur.execute("INSERT INTO fitness (id,poids, taille, goal, imc, interpretation) VALUES (%s, %s, %s, %s, %s, %s)",(id,poids, taille, goal,imc,conditions))
                con.commit()
                messagebox.showinfo("Succès", "Informations de suivi de santé enregistrées avec succès")

            finally:
                con.close()
        else:
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
    def fenetre_physic(self):
        self.root.destroy()
        import Physic




    '''def display_info_by_id(self):
        id = self.user[0]
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="ensah")
            with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM info WHERE id=%s", id)
                row = cur.fetchone()
                if row is not None:
                    messagebox.showinfo("Informations", f"Informations pour l'ID {id}:\n"
                                                        f"ID: {row[0]}\n"
                                                        f"Poids: {row[1]}\n"
                                                        f"Taille: {row[2]}\n"
                                                        f"Objectif: {row[3]}\n"
                                                        f"IMC: {row[4]}\n"
                                                        f"Interprétation de l'IMC: {row[5]}")
                else:
                    messagebox.showerror("Erreur", "Cet ID n'existe pas")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la récupération des informations : {str(e)}")'''
    def fenetre_sante(self):
        self.root.destroy()
        import Sante





root = Tk()
obj=FIT(root)
root.mainloop()
