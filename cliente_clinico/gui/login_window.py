# gui/login_window.py

import customtkinter as ctk
from tkinter import messagebox

from api import login
from utils.auth import save_session
from utils.validators import validate_login
from gui.main_window import MainWindow


class LoginWindow:

    def __init__(self, root):

        self.root = root

        self.root.title("Sistema - Login")
        self.root.geometry("400x350")

        self.create_widgets()


    def create_widgets(self):

        self.title_label = ctk.CTkLabel(
            self.root,
            text="Inicio de sesión",
            font=("Arial", 24)
        )

        self.title_label.pack(
            pady=20
        )


        self.username_entry = ctk.CTkEntry(
            self.root,
            placeholder_text="Usuario"
        )

        self.username_entry.pack(
            pady=10,
            padx=40,
            fill="x"
        )


        self.password_entry = ctk.CTkEntry(
            self.root,
            placeholder_text="Contraseña",
            show="*"
        )

        self.password_entry.pack(
            pady=10,
            padx=40,
            fill="x"
        )


        self.login_button = ctk.CTkButton(
            self.root,
            text="Ingresar",
            command=self.login_user
        )

        self.login_button.pack(
            pady=20
        )


    def login_user(self):

        username = self.username_entry.get()
        password = self.password_entry.get()


        valid, message = validate_login(
            username,
            password
        )

        if not valid:
            messagebox.showwarning(
                "Datos incompletos",
                message
            )
            return


        response = login(
            username,
            password
        )


        if "access_token" in response:

            save_session(
                response["access_token"],
                username
            )


            messagebox.showinfo(
                "Correcto",
                "Inicio de sesión exitoso"
            )


            self.open_main_window()


        else:

            messagebox.showerror(
                "Error",
                response.get(
                    "message",
                    "Usuario o contraseña incorrectos"
                )
            )


    def open_main_window(self):

        self.root.destroy()

        new_root = ctk.CTk()

        MainWindow(
            new_root
        )

        new_root.mainloop()