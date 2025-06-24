Запускать из папки Gala, предварительно выполнить указания из README.md в Gala.
Сервер:
python 2_Explanation\2_Practice\1_implementation_of_TCP_client_and_TCP_server\tcp_server.py --host 0.0.0.0 --port 5001 --log 2_Explanation/2_Practice/1_implementation_of_TCP_client_and_TCP_server/server_app.log
Клиент (отдельный терминал):
python 2_Explanation\2_Practice\1_implementation_of_TCP_client_and_TCP_server\tcp_client.py --host 127.0.0.1 --port 5001 --message "Hello TCP Server!" --log 2_Explanation/2_Practice/1_implementation_of_TCP_client_and_TCP_server/client_app.log