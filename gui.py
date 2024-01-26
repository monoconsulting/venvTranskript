import tkinter as tk
import csv
import os
import logging
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Konfiguration av logger
logging.basicConfig(level=logging.INFO,
                    filename='myapp.log',
                    filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("gui.py startas")

class GuiApp:
    def __init__(self, filename):
        self.root = tk.Tk()
        self.root.title(f"Projektväljare - {filename}")

        # Ställ in storlek och position
        self.root.geometry("800x600+100+100")

        # Ändra bakgrundsfärg
        self.root.configure(bg='#f0f0f0')
        self.selected_project = None
        self.company_name = None
        self.meeting_type = None
        self.participants = None

        # Dropdown för projekt
        self.project_options = self.read_projects('projects.csv')
        self.project_var = tk.StringVar(self.root)
        self.project_var.set(self.project_options[0][0])  # Sätt standardval till första projektet
        self.project_dropdown = tk.OptionMenu(self.root, self.project_var, *[option[0] for option in self.project_options])
        self.project_dropdown.pack()

        # Label och Fritextfält för mötestyp
        self.meeting_type_label = tk.Label(self.root, text="Mötestyp")
        self.meeting_type_label.pack()
        self.meeting_type_entry = tk.Entry(self.root)
        self.meeting_type_entry.pack()

        # Label och Fritextfält för deltagarlista
        self.participant_list_label = tk.Label(self.root, text="Deltagare")
        self.participant_list_label.pack()
        self.participant_list_entry = tk.Entry(self.root)
        self.participant_list_entry.pack()

        # Knapp för att visa val
        self.show_selection_button = tk.Button(self.root, text="Visa Val", command=self.show_selections)
        self.show_selection_button.pack()

        # Knapp för att starta processen
        self.start_button = tk.Button(self.root, text="Starta Process", command=self.start_process)
        self.start_button.pack()

    def run(self):
        self.root.mainloop()

    def read_projects(self, filename):
        project_data = []
        with open(filename, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                project_data.append((row['project_name'], row['company_name']))
        return project_data

    def show_selections(self):
        selected_project_name = self.project_var.get()
        selected_project_info = next((item for item in self.project_options if item[0] == selected_project_name), (None, None))
        self.selected_project, self.company_name = selected_project_info
        self.meeting_type = self.meeting_type_entry.get()
        self.participants = self.participant_list_entry.get()
        print(f"Valt projekt: {self.selected_project}, Företag: {self.company_name}, Mötestyp: {self.meeting_type}, Deltagarlista: {self.participants}")

    def start_process(self):
        selected_project_name = self.project_var.get()
        selected_project_info = next((item for item in self.project_options if item[0] == selected_project_name), (None, None))
        self.selected_project, self.company_name = selected_project_info
        self.meeting_type = self.meeting_type_entry.get()
        self.participants = self.participant_list_entry.get()

        if None not in [self.selected_project, self.company_name, self.meeting_type, self.participants]:
# Skriv ut valen till en fil
            with open("selected_options.txt", "w") as file:
                file.write(f"{self.selected_project}\n")
                file.write(f"{self.company_name}\n")
                file.write(f"{self.meeting_type}\n")
                file.write(f"{self.participants}\n")
            print("Valen har sparats")

        else:
            print("Ett eller flera val är inte gjorda korrekt")

        # Stäng ner GUI:t
        self.root.destroy()

# Om du vill köra GUI direkt för testning
if __name__ == "__main__":
    app = GuiApp("Testfil")
    app.run()
