from machine import Pin, ADC, deepsleep
import time
import network
import urequests
import json

def main():
    connect()
    
    adc = ADC(Pin(32))
    adc.width(ADC.WIDTH_10BIT)
    adc.atten(ADC.ATTN_6DB)

        
    temperature = adc.read()
    temperature = temperature / 1023
    temperature = temperature * 2
    temperature = temperature - 0.5
    temperature = temperature * 100
    print("Temperature", temperature, " , afgerond", int(round(temperature)))
    send_temp(round(temperature,2))

    
def send_temp(temperature):
    url = "http://ronleon.nl:5000/"
 
    data = {
        'sensor':2,
        'degrees':temperature
        }
    json_object = json.dumps(data)
    
    request = urequests.post(url, data=json_object)
    
    request.close()

if __name__ == "__main__":
    try:
        main()
        deepsleep(60000)
    except:
        deepsleep(1000)




