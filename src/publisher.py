# src/publisher.py
from __future__ import annotations
import time
from src.sensors import TemperatureSensor, HumiditySensor, ProximitySensor
from src.mqtt_io import make_client
from src.utils import load_config, to_json, ts
 
def main():
    cfg = load_config()
    client = make_client("publisher", cfg["broker"], cfg["port"], cfg["username"], cfg["password"])
    client.loop_start()
 
    temp = TemperatureSensor()
    hum = HumiditySensor()
    prox = ProximitySensor()
 
    try:
        while True:
            payloads = [
                (f"{cfg['base_topic']}/temp", {"t": ts(), "type":"temperature", "unit":"C", "v":1, "value": temp.read()}),
                (f"{cfg['base_topic']}/hum",  {"t": ts(), "type":"humidity",    "unit":"%", "v":1, "value": hum.read()}),
                (f"{cfg['base_topic']}/prox", {"t": ts(), "type":"proximity",   "unit":"cm","v":1, "value": prox.read()}),
            ]
            for topic, data in payloads:
                client.publish(topic, to_json(data), qos=0, retain=False)
                print(f"PUB {topic}: {data}")
            time.sleep(cfg["interval"])
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()
 
if __name__ == "__main__":
    main()
