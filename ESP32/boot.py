def connect():
    ssid = "Covid19 5G Aluistermast"
    password = "Kaaskaas123"
    
    ssid = "fam.bos"
    password = "Stroopwafels1"
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(0.2)
            print('.',end=".")
    print("network config:", wlan.ifconfig())
