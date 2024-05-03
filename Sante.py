from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk, Image
import pymysql
import login
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



class FitTrackerApp:
    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(self.parent)
        self.frame.pack()
        self.sleeping_quality_var = StringVar(value="")
        self.hours_var = StringVar(value="")
        self.date_var = StringVar(value="")
        self.time_values = []
        self.hours_values = []
        self.date_values = []
        self.create_widgets()

    def create_widgets(self):
        sleeping_label = Label(self.frame, text="Sleeping Quality:")
        sleeping_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.sleeping_quality_display = Label(self.frame, textvariable=self.sleeping_quality_var)
        self.sleeping_quality_display.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        hours_label = Label(self.frame, text="Number of Hours:")
        hours_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.hours_entry = ttk.Entry(self.frame, textvariable=self.hours_var)
        self.hours_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        date_label = Label(self.frame, text="Sleeping Date:")
        date_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.date_entry = DateEntry(self.frame, textvariable=self.date_var, date_pattern="yyyy-mm-dd")
        self.date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.plot_btn = Button(self.frame, text="Plot", command=self.plot_graph)
        self.plot_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def determine_sleeping_quality(self, hours):
        if hours >= 8:
            return "Excellent"
        elif hours >= 7:
            return "Good"
        elif hours >= 6:
            return "Fair"
        else:
            return "Poor"

    def plot_graph(self):
        try:
            hours = int(float(self.hours_var.get()))
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of hours.")
            return

        date = self.date_var.get()
        if not date:
            messagebox.showerror("Error", "Please enter a sleeping date.")
            return

        quality = self.determine_sleeping_quality(hours)
        self.sleeping_quality_var.set(quality)

        self.time_values.append(date)
        self.hours_values.append(hours)
        self.date_values.append(date)

        self.ax.clear()
        self.ax.plot(self.date_values, self.hours_values, marker='o', linestyle='-')
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Number of Hours")
        self.fig.autofmt_xdate()
        self.fig.canvas.draw()

class Formulaire:
    def __init__(self, root):
        self.root = root
        self.user = login.user
        self.root.title("suivi de santé")
        self.root.geometry("700x500")
        self.df = None

        self.bg_image = Image.open(r"C:\Users\DELL 5410\Documents\fit.png")  # Assuming fit.png is in the same directory
        self.bg_image = self.bg_image.resize((800, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.background_label = Label(self.root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.info_frame = Frame(self.root, bg="white", bd=5)
        self.info_frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.3, anchor='n')

        self.fitness_frame = Frame(self.root, bg="white", bd=5)
        self.fitness_frame.place(relx=0.5, rely=0.45, relwidth=0.75, relheight=0.4, anchor='n')

        self.title_label = Label(self.root, text="Suivi de santé ", font=("Arial", 18, "bold"), bg="#1a4f76", fg="white")
        self.title_label.place(relx=0.5, rely=0.02, anchor='n')

        consulte_button = Button(self.root, text="mon profil", command=self.consulter, font=("Arial", 12),bg="#1a4f76", fg="white", relief="raised")
        consulte_button.place(relx=0.5, rely=0.85, relwidth=0.2, relheight=0.1, anchor='n')

        nutrition_frame = Frame(self.root, bg="white", bd=5)
        nutrition_frame.place(relx=0.3, rely=0.85, relwidth=0.2, relheight=0.1, anchor='n')


        button1 = Button(self.root, text="Nutrition",command=self.fenetre_Nutrition,font=("Arial", 12), bg="#1a4f76",fg="white", relief="raised")
        button1.place(relx=0.3, rely=0.85, relwidth=0.2, relheight=0.1,anchor='n')

        button2 = Button(self.root, text="suivi de sommeil", command=self.show_sleep_frame, font=("Arial", 12),
                         bg="#1a4f76", fg="white", relief="raised")
        button2.place(relx=0.7, rely=0.85, relwidth=0.2, relheight=0.1,anchor='n')

    def show_sleep_frame(self):
        self.info_frame.pack_forget()
        self.fitness_frame.pack_forget()
        self.fit_app = FitTrackerApp(self.root)



    def consulter(self):
        try:
            inserted_id = self.user[0]
            con = pymysql.connect(host="localhost", user="root", password="", database="ensah")
            cur = con.cursor()

            cur.execute("SELECT * FROM info WHERE id=%s", inserted_id)
            user_info = cur.fetchone()

            if user_info is None:
                messagebox.showerror("Erreur", "Cet ID n'existe pas", parent=self.root)
            else:
                cur.execute("SELECT * FROM fitness WHERE id=%s ORDER BY id_fit DESC LIMIT 1", inserted_id)
                fitness_info = cur.fetchone()

                if fitness_info is not None:
                    self.display_user_info(user_info)
                    self.display_fitness_info(fitness_info)
                else:
                    messagebox.showerror("Erreur", "Aucune donnée fitness trouvée pour cet utilisateur")

        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

        finally:
            if 'con' in locals():
                con.close()

    def display_user_info(self, user_info):
        for widget in self.info_frame.winfo_children():
            widget.destroy()

        labels = ["ID", "Prénom", "Nom", "Age", "Genre", "Email"]
        for i, label in enumerate(labels):
            Label(self.info_frame, text=f"{label}:", font=("Arial", 12), bg="white").grid(row=i, column=0, padx=10, pady=5)
            Label(self.info_frame, text=f"{user_info[i]}", font=("Arial", 12), bg="white").grid(row=i, column=1, padx=10, pady=5)

    def display_fitness_info(self, fitness_info):
        for widget in self.fitness_frame.winfo_children():
            widget.destroy()

        labels = ["Poids (kg)","Taille (cm)", "Goal", "IMC","Interprétation"]
        for i, label in enumerate(labels):
            Label(self.fitness_frame, text=f"{label}:", font=("Arial", 12), bg="white").grid(row=i, column=0, padx=10, pady=5)
            Label(self.fitness_frame, text=f"{fitness_info[i+2]}", font=("Arial", 12), bg="white").grid(row=i, column=1, padx=10, pady=5)
    def fenetre_Nutrition(self):
        self.root.destroy()
        import nutrition
root = Tk()
app = Formulaire(root)
root.mainloop()
