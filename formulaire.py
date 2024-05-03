from tkinter import *
from tkinter import ttk, messagebox
import pymysql
from PIL import ImageTk, Image
import re
import hashlib

class Formulaire:
    def __init__(self, root):
        self.root = root

        self.root.title("Application de suivi d'activité physique et de santé")
        self.root.geometry("750x600")
        self.bg_image = Image.open(r"C:\Users\DELL 5410\Documents\fit.png")
        self.bg_image = self.bg_image.resize((750, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Set the background image as the window background
        self.background_label = Label(self.root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # First Name

        # Entry for first name
        info_frame = Frame(root, bg="#1a4f76")
        info_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Title
        title = Label(info_frame, text="Créer un compte", font="Calibre 20 bold",
                      fg="orange",bg="#1a4f76")
        title.grid(row=0, column=0, columnspan=5, pady=25)

        # First name and last name
        fname = Label(info_frame, text="Prenom", font="Calibre 10 bold",bg="#1a4f76")
        fname.grid(row=1, column=0, pady=10, padx=10)
        self.fname_entry = Entry(info_frame, width=20, bg="#d3d3d3")
        self.fname_entry.grid(row=1, column=1, pady=10)
        lname = Label(info_frame, text="Nom", font="Calibre 10 bold",bg="#1a4f76")
        lname.grid(row=1, column=2, pady=10, padx=10)
        self.lname_entry = Entry(info_frame, width=20, bg="#d3d3d3")
        self.lname_entry.grid(row=1, column=3, pady=10)

        # Age
        age_label = Label(info_frame, text="Age", font="Calibre 10 bold",bg="#1a4f76")
        age_label.grid(row=2, column=0, pady=10, padx=10)
        self.age_entry = Entry(info_frame, width=20, bg="#d3d3d3")
        self.age_entry.grid(row=2, column=1, pady=10)

        # Gender
        gender_label = Label(info_frame, text="Gender", font="Calibre 25 bold",bg="#1a4f76")
        gender_label.grid(row=2, column=2, pady=10, padx=10)
        gender_label.config(fg="black", font=("Calibre", 10, "bold"))  # Apply font and color configurations correctly
        self.gender = StringVar()
        self.gender.set("none")
        male = Radiobutton(info_frame, text="Male", variable=self.gender, value="Male",bg="#1a4f76")
        male.grid(row=2, column=3, pady=15, sticky="w")
        Femele = Radiobutton(info_frame, text="Femele", variable=self.gender, value="Femele",bg="#1a4f76")
        Femele.grid(row=2, column=4, pady=15, sticky="w")

        # Email
        email_label = Label(info_frame, text="Email", font="Calibre 10 bold",bg="#1a4f76")
        email_label.grid(row=3, column=0, pady=10, padx=10)
        self.email_entry = Entry(info_frame, width=20, bg="#d3d3d3")
        self.email_entry.grid(row=3, column=1, columnspan=3, sticky="we", padx=10)

        # Password & confirm password
        aff_password = Label(info_frame, text="Mot de passe", font="Calibre 10 bold",bg="#1a4f76")
        aff_password.grid(row=4, column=0, pady=10, padx=10)
        self.ecri_password = Entry(info_frame, show="*", width=20, bg="#d3d3d3")
        self.ecri_password.grid(row=4, column=1, pady=10)
        conf_password = Label(info_frame, text="Confirmer mot de passe", font="Calibre 10 bold",bg="#1a4f76")
        conf_password.grid(row=4, column=2, pady=10, padx=10)
        self.ecri_cnfpassword = Entry(info_frame, show="*", width=20, bg="#d3d3d3")
        self.ecri_cnfpassword.grid(row=4, column=3, pady=10)

        # Terms and conditions
        self.var = IntVar()
        chk = Checkbutton(info_frame, variable=self.var, onvalue=1, offvalue=0,
                          text="J'accepte les conditions et les termes", font="Calibre 12 bold", fg="red",bg="#1a4f76")
        chk.grid(row=5, column=0, columnspan=5, pady=10, padx=10)

        # Save and next
        enregistrer = Button(info_frame, text="Creer",command=self.creer)
        enregistrer.grid(row=6, column=3, pady=15, padx=10, sticky="e")
        next_button = Button(info_frame, text="Connexion",command=self.login_fenetre)
        next_button.grid(row=6, column=4, pady=15, padx=10, sticky="w")

        # Configuring button colors
        enregistrer.config(bg="green", fg="white", font="Calibre 8 bold")
        next_button.config(bg="green", fg="white", font="Calibre 8 bold")

    def isEmailValide(self, email):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(regex, email):
            return True
        else:
            return False

    def isAgeValide(self, age):
        try:
            age = int(age)
            if age >= 0:
                return True
            else:
                return False
        except ValueError:
            return False

    def creer(self):
        # Récupération des données du formulaire
        firstname = self.fname_entry.get()
        lastname = self.lname_entry.get()
        gendery = self.gender.get()
        age = self.age_entry.get()
        email = self.email_entry.get()
        motPasse = self.ecri_password.get()
        confirmPassword = self.ecri_cnfpassword.get()
        check = self.var.get()

        if firstname == "" or lastname == "" or gendery == "" or age == "" or email == "" or motPasse == "" or confirmPassword == "":
            messagebox.showerror("Erreur", "Remplir les champs", parent=root)
        elif self.isEmailValide(email) == False:
            messagebox.showerror("Erreur", "Email invalide")
        elif self.isAgeValide(age) == False:
            messagebox.showerror("Erreur", "age invalide")
        elif motPasse != confirmPassword:
            messagebox.showerror("Erreur", "Les mots de passe ne sont pas conformes", parent=self.root)
        elif check == 0:
            messagebox.showerror("Erreur", "Veuillez accepter les termes et conditions", parent=self.root)
        else:
            # Hashage du mot de passe
            hashed_password = hashlib.sha256(motPasse.encode()).hexdigest()

            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="ensah")
                cur = con.cursor()
                cur.execute("SELECT * FROM info WHERE email=%s", email)
                row = cur.fetchone()

                if row is not None:
                    messagebox.showerror("Erreur", "Ce mail existe déjà", parent=self.root)
                else:
                    cur.execute(
                        "INSERT INTO info (prenom, nom, age, gender, email, mot_de_passe) VALUES (%s, %s, %s, %s,%s, %s)",
                        (firstname, lastname, age, gendery, email, hashed_password))
                    con.commit()
                      # Récupérer l'ID nouvellement inséré
                    messagebox.showinfo("Succes", f"Votre compte a été créé,Bienvenue",
                                        parent=self.root)
                    self.reini()

            finally:
                if con:
                    con.close()

    def reini(self):
        self.fname_entry.get().delete(0,END)
        self.lname_entry.get().delete(0,END)
        self.gender.get().current(0)
        self.age_entry.get().delete(0,END)
        self.email_entry.get().delete(0,END)
        self.ecri_password.get().delete(0,END)
    def login_fenetre(self):
        self.root.destroy()
        import login



root = Tk()
obj = Formulaire(root)
root.mainloop()
