import tkinter as tk
import socket
from classes import Config


class ClientScreen(tk.Frame):
    def __init__(self, parent, on_server_found):
        super().__init__(parent)

        self.app = parent.winfo_toplevel()  # получаем экземпляр класса App
        self.on_server_found = on_server_found

        self.ip_address = Config.get('client', 'ip_address')
        self.port = Config.get('client', 'port')

        # Создание поля для ввода IP-адреса
        ip_label = tk.Label(self, text="IP-адрес")
        ip_label.place(relx=0.25, rely=0.5, anchor="e")
        self.ip_entry = tk.Entry(self)
        self.ip_entry.place(relx=0.3, rely=0.5, anchor="w")

        # Создание поля для ввода порта
        port_label = tk.Label(self, text="Порт")
        port_label.place(relx=0.25, rely=0.55, anchor="e")
        self.port_entry = tk.Entry(self)
        self.port_entry.place(relx=0.3, rely=0.55, anchor="w")

        self.ip_entry.insert(0, self.ip_address)
        self.port_entry.insert(0, self.port)

        # Создание кнопки "Назад"
        back_button = tk.Button(self, text="Back", font=("Times New Roman", 14), command=self.back_to_start_screen)
        back_button.place(relx=0.25, rely=0.75, anchor="w")

        # Создание кнопки "Подключиться"
        connect_button = tk.Button(self, text="Connect", font=("Times New Roman", 14), command=self.connect_action)
        connect_button.place(relx=0.5, rely=0.75, anchor="center")

    def connect_action(self):
        ip = self.ip_entry.get()
        port = int(self.port_entry.get())

        if self.ip_address == '':
            Config.set('client', 'ip_address', ip)

        if self.port == '':
            Config.set('client', 'port', port)

        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((ip, port))

            self.on_server_found(server_socket)

        except ConnectionRefusedError:
            print("Server is not available!")

    def back_to_start_screen(self):
        self.pack_forget()
        self.app.show_start_screen()
