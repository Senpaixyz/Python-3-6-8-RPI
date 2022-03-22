from scapy.all import *
from scapy.sendrecv import sniff
import pyrebase
from helper.FlowRecoder import get_data, gen_json
import time
# net start npcap  <- if windows user to enable monitor mode

### THIS PYTHON FILE SHOULD INSTALL INSIDE RPI


config = {
    "apiKey": "AIzaSyBym004axtB-2cyCO3a0_F1kDaGgaz0h_w",
    "authDomain": "anomaly-detection-1bd55.firebaseapp.com",
    "projectId": "anomaly-detection-1bd55",
    "databaseURL":"https://anomaly-detection-1bd55-default-rtdb.firebaseio.com/",
    "storageBucket": "anomaly-detection-1bd55.appspot.com",
    "messagingSenderId": "164779489599",
    "appId": "1:164779489599:web:503ca5bedb4beb5cb13b8a"
};

firebase = pyrebase.initialize_app(config)

storage = firebase.storage()
database = firebase.database()


def main():
    sleep_interval = 1
    print("Setting up device...");
    while True:
        captured_buffer = []
        isActive = eval(database.child("Network-Active").get().val())
        database.child("Network-Connection").set("Connected")
        if isActive == True:
            for pkt in sniff(iface=conf.iface, count=40):
                captured_buffer.append(pkt)
            data = get_data(captured_buffer)
            data = gen_json(data)
            database.child("Network-Traffic").set(data)
            database.child("Network-Active").set("True")
            print(captured_buffer)
        time.sleep(sleep_interval)



if __name__ == '__main__':
    try:
        main()
    finally:
        print("Terminating the program")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
