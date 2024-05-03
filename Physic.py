from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import tkcalendar
import  login
import pymysql
import datetime
class SportWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Chronomètre")
        self.wanted_hour = IntVar(value=0)
        self.wanted_minute = IntVar(value=0)
        self.wanted_second = IntVar(value=0)
        self.hour_var = StringVar(value='00')
        self.minute_var = StringVar(value='00')
        self.second_var = StringVar(value='00')
        self.counting = False

        self.create_widgets()

    def create_widgets(self):
        # Load image
        image_path = r"C:\Users\DELL 5410\Documents\run.jpg"
        image = Image.open(image_path)
        image = image.resize((200, 200), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)

        # Image label
        self.image_label = Label(self, image=self.photo)
        self.image_label.grid(row=0, column=0, pady=10)

        # Time display
        time_frame = Frame(self)
        time_frame.grid(row=1, column=0, pady=10)
        Label(time_frame, font=('Arial', 50), textvariable=self.hour_var).grid(row=0, column=0)
        Label(time_frame, font=('Arial', 50), text=":").grid(row=0, column=1)
        Label(time_frame, font=('Arial', 50), textvariable=self.minute_var).grid(row=0, column=2)
        Label(time_frame, font=('Arial', 50), text=":").grid(row=0, column=3)
        Label(time_frame, font=('Arial', 50), textvariable=self.second_var).grid(row=0, column=4)

        # Buttons
        button_frame = Frame(self)
        button_frame.grid(row=2, column=0, pady=10)
        Button(button_frame, text="Start", command=self.start_countdown).grid(row=0, column=0)
        Button(button_frame, text="Edit", command=self.edit_time).grid(row=0, column=1)
    def create_widgets1(self):
        # Load image
        image_path = r"C:\Users\DELL 5410\Documents\run.jpg"
        image = Image.open(image_path)
        image = image.resize((200, 200), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(image)

        # Image label
        self.image_label = Label(self, image=self.photo)
        self.image_label.grid(row=0, column=1, pady=10)

        # Time display
        time_frame = Frame(self)
        time_frame.grid(row=1, column=1, pady=10)
        Label(time_frame, font=('Arial', 50), textvariable=self.hour_var).grid(row=1, column=0)
        Label(time_frame, font=('Arial', 50), text=":").grid(row=0, column=1)
        Label(time_frame, font=('Arial', 50), textvariable=self.minute_var).grid(row=1, column=2)
        Label(time_frame, font=('Arial', 50), text=":").grid(row=0, column=3)
        Label(time_frame, font=('Arial', 50), textvariable=self.second_var).grid(row=1, column=4)

        # Buttons
        button_frame = Frame(self)
        button_frame.grid(row=3, column=0, pady=10)
        Button(button_frame, text="Start", command=self.start_countdown).grid(row=1, column=0)
        Button(button_frame, text="Edit", command=self.edit_time).grid(row=0, column=1)

    def start_countdown(self):
        self.counting = True
        total_seconds = self.wanted_hour.get() * 3600 + self.wanted_minute.get() * 60 + self.wanted_second.get()
        while total_seconds > -1 and self.counting:
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.hour_var.set(f'{hours:02d}')
            self.minute_var.set(f'{minutes:02d}')
            self.second_var.set(f'{seconds:02d}')
            self.update()

            total_seconds -= 1
            self.after(1000)  # Wait for 1 second

    def edit_time(self):
        self.counting = False
        edit_window = Toplevel(self)
        edit_window.title("Edit Time")
        edit_window.geometry("200x150")
        Label(edit_window, text="Hour:").grid(row=0, column=0)
        Label(edit_window, text="Minute:").grid(row=1, column=0)
        Label(edit_window, text="Second:").grid(row=2, column=0)
        hour_entry = Entry(edit_window)
        minute_entry = Entry(edit_window)
        second_entry = Entry(edit_window)
        hour_entry.grid(row=0, column=1)
        minute_entry.grid(row=1, column=1)
        second_entry.grid(row=2, column=1)
        submit_button = Button(edit_window, text="Submit", command=lambda: self.submit_time(hour_entry.get(), minute_entry.get(), second_entry.get(), edit_window))
        submit_button.grid(row=3, columnspan=2, pady=10)

    def submit_time(self, hour, minute, second, window):
        try:
            hour = int(hour)
        except ValueError:
            hour = 0
        try:
            minute = int(minute)
        except ValueError:
            minute = 0
        try:
            second = int(second)
        except ValueError:
            second = 0

        self.wanted_hour.set(hour)
        self.wanted_minute.set(minute)
        self.wanted_second.set(second)
        self.hour_var.set(f'{hour:02d}')
        self.minute_var.set(f'{minute:02d}')
        self.second_var.set(f'{second:02d}')

        window.destroy()

class FitTrackerApp:
    def __init__(self, root):
        self.root = root
        self.user = login.user
        self.root.title("FitTracker")
        self.root.geometry("800x600")
        self.bg_image = Image.open(r"C:\Users\DELL 5410\Documents\fit.png")
        self.bg_image = self.bg_image.resize((800, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Set the background image as the window background
        self.background_label = Label(self.root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.root.focus_force()

        self.data_list = []
        self.create_widgets()

    def create_widgets(self):
        # Initialisation de l'interface utilisateur
        self.initialize_ui()

        # Création des widgets
        self.create_input_widgets()
        self.create_buttons()

        # Affichage du tableau
        self.create_table()

        # Affichage du graphique
        self.create_plot()

    def initialize_ui(self):
        # Chargement de l'image de fond
        self.bg_image = Image.open(r"C:\Users\DELL 5410\Documents\fit.png")
        self.bg_image = self.bg_image.resize((800, 600), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        # Affichage de l'image de fond
        self.background_label = Label(self.root, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_input_widgets(self):
        # Labels et champs de saisie
        self.date_label = Label(self.root, text="Date:", font="Calibre 15 bold", bg="#1a4f76")
        self.date_label.grid(row=0, column=0, padx=5, pady=5)
        date_pattern = 'dd/MM/yyyy'
        self.date_entry = tkcalendar.DateEntry(self.root,date_pattern= date_pattern, width=20, bg="#d3d3d3", font=("Arial", 12))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        # Liste des sports
        self.sport_label = Label(self.root, text="Sport:", font="Calibre 15 bold", bg="#1a4f76")
        self.sport_label.grid(row=1, column=0, padx=5, pady=5)
        self.sport_combobox = ttk.Combobox(self.root, values=["push up", "squats", "pull up", "cardio"], width=20)
        self.sport_combobox.grid(row=1, column=1, padx=5, pady=5)


        # Type d'activité (faible, modérée, intense)
        self.activity_label = Label(self.root, text="Type d'activité:", font="Calibre 15 bold", bg="#1a4f76")
        self.activity_label.grid(row=2, column=0)
        self.activity_var = StringVar()
        self.activity_radiobutton1 = Radiobutton(self.root, text="Faible", variable=self.activity_var, value="Faible")
        self.activity_radiobutton1.grid(row=2, column=1)
        self.activity_radiobutton2 = Radiobutton(self.root, text="Modérée", variable=self.activity_var, value="Modérée")
        self.activity_radiobutton2.grid(row=2, column=2)
        self.activity_radiobutton3 = Radiobutton(self.root, text="Intense", variable=self.activity_var, value="Intense")
        self.activity_radiobutton3.grid(row=2, column=3)
        self.add_button = Button(self.root, text="chronometre",command=self.sport, bg="#1a4f76", font="Calibre 15 bold")
        self.add_button.grid(row=3, column=0, padx=5, pady=5)

        # Durée de l'entraînement
        self.duration_label = Label(self.root, text="Durée (minutes):", font="Calibre 15 bold", bg="#1a4f76")
        self.duration_label.grid(row=4, column=0, padx=5, pady=5)
        self.duration_entry = Entry(self.root, width=20, bg="#d3d3d3", font=("Arial", 12))
        self.duration_entry.grid(row=4, column=1, padx=5, pady=5)

    def create_buttons(self):
        # Boutons
        self.add_button = Button(self.root, text="Ajouter", command=self.add_data, bg="green", font="Calibre 15 bold")
        self.add_button.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

        self.clear_button = Button(self.root, text="Effacer", command=self.clear_fields, bg="red",
                                   font="Calibre 15 bold")
        self.clear_button.grid(row=4, column=3, columnspan=2, padx=5, pady=5)
        self.Retour_button = Button(self.root, text="acceuil", command=self.fenetre_fitness, bg="orange",
                                   font="Calibre 15 bold")
        self.Retour_button.grid(row=4, column=1, columnspan=4, padx=7, pady=5)

    def create_table(self):
        # Tableau
        self.data_table = Listbox(self.root, width=50, height=10)
        self.data_table.grid(row=5, column=0, columnspan=2, padx=8, pady=10)

    def create_plot(self):
        # Figure Matplotlib et canevas pour le premier graphe
        self.fig, self.ax = plt.subplots(figsize=(4, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=5, column=2, columnspan=2, padx=10, pady=10)

    def add_data(self):
        sport = self.sport_combobox.get()
        activity = self.activity_var.get()
        duration = int(self.duration_entry.get())
        user_id = self.user[0]  # Assuming user ID is stored in self.user[0]

        # Calcul des calories brûlées en fonction du type d'activité et de la durée
        calories = self.calculate_calories(sport, activity, duration)

        new_data = {
            "id": len(self.data_list) + 1,
            "date": self.date_entry.get(),
            "sport": sport,
            "calories": calories
        }
        self.data_list.append(new_data)
        self.update_table()
        self.plot_data()

        con = None  # Initialize con outside the try block
        try:
            con = pymysql.connect(host="localhost", user="root", password="", database="ensah")
            cur = con.cursor()

            # Format the date to 'YYYY-MM-DD' format
            formatted_date = datetime.datetime.strptime(new_data["date"], "%d/%m/%Y").strftime("%Y-%m-%d")

            # Assuming you have a table named 'data' with appropriate columns
            cur.execute(
                "INSERT INTO data (info_id, date, sport, type_sport, duree, calories) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, formatted_date, new_data["sport"], activity, duration, calories))
            con.commit()

        except pymysql.Error as e:
            print(f"Error: {e}")

        finally:
            if con:  # Check if con is not None before closing
                con.close()

    def calculate_calories(self, sport, activity, duration):
        # Votre calcul de calories ici...
        calorie_values = {
            "push up": {"Faible": 10, "Modérée": 20, "Intense": 30},
            "squats": {"Faible": 15, "Modérée": 25, "Intense": 35},
            "pull up": {"Faible": 20, "Modérée": 30, "Intense": 40},
            "cardio": {"Faible": 25, "Modérée": 35, "Intense": 45}
        }

        if sport in calorie_values and activity in calorie_values[sport]:
            return calorie_values[sport][activity] * duration
        else:
            return 0

    def clear_fields(self):
        self.date_entry.delete(0, END)
        self.sport_combobox.set("")
        self.duration_entry.delete(0, END)

    def update_table(self):
        self.data_table.delete(0, END)
        for entry in self.data_list:
            self.data_table.insert(END, f"{entry['id']} | {entry['date']} | {entry['sport']} | {entry['calories']} cal")

    def plot_data(self):
        self.ax.clear()
        sports = [entry['date'] for entry in self.data_list]
        calories = [entry['calories'] for entry in self.data_list]
        self.ax.bar(sports, calories, color='skyblue')
        self.ax.set_xlabel("date")
        self.ax.set_ylabel("Calories")
        self.ax.set_title("Calories vs. date")
        self.canvas.draw()
    def sport(self):
        self.root2 = SportWindow(self.root)
    def fenetre_fitness(self):
        self.root.destroy()
        import fitness

root = Tk()
app = FitTrackerApp(root)
root.mainloop()