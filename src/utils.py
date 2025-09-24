# src/utils.py
import os, json, time
from dotenv import load_dotenv
 
def load_config():
    load_dotenv()
    return {
        "broker": os.getenv("MQTT_BROKER", "localhost"),
        "port": int(os.getenv("MQTT_PORT", "1883")),
        "username": os.getenv("MQTT_USERNAME") or None,
        "password": os.getenv("MQTT_PASSWORD") or None,
        "base_topic": os.getenv("MQTT_BASE_TOPIC", "cursoIoT/demo"),
        "interval": float(os.getenv("PUBLISH_INTERVAL_SEC", "1.0")),
    }
 
def ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
 
def to_json(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False)
