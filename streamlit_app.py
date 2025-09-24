# streamlit_app.py
import json, threading, collections
import streamlit as st
import paho.mqtt.client as mqtt
from src.mqtt_io import make_client
from src.utils import load_config
 
st.set_page_config(page_title="IoT Live Dashboard", layout="wide")
cfg = load_config()
BUFFER = 200
store = {k: collections.deque(maxlen=BUFFER) for k in ("temp","hum","prox")}
 
def on_message(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode("utf-8"))
        topic = message.topic.split("/")[-1]
        if topic in store:
            store[topic].append(float(payload["value"]))
    except Exception:
        pass
 
def mqtt_thread():
    client = make_client("streamlit", cfg["broker"], cfg["port"], cfg["username"], cfg["password"], on_message)
    client.subscribe(f"{cfg['base_topic']}/#")
    client.loop_forever()
 
if "mqtt_started" not in st.session_state:
    threading.Thread(target=mqtt_thread, daemon=True).start()
    st.session_state["mqtt_started"] = True
 
st.title("Simulación IoT – Dashboard en Tiempo Real")
col1, col2, col3 = st.columns(3)
for c, k, label in [(col1,"temp","Temperatura (°C)"), (col2,"hum","Humedad (%)"), (col3,"prox","Proximidad (cm)")]:
    val = store[k][-1] if len(store[k]) else None
    c.metric(label, val)
 
st.line_chart(list(store["temp"]), height=200)
st.line_chart(list(store["hum"]), height=200)
st.line_chart(list(store["prox"]), height=200)
st.caption(f"Broker: {cfg['broker']} | Base topic: {cfg['base_topic']}")
