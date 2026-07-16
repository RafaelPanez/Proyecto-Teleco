# gui/study_window.py

import customtkinter as ctk

from tkinter import messagebox

from api import get_studies, get_study
from utils.auth import get_token


class StudyWindow:

    def __init__(self, root):

        self.root = root

        self.root.title("Estudios disponibles")
        self.root.geometry("600x500")

        self.studies = []

        self.create_widgets()

        self.load_studies()


    def create_widgets(self):

        self.title_label = ctk.CTkLabel(
            self.root,
            text="Estudios",
            font=("Arial", 22)
        )

        self.title_label.pack(
            pady=20
        )


        self.study_list = ctk.CTkTextbox(
            self.root,
            width=500,
            height=200
        )

        self.study_list.pack(
            pady=10,
            padx=40
        )


        self.code_entry = ctk.CTkEntry(
            self.root,
            placeholder_text="Código del estudio"
        )

        self.code_entry.pack(
            pady=10,
            padx=50,
            fill="x"
        )


        self.details_button = ctk.CTkButton(
            self.root,
            text="Ver detalles",
            command=self.show_details
        )

        self.details_button.pack(
            pady=10
        )


    def load_studies(self):

        token = get_token()

        response = get_studies(token)


        if isinstance(response, list):

            self.studies = response


            self.study_list.delete(
                "0.0",
                "end"
            )


            for study in self.studies:

                self.study_list.insert(
                    "end",
                    f"Código: {study.get('study_code')}\n"
                    f"Paciente: {study.get('patient_name')}\n"
                    f"Tipo: {study.get('study_type')}\n"
                    f"Estado: {study.get('status')}\n"
                    "----------------------\n"
                )


        else:

            messagebox.showerror(
                "Error",
                response.get(
                    "message",
                    "No se pudieron cargar estudios"
                )
            )
    

    def show_details(self):

        code = self.code_entry.get()


        if not code:

            messagebox.showwarning(
                "Código",
                "Ingrese el código del estudio"
            )

            return


        token = get_token()


        response = get_study(
            code,
            token
        )


        if response.get("success", True):

            details = ""


            for key, value in response.items():

                details += f"{key}: {value}\n"


            messagebox.showinfo(
                "Detalles del estudio",
                details
            )


        else:

            messagebox.showerror(
                "Error",
                "No se encontró el estudio"
            )