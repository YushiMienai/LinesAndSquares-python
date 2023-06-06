import socket


def start_server():
    # Создаем сокет и ждем подключений
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Получаем имя хоста
    hostname = socket.gethostname()

    # Получаем IP-адрес хоста
    ip_address = socket.gethostbyname(hostname)
    server_socket.bind((ip_address, 8000))
    #server_socket.bind(('169.254.200.1', 8000))
    server_socket.listen()
    print('Сервер запущен, ожидание подключений...')
    port = server_socket.getsockname()[1]
    print(f'Для подключения клиента используйте адрес {ip_address} и порт {port}')

    # Принимаем подключения и читаем данные от клиентов
    while True:
        client_socket, address = server_socket.accept()
        print(f'Установлено соединение с {address}')
        data = client_socket.recv(1024).decode()
        print(f'Получены данные: {data}')

        # Отправляем ответ клиенту
        response_data = f'Сервер получил сообщение: {data}'
        client_socket.send(response_data.encode())

        # Закрываем соединение с клиентом
        client_socket.close()


def start_client():
    # Получаем адрес сервера и порт
    server_address = input('Введите адрес сервера: ')
    server_port = int(input('Введите порт сервера: '))

    # Подключаемся к серверу и отправляем данные
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_address, server_port))
    message = input('Введите сообщение: ')
    client_socket.send(message.encode())

    # Получаем ответ от сервера и выводим его
    response = client_socket.recv(1024).decode()
    print('Ответ от сервера:', response)

    # Закрываем соединение с сервером
    client_socket.close()


"""def main():
    # Показываем меню выбора режима работы
    print('1. Сервер')
    print('2. Клиент')
    choice = int(input('Выберите режим работы: '))

    # Запускаем сервер или клиент в зависимости от выбора пользователя
    if choice == 1:
        start_server()
    elif choice == 2:
        start_client()
    else:
        print('Ошибка: неверный выбор')

if __name__ == '__main__':
    main()"""
