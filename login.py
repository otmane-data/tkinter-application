from tkinter import *
from tkinter import ttk, messagebox
import pymysql
from PIL import ImageTk, Image
#from fitness import FIT
import hashlib
import re
class Login:
    def __init__(self, root):
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
        login_frame.place(relx=0.5, rely=0.5, anchor=CENTER, width=500)  # Adjust width of the login_frame

        email_label = Label(login_frame, text="  Email:", font=("Arial", 14), bg="#1a4f76", fg="black",pady=35)
        email_label.grid(row=1, column=0, padx=10, pady=10)
        self.email_entry = Entry(login_frame, font=("Arial", 12), bg="#d3d3d3")
        self.email_entry.grid(row=1, column=1, padx=10, pady=10)

        password_label = Label(login_frame, text="  Password:", font=("Arial", 14), bg="#1a4f76", fg="black")
        password_label.grid(row=2, column=0, padx=10, pady=10)
        self.password_entry = Entry(login_frame, show="*", font=("Arial", 12), bg="#d3d3d3")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        login_button = Button(login_frame, text="  Login  ", command=self.connexion, font=("Arial", 14), bg="cyan", fg="black")
        login_button.grid(row=4, column=1, columnspan=2, pady=20)

        creer_btn = Button(login_frame, text=" Créer un nouveau compte", command=self.fenetre_formulaire, cursor="hand2",
                           font=("calibre", 10), bd=0, fg="orange",bg="#1a4f76")
        creer_btn.grid(row=3, column=0, pady=20, sticky="w")

        oublier_btn = Button(login_frame, text="Mot de passe oublié", command=self.passwd_oublie, cursor="hand2", font=("calibre", 10),
                             bd=0, fg="orange",bg="#1a4f76")
        oublier_btn.grid(row=3, column=3, pady=20, sticky="e")


    def connexion(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if password == '' or email == '':
            messagebox.showerror("Erreur", "Remplir les champs", parent=self.root)

        else:
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="ensah")
                cur = con.cursor()
                cur.execute("SELECT * FROM info WHERE email=%s", email)
                row = cur.fetchone()

                if row is None:
                    messagebox.showerror("Erreur", "Email invalide", parent=self.root)
                else:
                    stored_password = row[6]  # Récupération du mot de passe haché dans la colonne appropriée

                    # Hashage du mot de passe entré par l'utilisateur
                    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

                    print("Hashed Password:", hashed_password)
                    print("Stored Password:", stored_password)

                    if hashed_password == stored_password:
                        messagebox.showinfo("Succes", "Bienvenu", parent=self.root)
                        global user
                        user = row
                        self.fenetre_fitness()
                    else:
                        messagebox.showerror("Erreur", "Mot de passe incorrect", parent=self.root)

            except Exception as es:
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(es)}", parent=self.root)

    def passwd_oublie(self):
        email = self.email_entry.get()

        if email == '':
            messagebox.showerror("Erreur", "Veuillez donner un mail valide", parent=self.root)
        else:
            try:
                con = pymysql.connect(host="localhost", user="root", password="", database="ensah")

                cur = con.cursor()
                cur.execute("SELECT * FROM info WHERE email=%s", email)
                row = cur.fetchone()

                if row ==None:
                    messagebox.showerror("Erreur", "Veuillez entrer un mail valide", parent=self.root)
                else:
                    con.close()
                    self.root2= Toplevel()
                    self.root2.title("Mot de passe oublié")
                    self.root2.geometry("300x300")
                    self.root2.config(bg="#b4c6d0")
                    self.root2.focus_force()
                    self.root2.grab_set()
                    info_frame = Frame(self.root2, bg="white")
                    info_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
                    # Label and entry for user to enter their email
                    email_label = Label( self.root2, text="email:", font=("Arial", 12))
                    email_label.pack(pady=10)


                    self.email_entry = Entry( self.root2, font=("Arial", 12))
                    self.email_entry.pack(pady=5)
                    NouvPass_label = Label( self.root2, text="nouveau mot de passe:", font=("Arial", 12))
                    NouvPass_label.pack(pady=10)
                    self.NouvPass_entry = Entry( self.root2, font=("Arial", 12), show="*")
                    self.NouvPass_entry.pack(pady=5)
                    cfPass_label = Label( self.root2, text="Confirmer mot de passe:", font=("Arial", 12))
                    cfPass_label.pack(pady=10)
                    self.cfPass_entry = Entry( self.root2, font=("Arial", 12), show="*")
                    self.cfPass_entry.pack(pady=5)
                    self.root2 = Button(self.root2, text="Modifier",bg="green",command=self.oublier)
                    self.root2.pack(pady=10)


            except Exception as es:
                  messagebox.showerror("Erreur", f"Erreur de connexion: {str(es)}", parent=self.root2)

    def oublier(self):
        # Check if all fields are filled
        if self.email_entry.get() == "" or self.NouvPass_entry.get() == "" or self.cfPass_entry.get() == "":
            messagebox.showerror("Erreur", "Remplir tous les champs", parent=self.root2)
        else:
            try:
                # Establish a connection to the database
                con = pymysql.connect(host="localhost", user="root", password="", database="ensah")
                cur = con.cursor()

                # Retrieve the user's information based on their email
                cur.execute("SELECT * FROM info WHERE email=%s", (self.email_entry.get(),))
                row = cur.fetchone()

                # If no user is found with the provided email
                if row is None:
                    messagebox.showerror("Erreur", "Email n'existe pas", parent=self.root2)
                else:
                    # Hash the new password
                    hashed_password = hashlib.sha256(self.NouvPass_entry.get().encode()).hexdigest()

                    # Update the user's password with the hashed password
                    cur.execute("UPDATE info SET mot_de_passe=%s WHERE email=%s",
                                (hashed_password, self.email_entry.get()))

                    # Commit the changes to the database
                    con.commit()

                    # Close the database connection
                    con.close()

                    # Inform the user that their password has been updated successfully
                    messagebox.showinfo("Succes", "Vous avez modifié votre mot de passe", parent=self.root2)
            except Exception as es:
                # Display an error message if any exception occurs during the process
                messagebox.showerror("Erreur", f"Erreur de connexion: {str(es)}", parent=self.root)
    def fenetre_formulaire(self):
        self.root.destroy()
        import formulaire
    def fenetre_fitness(self):
        self.root.destroy()
        import fitness



user = None
root = Tk()
obj = Login(root)
root.mainloop()
