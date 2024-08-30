from dataclasses import dataclass


@dataclass
class GpsPoint:
  latitude: int
  longitude: int


rpm = 0
lap = 0
current_pos = GpsPoint(0, 0)