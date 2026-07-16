# gui/delete_window.py

import customtkinter as ctk

from tkinter import messagebox

from api import get_studies, delete_study
from utils.auth import get_token



class DeleteWindow:


    def __init__(self, root):

        self.root = root

        self.root.title("Eliminar estudio")
        self.root.geometry("500x400")

        self.studies = []

        self.create_widgets()

        self.load_studies()



    def create_widgets(self):


        title = ctk.CTkLabel(
            self.root,
            text="Eliminar estudio",
            font=("Arial", 22)
        )

        title.pack(
            pady=20
        )



        self.study_combo = ctk.CTkComboBox(
            self.root,
            values=[]
        )

        self.study_combo.pack(
            pady=20,
            padx=50,
            fill="x"
        )



        self.delete_button = ctk.CTkButton(
            self.root,
            text="Eliminar seleccionado",
            command=self.delete_selected
        )

        self.delete_button.pack(
            pady=20
        )



    def load_studies(self):


        token = get_token()


        response = get_studies(token)


        if isinstance(response, list):

            self.studies = response


            options = []


            for study in response:

                options.append(
                    study["study_code"]
                )


            self.study_combo.configure(
                values=options
            )


            if options:

                self.study_combo.set(
                    options[0]
                )


        else:

            messagebox.showerror(
                "Error",
                response.get(
                    "message",
                    "No se pudieron cargar estudios"
                )
            )



    def delete_selected(self):


        study_code = self.study_combo.get()


        if not study_code:


            messagebox.showwarning(
                "Estudio",
                "Seleccione un estudio"
            )

            return



        confirm = messagebox.askyesno(
            "Confirmar",
            f"¿Eliminar {study_code}?"
        )


        if not confirm:

            return



        token = get_token()


        response = delete_study(
            study_code,
            token
        )



        if "error" not in response:


            messagebox.showinfo(
                "Correcto",
                response.get(
                    "message",
                    "Estudio eliminado"
                )
            )


            self.load_studies()



        else:


            messagebox.showerror(
                "Error",
                response.get(
                    "message",
                    "No se pudo eliminar"
                )
            )