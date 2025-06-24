import argparse
import socket
from loguru import logger
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='TCP server')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Server IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000,
                        help='Server port (default: 5000)')
    parser.add_argument('--log', type=str,
                        default='3_Practice/1_implementation_of_TCP_client_a' +
                        'nd_TCP_server/server.log',
                        help='Log file path (default: 3_Practice/1_implement' +
                        'ation_of_TCP_client_and_TCP_server/server.log)')
    return parser.parse_args()


def setup_logging(log_file):
    logger.remove()
    logger.add(sys.stdout, level="INFO",
               format="<green>{time}</green> | <level>{level}</level> | " +
               "{message}")
    logger.add(log_file, level="DEBUG", rotation="10 MB", compression="zip")
    return logger


def start_server(host, port, log):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen(5)

        log.info(f"Server started on {host}:{port}. Waiting for connections..."
                 )

        try:
            while True:
                client_socket, addr = server_socket.accept()
                log.info(f"New connection from {addr[0]}:{addr[1]}")

                with client_socket:
                    while True:
                        data = client_socket.recv(1024)
                        if not data:
                            log.debug(f"Client {addr} disconnected")
                            break

                        message = data.decode('utf-8')
                        log.info(f"Received from {addr}:{message}")

                        response = f"ECHO: {message}"
                        client_socket.sendall(response.encode('utf-8'))
                        log.debug(f"Sent responce to {addr}")
        except KeyboardInterrupt:
            log.info("Server shutdown by administrator")


if __name__ == '__main__':
    args = parse_args()
    log = setup_logging(args.log)
    start_server(args.host, args.port, log)
