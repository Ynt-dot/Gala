import argparse
import socket
from loguru import logger
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='UDP Server')
    parser.add_argument('--host', type=str, default='127.0.0.1',
                        help='Server IP address (default: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=5000,
                        help='Server port (default: 5000)')
    parser.add_argument('--log', type=str,
                        default='1_Presentation/2_Practice/2_UDP_client_and_' +
                        'UDP_server_implementation/udp_server.log',
                        help='Log file path (default: 1_Presentation/2_Pract' +
                        'ice/2_UDP_client_and_UDP_server_implementation/udp_' +
                        'server.log)')
    parser.add_argument('--buffer', type=int, default=1024,
                        help='Buffer size in bytes (default: 1024)')
    return parser.parse_args()


def setup_logging(log_file):
    logger.remove()
    logger.add(sys.stdout, level="INFO",
               format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>" +
               "{level}</level> | {message}")
    logger.add(log_file, level="DEBUG", rotation="10 MB", compression="zip")
    return logger


def start_server(host, port, buffer_size, log):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))
        log.info(
            f"UDP Server started on {host}:{port}. Waiting for datagrams...")

        try:
            while True:
                data, addr = server_socket.recvfrom(buffer_size)
                message = data.decode('utf-8')
                log.info(f"Received from {addr[0]}:{addr[1]}: {message}")

                # Эхо-ответ
                response = f"ACK: {message}"
                server_socket.sendto(response.encode('utf-8'), addr)
                log.debug(f"Sent response to {addr[0]}:{addr[1]}")
        except KeyboardInterrupt:
            log.info("Server shutdown by administrator")
        except Exception as e:
            log.error(f"Unexpected error: {str(e)}")


if __name__ == '__main__':
    args = parse_args()
    log = setup_logging(args.log)
    start_server(args.host, args.port, args.buffer, log)
