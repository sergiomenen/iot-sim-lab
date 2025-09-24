# src/subscriber_plot.py
from __future__ import annotations
import json, time, threading, collections
import matplotlib.pyplot as plt
import paho.mqtt.client as mqtt
from src.mqtt_io import make_client
from src.utils import load_config
 
BUFFER = 100
data = {
    "temp": collections.deque(maxlen=BUFFER),
    "hum":  collections.deque(maxlen=BUFFER),
    "prox": collections.deque(maxlen=BUFFER),
}
 
def on_message(client, userdata, message: mqtt.MQTTMessage):
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        topic = message.topic.split("/")[-1]
        if topic in data:
            data[topic].append(float(payload["value"]))
            print(f"SUB {topic}: {payload}")
    except Exception as e:
        print("Parse error:", e)
 
def plot_loop():
    plt.ion()
    fig, ax = plt.subplots(3, 1, figsize=(8,8))
    titles = ["Temperatura (°C)", "Humedad (%)", "Proximidad (cm)"]
    keys   = ["temp","hum","prox"]
    lines = []
    for i in range(3):
        (line,) = ax[i].plot([], [])
        ax[i].set_title(titles[i])
        ax[i].set_xlim(0, BUFFER)
        lines.append(line)
 
    while True:
        for i, k in enumerate(keys):
            y = list(data[k])
            x = list(range(len(y)))
            lines[i].set_xdata(x)
            lines[i].set_ydata(y)
            if y:
                ax[i].set_ylim(min(y)*0.95, max(y)*1.05)
                ax[i].set_xlim(0, max(len(y), 20))
        plt.pause(0.5)
 
def main():
    cfg = load_config()
    client = make_client("subscriber", cfg["broker"], cfg["port"], cfg["username"], cfg["password"], on_message)
    client.subscribe(f"{cfg['base_topic']}/#")
    client.loop_start()
 
    t = threading.Thread(target=plot_loop, daemon=True)
    t.start()
 
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()
 
if __name__ == "__main__":
    main()
