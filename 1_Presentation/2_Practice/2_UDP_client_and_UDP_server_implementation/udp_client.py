import argparse
import socket
from loguru import logger
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='UDP Client')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Server IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000,
                        help='Server port (default: 5000)')
    parser.add_argument('--message', type=str, required=True,
                        help='Message to send')
    parser.add_argument('--log', type=str,
                        default='1_Presentation/2_Practice/2_UDP_client_and_' +
                        'UDP_server_implementation/udp_client.log',
                        help='Log file path (default: 1_Presentation/2_Pract' +
                        'ice/2_UDP_client_and_UDP_server_implementation/udp_' +
                        'client.log)')
    parser.add_argument('--timeout', type=float, default=5.0,
                        help='Response timeout in seconds (default: 5.0)')
    parser.add_argument('--retry', type=int, default=3,
                        help='Max retry attempts (default: 3)')
    return parser.parse_args()


def setup_logging(log_file):
    logger.remove()
    logger.add(sys.stdout, level="INFO",
               format="<blue>{time:YYYY-MM-DD HH:mm:ss}</blue> | <level>" +
               "{level}</level> | {message}")
    logger.add(log_file, level="DEBUG", rotation="5 MB", compression="zip")
    return logger


def run_client(host, port, message, timeout, retry, log):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(timeout)
        server_address = (host, port)

        for attempt in range(1, retry + 1):
            try:
                # Отправка сообщения
                client_socket.sendto(message.encode('utf-8'), server_address)
                log.debug(f"Attempt {attempt}: Sent message to {host}:{port}")

                # Получение ответа
                response, _ = client_socket.recvfrom(1024)
                log.info(f"Server response: {response.decode('utf-8')}")
                return

            except socket.timeout:
                log.warning(f"Attempt {attempt}: Server response timeout")
            except Exception as e:
                log.error(f"Attempt {attempt}: Connection error - {str(e)}")
                break

        log.error("All retry attempts failed. No response from server.")


if __name__ == '__main__':
    args = parse_args()
    log = setup_logging(args.log)
    run_client(args.host, args.port, args.message, args.timeout, args.retry,
               log)
