import socket

# Налаштування UDP сервера
UDP_IP = "127.0.0.1"
UDP_PORT = 8125

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

print(f"Імітаційний StatsD сервер запущено на {UDP_IP}:{UDP_PORT}")

while True:
    data, addr = sock.recvfrom(1024) # Буфер 1024 байти
    print(f"Отримано метрику: {data.decode('utf-8')}")