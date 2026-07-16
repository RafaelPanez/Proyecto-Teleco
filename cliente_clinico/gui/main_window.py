# gui/main_window.py

import customtkinter as ctk

from tkinter import messagebox

from utils.auth import get_user, clear_session

from gui.upload_window import UploadWindow
from gui.study_window import StudyWindow
from utils.auth import get_token


class MainWindow:

    def __init__(self, root):

        self.root = root

        self.root.title("Sistema - Panel principal")
        self.root.geometry("500x400")

        self.create_widgets()


    def create_widgets(self):

        username = get_user()


        self.title_label = ctk.CTkLabel(
            self.root,
            text=f"Bienvenido {username}",
            font=("Arial", 22)
        )

        self.title_label.pack(
            pady=30
        )


        self.upload_button = ctk.CTkButton(
            self.root,
            text="Subir estudio",
            command=self.open_upload
        )

        self.upload_button.pack(
            pady=10,
            padx=60,
            fill="x"
        )


        self.study_button = ctk.CTkButton(
            self.root,
            text="Consultar estudios",
            command=self.open_studies
        )
        self.delete_button = ctk.CTkButton(
            self.root,
            text="Eliminar estudio",
            command=self.open_delete
        )

        self.delete_button.pack(
            pady=10
        )
        self.study_button.pack(
            pady=10,
            padx=60,
            fill="x"
        )


        self.logout_button = ctk.CTkButton(
            self.root,
            text="Cerrar sesión",
            command=self.logout
        )

        self.logout_button.pack(
            pady=30,
            padx=60,
            fill="x"
        )

    def open_delete(self):

        import customtkinter as ctk

        from gui.delete_window import DeleteWindow


        window = ctk.CTkToplevel(
            self.root
        )


        DeleteWindow(
            window
        )
        
    def open_upload(self):

        upload_window = ctk.CTkToplevel(
            self.root
        )

        UploadWindow(
            upload_window
        )


    def open_studies(self):

        study_window = ctk.CTkToplevel(
            self.root
        )

        StudyWindow(
            study_window
        )


    def logout(self):

        clear_session()

        self.root.quit()
        self.root.destroy()