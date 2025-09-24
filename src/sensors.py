# src/sensors.py
from __future__ import annotations
import random
import time
from dataclasses import dataclass
 
def _bounded_random_walk(value: float, low: float, high: float, step: float, jitter: float) -> float:
    center = (low + high) / 2
    drift = (center - value) * 0.05
    value += drift + random.uniform(-step, step) + random.uniform(-jitter, jitter)
    return max(low, min(high, value))
 
@dataclass
class TemperatureSensor:
    value: float = 24.0
    low: float = 20.0
    high: float = 30.0
    step: float = 0.2
    jitter: float = 0.05
    def read(self) -> float:
        self.value = _bounded_random_walk(self.value, self.low, self.high, self.step, self.jitter)
        return round(self.value, 2)
 
@dataclass
class HumiditySensor:
    value: float = 50.0
    low: float = 35.0
    high: float = 75.0
    step: float = 0.3
    jitter: float = 0.05
    def read(self) -> float:
        self.value = _bounded_random_walk(self.value, self.low, self.high, self.step, self.jitter)
        return round(self.value, 1)
 
@dataclass
class ProximitySensor:
    far_low: float = 120.0
    far_high: float = 200.0
    near_low: float = 15.0
    near_high: float = 40.0
    p_event: float = 0.07
    event_len_s: float = 2.5
    _in_event_until: float = 0.0
    def read(self) -> float:
        now = time.time()
        if now < self._in_event_until:
            return round(random.uniform(self.near_low, self.near_high), 1)
        if random.random() < self.p_event:
            self._in_event_until = now + self.event_len_s
            return round(random.uniform(self.near_low, self.near_high), 1)
        return round(random.uniform(self.far_low, self.far_high), 1)
