import tkinter as tk


class StartScreen(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        app = parent.winfo_toplevel()
        show_game_screen = app.show_game_screen
        show_client_screen = app.show_client_screen
        show_server_screen = app.show_server_screen

        # Создаем кнопки "Хост" и "Сервер" и привязываем к ней функцию show_game_screen
        server_button = tk.Button(self, text="Local game", font=("Times New Roman", 14),
                                  command=show_game_screen)
        server_button.place(relx=0.5, rely=0.3, anchor="center")
        server_button = tk.Button(self, text="Host", font=("Times New Roman", 14), command=show_server_screen)
        server_button.place(relx=0.5, rely=0.4, anchor="center")
        client_button = tk.Button(self, text="Client", font=("Times New Roman", 14), command=show_client_screen)
        client_button.place(relx=0.5, rely=0.5, anchor="center")
