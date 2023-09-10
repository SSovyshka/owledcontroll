import _thread
import socket
import json
import time
import network
import machine
from effects import *
from lets import *

led = machine.Pin('LED', machine.Pin.OUT)
led.off()

# ssid = 'OnePlus 8T'
# password = '546682743'
ssid = 'DIR-300NRU'
password = '963852741'
port = 61024

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)
while not wifi.isconnected():
    pass

led.on()
ip_address = wifi.ifconfig()[0]
print(f"IP-адрес устройства: {ip_address}:{port}")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', port))
server.listen(1)

# effect_name = None    # Переменная для хранения названия еффекта
# effect_thread = False # Переменная для ожидания завершения потока


def start_effect():
    global effect_name, effect_thread
    
    effect_on_start = effect_name
    effect_thread = True  # Устанавливаем флаг в True перед началом работы потока
    time.sleep(0.2)
    
    while True:
        if effect_name != effect_on_start:
            effect_thread = False  # По завершении работы потока устанавливаем флаг в False
            break
        
        print(effect_on_start)
        
        try:
            exec(f"{effect_on_start}()")
        except Exception as e:
            print("Effect not found and thread will stop")
            effect_thread = False
            break
        
        
def start_server():
    global effect_name, effect_thread
    print("Server start")
    while True:
        client, address = server.accept()

        data = client.recv(2048).decode()
        
        json_data = json.loads(data)
        effect_name = json_data['effect']
        
        
        while effect_thread:  # Ожидаем, пока effect_thread станет False. Таким образом, ждем завершения предыдущего потока.
            pass
        
        _thread.start_new_thread(start_effect, ())  # Запускаем новый поток для обработки эффекта
        
        client.close()

if __name__ == "__main__":
    start_server()
