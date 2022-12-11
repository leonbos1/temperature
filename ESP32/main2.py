from machine import Pin, ADC, deepsleep
import time
import network
import urequests
import json
import dht

def main():
    connect()
    dht22 = dht.DHT22(Pin(22))
    dht22.measure()
    temperature = dht22.temperature()
    humidity = dht22.humidity()
    
    print("Temperature", temperature, " , afgerond", int(round(temperature)))
    print("Humidity", humidity, " , afgerond", int(round(humidity)))
    send_temp(round(temperature,2), humidity)

    
def send_temp(temperature, humidity):
    url = "http://ronleon.nl:5000/"
 
    data = {
        'sensor':3,
        'degrees':temperature,
        'humidity':humidity
        }
    json_object = json.dumps(data)
    
    request = urequests.post(url, data=json_object)
    
    request.close()

if __name__ == "__main__":
    try:
        main()
        deepsleep(60000)
    except Exception as e:
        print(e)
        deepsleep(1000)





