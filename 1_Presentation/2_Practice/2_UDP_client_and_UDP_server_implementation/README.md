Запускать из папки Gala, предварительно выполнить указания из README.md в Gala.
Сервер:
python 1_Presentation\2_Practice\2_UDP_client_and_UDP_server_implementation\udp_server.py --host 0.0.0.0 --port 5001 --log 1_Presentation/2_Practice/2_UDP_client_and_UDP_server_implementation/udp_server_app.log --buffer 2048
Клиент (отдельный терминал):
python 1_Presentation\2_Practice\2_UDP_client_and_UDP_server_implementation\udp_client.py --host 127.0.0.1 --port 5001 --message "Hello UDP Server!" --log 1_Presentation/2_Practice/2_UDP_client_and_UDP_server_implementation/udp_client_app.log --timeout 2.0 --retry 5