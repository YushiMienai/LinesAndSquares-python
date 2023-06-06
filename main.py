import tkinter as tk
from start_screen import StartScreen
from server_screen import ServerScreen
from client_screen import ClientScreen
from game_screen import GameScreen


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Lines and Squares")
        self.geometry("400x500")
        self.resizable(False, False)

        # Создаем экраны
        self.screens = {}

        # Показываем начальный экран
        self.show_screen(StartScreen)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.destroy_all_screens()
        self.destroy()

    def show_screen(self, screen_class, **kwargs):
        self.destroy_all_screens()
        screen = screen_class(self, **kwargs)
        screen.pack(fill="both", expand=True)
        screen_name = screen_class.__name__.lower()
        self.screens[screen_name] = screen

    def destroy_all_screens(self):
        for screen in self.screens.values():
            screen.destroy()
        self.screens = {}

    def show_start_screen(self):
        self.show_screen(StartScreen)

    def show_game_screen(self):
        self.show_screen(GameScreen)

    def show_client_screen(self):
        # Создаем экран подключения клиента и показываем его
        def on_server_found(server_socket):
            self.show_screen(GameScreen, socket=server_socket, active_player=1)

        self.show_screen(ClientScreen, on_server_found=on_server_found)

    def show_server_screen(self):
        # Создаем экран сервера и показываем его
        def on_client_connected(client_socket):
            self.show_screen(GameScreen, socket=client_socket, active_player=0)

        self.show_screen(ServerScreen, on_client_connected=on_client_connected)


if __name__ == "__main__":
    app = App()
    app.mainloop()
