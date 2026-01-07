import logging
import time
import socket
from flask import Flask, jsonify

app = Flask(__name__)

# --- Налаштування журналювання ---
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# --- Глобальні змінні для /status ---
start_time = time.time()
request_count = 0

# --- Функція для відправки на StatsD ---
def send_to_statsd(message):
    try:
        UDP_IP = "127.0.0.1"
        UDP_PORT = 8125
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode('utf-8'), (UDP_IP, UDP_PORT))
    except Exception as e:
        logging.error(f"Не вдалося відправити дані на StatsD: {e}")

# Мідлвар для підрахунку запитів
@app.before_request
def count_requests():
    global request_count
    request_count += 1

@app.route('/')
def index():
    logging.info("Відвідано головну сторінку")
    return "Сервіс працює"

@app.route('/error')
def cause_error():
    logging.warning("Користувач зайшов на небезпечний маршрут /error")
    try:
        result = 1 / 0  # Свідома помилка
    except Exception as e:
        logging.exception("Виявлено критичну помилку!")
        send_to_statsd("error.count:1|c")
        return "Сталася помилка, дані відправлено в систему моніторингу", 500

@app.route('/status')
def status():
    uptime = round(time.time() - start_time, 2)
    logging.info(f"Запит статусу: uptime={uptime}, requests={request_count}")
    return jsonify({
        "status": "online",
        "uptime_seconds": uptime,
        "total_requests": request_count
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)