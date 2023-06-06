import threading
import tkinter as tk
import socket
from classes import Config


class ServerScreen(tk.Frame):
    def __init__(self, parent, on_client_connected):
        super().__init__(parent)

        self.app = parent.winfo_toplevel()  # получаем экземпляр класса App
        self.on_client_connected = on_client_connected
        hostname = socket.gethostname()

        ip_address = Config.get('server', 'ip_address') or socket.gethostbyname(hostname)
        port = Config.get('server', 'port', 'int') or 5050

        # Создаем сокет сервер и ждем подключения клиента
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((ip_address, port))
        self.server_socket.listen(1)

        self.thread = threading.Thread(target=self.wait_for_client)
        self.thread.start()

        tk.Label(self, text="Ждем подключения клиента", font=("Times New Roman", 14)).pack(padx=5, pady=10)
        tk.Label(self, text="по адресу {}:{}".format(ip_address, port), font=("Times New Roman", 14)).pack(padx=5,
                                                                                                           pady=1)

        # Создание кнопки "Назад"
        back_button = tk.Button(self, text="Back", font=("Times New Roman", 14), command=self.back_to_start_screen)
        back_button.place(relx=0.65, rely=0.2)

    def on_close(self):
        self.server_socket.close()
        self.thread.join()
        self.quit()

    def wait_for_client(self):
        try:
            client_socket, address = self.server_socket.accept()
        except OSError:
            return

        tk.Label(self, text=f"Client {address} has connected!", font=("Times New Roman", 14)).pack(padx=10, pady=10)
        self.on_client_connected(client_socket)

    def back_to_start_screen(self):
        self.server_socket.close()
        self.app.show_start_screen()
