# src/mqtt_io.py
from __future__ import annotations
import paho.mqtt.client as mqtt
from typing import Optional, Callable
 
def make_client(client_id: str,
                host: str,
                port: int,
                username: Optional[str]=None,
                password: Optional[str]=None,
                on_message: Optional[Callable]=None) -> mqtt.Client:
 
    client = mqtt.Client(client_id=client_id, callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    if username and password:
        client.username_pw_set(username, password)
    if on_message:
        client.on_message = on_message
 
    def _on_connect(c, userdata, flags, reason_code, properties=None):
        print(f"[MQTT] Connected rc={reason_code}")
 
    def _on_disconnect(c, userdata, reason_code, properties=None):
        print(f"[MQTT] Disconnected rc={reason_code}")
 
    client.on_connect = _on_connect
    client.on_disconnect = _on_disconnect
    client.connect(host, port, keepalive=30)
    return client
