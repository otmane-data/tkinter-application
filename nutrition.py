import tkinter as tk
from tkcalendar import DateEntry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class Aliment:
    def __init__(self, nom, calories, proteines, lipides, glucides):
        self.nom = nom
        self.calories = calories
        self.proteines = proteines
        self.lipides = lipides
        self.glucides = glucides

    def afficher_info_nutritionnelle(self):
        info = f"Informations nutritionnelles pour {self.nom}\n"
        info += f"Calories: {self.calories}\n"
        info += f"Protéines: {self.proteines} g\n"
        info += f"Lipides: {self.lipides} g\n"
        info += f"Glucides: {self.glucides} g"
        return info

    def calculer_nombre_calories(self, portion):
        return self.calories * portion


class FitTrackerApp:
    def __init__(self, master):
        self.master = master
        master.title("Fit Tracker")

        self.aliments_athlete = {
            "Breakfast": [
                Aliment("Oeufs", 155, 13, 11, 1),
                Aliment("Avoine", 150, 5, 3, 27),
                Aliment("Poulet", 165, 31, 3.6, 0),
            ],
            "Lunch": [
                Aliment("Saumon", 206, 29.6, 8.6, 0),
                Aliment("Riz", 130, 2.7, 0.3, 28),
                Aliment("Brocoli", 55, 4.6, 0.6, 11),
            ],
            "Dinner": [
                Aliment("Boeuf", 250, 26, 16, 0),
                Aliment("Pâtes", 131, 5.5, 0.6, 25),
                Aliment("Salade", 15, 1.35, 0.1, 2.87),
            ]
        }

        self.aliments_non_athlete = {
            "Breakfast": [
                Aliment("Pomme", 52, 0.3, 0.2, 14),
                Aliment("Yaourt", 159, 3.8, 5, 22),
                Aliment("Céréales", 210, 4, 1.5, 45),
            ],
            "Lunch": [
                Aliment("Sandwich", 330, 15, 15, 30),
                Aliment("Salade", 80, 6, 0, 16),
                Aliment("Jus d'orange", 110, 2, 0, 26),
            ],
            "Dinner": [
                Aliment("Poisson", 206, 29.6, 8.6, 0),
                Aliment("Pommes de terre", 77, 2, 0, 17),
                Aliment("Haricots verts", 31, 2, 0, 7),
            ]
        }

        self.creer_interface()

    def creer_interface(self):
        self.frames_repas = []

        for repas in ["Breakfast", "Lunch", "Dinner"]:
            frame_repas = tk.Frame(self.master)
            frame_repas.pack(pady=10)
            label_repas = tk.Label(frame_repas, text=f"{repas}")
            label_repas.pack()

            for aliment in self.aliments_athlete[repas]:  # Afficher les aliments pour un athlète par défaut
                label_aliment = tk.Label(frame_repas, text=f"{aliment.nom}:")
                label_aliment.pack(side=tk.LEFT)
                entry_portion = tk.Entry(frame_repas, width=5)
                entry_portion.pack(side=tk.LEFT)
                entry_portion.insert(0, '0')  # Par défaut, la portion est 0
                setattr(self, f"entry_{aliment.nom}_{repas}", entry_portion)

            self.frames_repas.append(frame_repas)

        self.athletetype_var = tk.StringVar(self.master)
        self.athletetype_var.set("Athlete")
        self.athletetype_menu = tk.OptionMenu(self.master, self.athletetype_var, "Athlete", "Non-Athlete",
                                              command=self.maj_interface)
        self.athletetype_menu.pack()

        self.date_label = tk.Label(self.master, text="Date:")
        self.date_label.pack()

        self.cal = DateEntry(self.master, width=12, background='darkblue',
                             foreground='white', borderwidth=2)
        self.cal.pack(padx=10, pady=10)

        self.bouton_calculer = tk.Button(self.master, text="Calculer les calories totales",
                                         command=self.calculer_calories)
        self.bouton_calculer.pack()

        self.label_resultat = tk.Label(self.master, text="")
        self.label_resultat.pack()

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack()

    def maj_interface(self, event=None):
        if self.athletetype_var.get() == "Athlete":
            self.maj_aliments_interface(self.aliments_athlete)
        else:
            self.maj_aliments_interface(self.aliments_non_athlete)

    def maj_aliments_interface(self, aliments):
        for frame_repas in self.frames_repas:
            for widget in frame_repas.winfo_children():
                widget.destroy()

        for repas in ["Breakfast", "Lunch", "Dinner"]:
            frame_repas = self.frames_repas.pop(0)
            for aliment in aliments[repas]:
                label_aliment = tk.Label(frame_repas, text=f"{aliment.nom}:")
                label_aliment.pack(side=tk.LEFT)
                entry_portion = tk.Entry(frame_repas, width=5)
                entry_portion.pack(side=tk.LEFT)
                entry_portion.insert(0, '0')
                setattr(self, f"entry_{aliment.nom}_{repas}", entry_portion)
            self.frames_repas.append(frame_repas)

    def calculer_calories(self):
        total_calories = 0
        for repas in ["Breakfast", "Lunch", "Dinner"]:
            for aliment in self.aliments_athlete[repas] if self.athletetype_var.get() == "Athlete" else \
            self.aliments_non_athlete[repas]:
                entry_portion = getattr(self, f"entry_{aliment.nom}_{repas}")
                portion = float(entry_portion.get())
                total_calories += aliment.calculer_nombre_calories(portion)
        self.label_resultat.config(text=f"Total des calories consommées dans la journée: {total_calories} calories")

        # Créer un graphique à barres pour les calories par repas
        repas = ["Breakfast", "Lunch", "Dinner"]
        calories_par_repas = [sum(
            aliment.calculer_nombre_calories(float(getattr(self, f"entry_{aliment.nom}_{repas[i]}").get())) for aliment
            in self.aliments_athlete[repas[i]] if self.athletetype_var.get() == "Athlete") for i in range(3)]
        self.ax.clear()
        self.ax.bar(repas, calories_par_repas, color='skyblue')
        self.ax.set_ylabel('Calories')
        self.ax.set_title('Calories par repas')
        self.canvas.draw()
    def fenetre_fit(self):
        self.master.destroy()
        import fitness


root = tk.Tk()
app = FitTrackerApp(root)
root.mainloop()