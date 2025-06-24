# Этот код реализует TCP-клиента, который подключается к серверу, отправляет
# сообщение и получает ответ. Разберём его по компонентам:
# 1. Импорт модулей
import argparse  # Для обработки аргументов командной строки
import socket  # Для сетевого взаимодействия
from loguru import logger  # Для продвинутого логирования
import sys  # Для работы с системными потоками


def parse_args():  # 2. Парсинг аргументов
    parser = argparse.ArgumentParser(description='TCP Client')
    # IP сервера (по умолчанию localhost)
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Server IP address (default: 127.0.0.1)')
    # Порт сервера (по умолчанию 5000)
    parser.add_argument('--port', type=int, default=5000,
                        help='Server port (default: 5000)')
    # Обязательное сообщение для отправки
    parser.add_argument('--message', type=str, required=True,
                        help='Message to send')
    # Путь к файлу логов (по умолчанию 'client.log')
    parser.add_argument('--log', type=str,
                        default='2_Explanation/2_Practice/1_implementation_' +
                        'of_TCP_client_and_TCP_server/client.log',
                        help='Log file path (default: 2_Explanation/2_Pract' +
                        'ice/1_implementation_of_TCP_client_and_TCP_server/c' +
                        'lient.log)')
    return parser.parse_args()


def setup_logging(log_file):  # . Настройка логирования
    logger.remove()
    # Консольный вывод (синие метки времени, только INFO+)
    logger.add(sys.stdout, level="INFO", format="<blue>{time}</blue> | <level>\
               {level}</level> | {message}")
    # Файловый вывод (все уровни, ротация при 5MB)
    # Автоматическое сжатие старых логов (zip)
    logger.add(log_file, level="DEBUG", rotation="5 MB", compression="zip")
    return logger


def run_client(host, port, message, log):  # 4. Основная логика клиента
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Подключение к серверу
            client_socket.connect((host, port))
            log.info(f"Connected to server {host}:{port}")

            # Отправка сообщения
            # Кодирование сообщения в UTF-8
            # Использование sendall() для гарантированной отправки
            client_socket.sendall(message.encode('utf-8'))
            # Логирование отправки (уровень DEBUG)
            log.debug(f"Sent message: {message}")

            # Получение ответа
            # Ожидание данных (буфер 1024 байта)
            response = client_socket.recv(1024)
            # Декодирование из UTF-8
            # Логирование ответа (уровень INFO)
            log.info(f"Server response: {response.decode('utf-8')}")

        except ConnectionRefusedError:  # Сервер недоступен
            log.error("Server is not available")
        except Exception as e:  # Другие сетевые ошибки
            log.error(f"Connection error: {str(e)}")


if __name__ == '__main__':  # 5. Точка входа
    args = parse_args()
    log = setup_logging(args.log)
    run_client(args.host, args.port, args.message, log)


# Особенности реализации
# 1. Однократное взаимодействие:
#       Клиент отправляет одно сообщение и получает один ответ
#       После получения ответа соединение закрывается
# 2. Безопасное управление ресурсами:
#       Использование with для автоматического закрытия сокета
#       Гарантированное освобождение ресурсов даже при ошибках
# 3. Комплексная обработка ошибок:
#       Специальная обработка отказа подключения
#       Перехват любых исключений сети
# 4. Гибкая конфигурация:
#       Все параметры настраиваются через аргументы командной строки
#       Обязательное сообщение для отправки
