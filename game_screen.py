import json
import threading
import tkinter as tk

from classes import Coordinate, Line, Square, Player


class GameScreen(tk.Frame):
    def __init__(self, parent, socket=None, active_player=0):
        super().__init__(parent)

        self.players = [Player("blue"), Player("red")]

        self.parent = parent
        self.app = parent.winfo_toplevel()  # получаем экземпляр класса App
        self.active_player = active_player
        self.socket = socket

        # Создаем холст для рисования
        self.canvas = tk.Canvas(self, width=400, height=500)
        self.canvas.pack()
        self.score_text = self.canvas.create_text(20, 360, text="Score: 0 - 0", font=("Times New Roman", 14),
                                                  anchor='nw')
        self.player_text = self.canvas.create_text(20, 380, text=f"Current player: {self.get_active_player().color}",
                                                   font=("Times New Roman", 14), anchor='nw')

        # Создание кнопки "Назад"
        back_button = tk.Button(self, text="Back", font=("Times New Roman", 14), command=self.back_to_start_screen)
        back_button.place(relx=0.73, rely=0.75, anchor="w")

        # Создаем отдельный поток для чтения данных из сокета
        if socket is not None:
            self.socket_thread = threading.Thread(target=self.receive_data_from_socket)
            self.socket_thread.daemon = True
            self.socket_thread.start()

        # Создаем линии и квадраты
        self.horizontal_lines = []
        for i in range(0, 10):
            for j in range(0, 9):
                x = j * 36 + 20
                y = i * 36 + 20
                start = Coordinate(x, y)
                end = Coordinate(x + 36, y)
                line = Line(start, end)
                self.horizontal_lines.append(line)

        self.vertical_lines = []
        for i in range(0, 9):
            for j in range(0, 10):
                x = j * 36 + 20
                y = i * 36 + 20
                start = Coordinate(x, y)
                end = Coordinate(x, y + 36)
                line = Line(start, end)
                self.vertical_lines.append(line)

        self.squares = []
        for i in range(0, 9):
            for j in range(0, 9):
                top = self.horizontal_lines[i * 9 + j]
                bottom = self.horizontal_lines[(i + 1) * 9 + j]
                left = self.vertical_lines[i * 10 + j]
                right = self.vertical_lines[i * 10 + j + 1]
                square = Square(top, right, bottom, left)
                self.squares.append(square)

        # Рисуем линии на холсте
        for line in self.horizontal_lines + self.vertical_lines:
            self.draw_line(line)

    def receive_data_from_socket(self):
        while True:
            try:
                # Ожидаем ответ от другого игрока
                data = self.socket.recv(1024)

                if not data:
                    # Соединение было закрыто
                    break

                # Распаковываем полученные данные
                message = json.loads(data.decode())

                self.canvas.itemconfig(message['line_id'], width=2, fill='black')
                line = self.find_line_by_id(message['line_id'])
                line.isSelected = True
                for square in self.squares:
                    if square.contains_line(line):
                        if square.is_all_selected():
                            self.add_square(square)

                if message['switch_active_player']:
                    self.switch_active_player()

            except ConnectionResetError:
                # Соединение было неожиданно разорвано
                self.back_to_start_screen()
                break

    def draw_line(self, line):
        if line is None:
            return
        color = "black" if line.isSelected else "lightgray"
        width = 2 if line.isSelected else 1
        line_id = self.canvas.create_line(line.start.x, line.start.y, line.end.x, line.end.y, width=width, fill=color)
        line.set_id(line_id)
        self.canvas.tag_bind(line_id, '<ButtonPress-1>', lambda event: self.on_line_click(line_id))

    def find_line_by_id(self, line_id):
        for line in self.horizontal_lines + self.vertical_lines:
            if line.id == line_id:
                return line

    def add_square(self, square):
        self.canvas.create_rectangle(
            square.top.start.x + 2,
            square.top.start.y + 2,
            square.bottom.end.x - 3,
            square.bottom.end.y - 3,
            fill=self.get_active_player().color)
        self.get_active_player().num_cells += 1
        score_text_value = f"Score: {self.players[0].num_cells} - {self.players[1].num_cells}"
        self.canvas.itemconfig(self.score_text, text=score_text_value)
        self.check_win_condition()

    def switch_active_player(self):
        self.active_player = 1 if self.active_player == 0 else 0
        player_text_value = f"Current player: {self.get_active_player().color}"
        self.canvas.itemconfig(self.player_text, text=player_text_value)

    def on_line_click(self, line_id):
        line = self.find_line_by_id(line_id)
        if line.isSelected or (self.socket is not None and self.active_player == 1):
            return
        line.isSelected = True
        self.canvas.itemconfig(line_id, width=2, fill='black')

        need_switch = True
        for square in self.squares:
            if square.contains_line(line):
                if square.is_all_selected():
                    self.add_square(square)
                    need_switch = False

        if need_switch:
            self.switch_active_player()

        if self.socket:
            self.socket.send(json.dumps({'switch_active_player': need_switch, 'line_id': line_id}).encode())

    def check_win_condition(self):
        if Player.squares_owned(players=self.players) == len(self.squares):
            message = 'Draw!'

            if self.players[0].num_cells > self.players[1].num_cells:
                message = f'{self.players[0].color.capitalize()} player wins!' if self.socket is None else 'You win!'
            elif self.players[0].num_cells < self.players[1].num_cells:
                message = f'{self.players[1].color.capitalize()} player wins' if self.socket is None else 'You lose!'

            # Создаем Label с текстом сообщения и задаем его расположение на холсте
            message_label = tk.Label(self.canvas, text=message, font=("Times New Roman", 20), bg='white')
            message_label.place(relx=0.45, rely=0.5, anchor="center")

    def get_active_player(self):
        return self.players[self.active_player]

    def back_to_start_screen(self):
        self.app.show_start_screen()

