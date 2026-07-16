# gui/upload_window.py

import customtkinter as ctk

from tkinter import filedialog, messagebox

from api import upload_file
from utils.auth import get_token



class UploadWindow:


    def __init__(self, root):

        self.root = root

        self.root.title("Subir estudio")
        self.root.geometry("650x850")

        self.filepath = None

        self.entries = {}

        self.create_widgets()



    def create_widgets(self):


        title = ctk.CTkLabel(
            self.root,
            text="Carga de estudio",
            font=("Arial", 24)
        )

        title.pack(
            pady=20
        )



        # -------------------------
        # Selección de archivo
        # -------------------------

        self.file_button = ctk.CTkButton(
            self.root,
            text="Seleccionar archivo",
            command=self.select_file
        )

        self.file_button.pack(
            pady=10
        )


        self.file_label = ctk.CTkLabel(
            self.root,
            text="Ningún archivo seleccionado"
        )

        self.file_label.pack(
            pady=5
        )



        # -------------------------
        # Centros y estudios válidos
        # -------------------------

        self.centers = {


            "Centro 1 - Monitoreo Fisiologico": [

                "Electrocardiograma",
                "Frecuencia cardíaca",
                "Saturación de oxígeno",
                "Temperatura corporal",
                "Presión arterial"

            ],



            "Centro 2 - Diagnostico por Imagenes": [

                "Radiografías",
                "Ecografías",
                "Imágenes clínicas asociadas a procedimientos diagnósticos"

            ],



            "Centro 3 - Estudios Avanzados": [

                "Electrocardiograma",
                "Frecuencia cardíaca",
                "Saturación de oxígeno",
                "Temperatura corporal",
                "Presión arterial",
                "Radiografías",
                "Ecografías",
                "Imágenes clínicas asociadas a procedimientos diagnósticos",
                "Estudios avanzados"

            ]

        }



        center_label = ctk.CTkLabel(
            self.root,
            text="Centro"
        )

        center_label.pack(
            pady=5
        )



        self.center_combo = ctk.CTkComboBox(

            self.root,

            values=list(
                self.centers.keys()
            ),

            command=self.update_study_types

        )

        self.center_combo.pack(

            pady=5,

            padx=50,

            fill="x"

        )


        self.center_combo.set(
            "Seleccione centro"
        )




        study_label = ctk.CTkLabel(
            self.root,
            text="Tipo de estudio"
        )

        study_label.pack(
            pady=5
        )



        self.study_combo = ctk.CTkComboBox(

            self.root,

            values=[]

        )

        self.study_combo.pack(

            pady=5,

            padx=50,

            fill="x"

        )


        self.study_combo.set(
            "Seleccione tipo de estudio"
        )



        # -------------------------
        # Campos adicionales
        # -------------------------

        fields = [

            ("patient_id", "ID paciente"),

            ("patient_name", "Nombre paciente"),

            ("study_code", "Código estudio"),

            ("center_code", "Código centro"),

            ("center_location", "Ubicación centro"),

            ("operator_code", "Código operador"),

            ("operator_name", "Nombre operador"),

            ("report", "Reporte")

        ]



        for key, placeholder in fields:


            entry = ctk.CTkEntry(

                self.root,

                placeholder_text=placeholder

            )


            entry.pack(

                pady=5,

                padx=50,

                fill="x"

            )


            self.entries[key] = entry




        # -------------------------
        # Botón enviar
        # -------------------------

        upload_button = ctk.CTkButton(

            self.root,

            text="Enviar estudio",

            command=self.send_file

        )


        upload_button.pack(

            pady=20

        )





    def update_study_types(self, selected_center):


        studies = self.centers[selected_center]


        self.study_combo.configure(

            values=studies

        )


        self.study_combo.set(

            "Seleccione tipo de estudio"

        )





    def select_file(self):


        filepath = filedialog.askopenfilename()


        if filepath:


            self.filepath = filepath


            self.file_label.configure(

                text=filepath

            )





    def send_file(self):


        if not self.filepath:


            messagebox.showwarning(

                "Archivo",

                "Seleccione un archivo"

            )

            return




        metadata = {}

        missing = []



        # Centro

        selected_center = self.center_combo.get()


        if selected_center == "Seleccione centro":


            missing.append(
                "center_name"
            )


        else:


            metadata["center_name"] = selected_center




        # Tipo de estudio

        selected_study = self.study_combo.get()


        if selected_study == "Seleccione tipo de estudio":


            missing.append(
                "study_type"
            )


        else:


            metadata["study_type"] = selected_study




        # Campos restantes

        for key, entry in self.entries.items():


            value = entry.get().strip()


            if not value:


                missing.append(key)


            metadata[key] = value





        if missing:


            messagebox.showwarning(

                "Campos faltantes",

                "Complete:\n\n" +
                "\n".join(missing)

            )

            return




        token = get_token()



        response = upload_file(

            self.filepath,

            token,

            metadata

        )



        if "error" not in response:


            messagebox.showinfo(

                "Correcto",

                response.get(

                    "message",

                    "Estudio enviado correctamente"

                )

            )


            self.root.destroy()



        else:


            messagebox.showerror(

                "Error",

                response.get(

                    "message",

                    "Error al subir estudio"

                )

            )