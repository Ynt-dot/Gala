# Этот код представляет собой реализацию TCP-сервера с эхо-функционалом,
# логированием и обработкой аргументов командной строки. Разберём его детально:
# 1. Импорт модулей
import argparse  # Для обработки аргументов командной строки
import socket  # Для сетевых операций (реализация TCP-сервера)
from loguru import logger  # Мощный инструмент логирования
import sys  # Для взаимодействия с системой (здесь - вывод в stdout)


def parse_args():  # 2. Обработка аргументов командной строки
    parser = argparse.ArgumentParser(description='TCP Server')
    # IP-адрес сервера (по умолчанию localhost)
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Server IP address (default: 127.0.0.1)')
    # Порт сервера (по умолчанию 5000)
    parser.add_argument('--port', type=int, default=5000,
                        help='Server port (default: 5000)')
    # Путь к файлу логов (по умолчанию 'server.log')
    parser.add_argument('--log', type=str,
                        default='2_Explanation/2_Practice/1_implementation_' +
                        'of_TCP_client_and_TCP_server/server.log',
                        help='Log file path (default: 2_Explanation/2_Pract' +
                        'ice/1_implementation_of_TCP_client_and_TCP_server/s' +
                        'erver.log)')
    return parser.parse_args()


def setup_logging(log_file):  # 3. Настройка логирования
    logger.remove()  # Удаление стандартных обработчиков
    # Два обработчика: консоль (только важные сообщения) и файл (все сообщения)
    # Логи в консоль (только INFO и выше)
    logger.add(sys.stdout, level="INFO",
               format="<green>{time}</green> | <level>{level}</level> | " +
               "{message}")
    # Логи в файл (все уровни, ротация при 10MB)
    # Создание нового файла при достижении 10MB
    # Архивация старых логов
    logger.add(log_file, level="DEBUG", rotation="10 MB", compression="zip")
    return logger


def start_server(host, port, log):  # 4. Основная логика сервера
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # socket.SO_REUSEADDR Позволяет повторно использовать адрес после
        # перезапуска
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)  # Максимум 5 подключений в очереди

        log.info(f"Server started on {host}:{port}. Waiting for connections..."
                 )

        try:
            while True:  # Бесконечный цикл принятия подключений
                # accept() блокирует выполнение до нового подключения
                client_socket, addr = server_socket.accept()
                log.info(f"New connection from {addr[0]}:{addr[1]}")

                with client_socket:
                    while True:
                        # Чтение данных порциями по 1024 байта
                        data = client_socket.recv(1024)
                        if not data:  # Пустые данные = отключение клиента
                            log.debug(f"Client {addr} disconnected")
                            break

                        # Декодирование байтов в строку (UTF-8)
                        message = data.decode('utf-8')
                        log.info(f"Received from {addr}: {message}")

                        # Эхо-ответ
                        # Формирование эхо-ответа с префиксом "ECHO: "
                        response = f"ECHO: {message}"
                        # Отправка ответа клиенту
                        client_socket.sendall(response.encode('utf-8'))
                        log.debug(f"Sent response to {addr}")
        # Обработка Ctrl+C для корректного завершения
        except KeyboardInterrupt:  # Не работает
            log.info("Server shutdown by administrator")


if __name__ == '__main__':  # 5. Точка входа
    args = parse_args()  # Парсинг аргументов
    log = setup_logging(args.log)  # Инициализация логирования
    start_server(args.host, args.port, log)  # Запуск сервера


# Ключевые особенности:
# 1. Эхо-сервер: Отправляет полученные сообщения обратно клиенту
# 2. Контекстные менеджеры (with):
#       Автоматическое закрытие сокетов
#       Гарантия освобождения ресурсов
# 3. Многоуровневое логирование:
#       Консоль: только INFO и выше
#       Файл: все сообщения с ротацией
# 4. Обработка прерываний: Корректное завершение по Ctrl+C
# 5. Гибкая конфигурация через аргументы командной строки
