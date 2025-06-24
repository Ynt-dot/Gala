import argparse
import socket
from loguru import logger
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='TCP_client')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Server IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000,
                        help='Server port (default: 5000)')
    parser.add_argument('--message', type=str, required=True,
                        help='Message to send')
    parser.add_argument('--log', type=str,
                        default='3_Practice/1_implementation_of_TCP_client_a' +
                        'nd_TCP_server/client.log',
                        help='Log file path (default: 3_Practice/1_implement' +
                        'ation_of_TCP_client_and_TCP_server/client.log)')
    return parser.parse_args()


def setup_logging(log_file):
    logger.remove()
    logger.add(sys.stdout, level="INFO",
               format="<blue>{time}</blue> | <level>{level}</level> | " +
               "{message}")
    logger.add(log_file, level="DEBUG", rotation="5 MB", compression="zip")
    return logger


def run_client(host, port, message, log):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((host, port))
            log.info(f"Connected to server {host}:{port}")

            client_socket.sendall(message.encode('utf-8'))
            log.debug(f"Sent message {message}")

            response = client_socket.recv(1024)
            log.info(f"Server response: {response}")
        except ConnectionRefusedError:
            log.error("Server is not available")
        except Exception as e:
            log.error(f"Connection error: {e}")


if __name__ == '__main__':
    args = parse_args()
    log = setup_logging(args.log)
    run_client(args.host, args.port, args.message, log)
