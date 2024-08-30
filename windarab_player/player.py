import sys, can
from typing import Any, Callable
from dataclasses import dataclass
from threading import Thread
from time import sleep
from collections import defaultdict
from windarab_player import shared_state

@dataclass(frozen=True)
class ChannelInfo:
  can_id: int
  can_fmt_fn: Callable

@dataclass(frozen=True)
class PlayerParams:
  time_points: list[float]
  channels: dict[str, ChannelInfo]
  endianness: dict[int, str]
  channel_samples: dict[str, list[Any]]
  can_interface: can.Bus

class LogPlayer:
  def __init__(self, params: PlayerParams):
    self.params = params
    self.tx_thread = Thread(target=self.player, name="player_thread")
    self.killed = False
    self.paused = False
    self.speed_factor = 1

  def paused_busy_wait(self):
    while self.paused:
      sleep(1e-2)

  def send(self, idx):
    messages = defaultdict(int)

    for channel_label, channel_info in self.params.channels.items():
      id = channel_info.can_id
      format_fn = channel_info.can_fmt_fn
      messages[id] |= format_fn(value := self.params.channel_samples[channel_label][idx])
      
      if channel_label == "nmot": shared_state.rpm = value
      if channel_label == "IMU_LAT": shared_state.current_pos.latitude = value
      if channel_label == "IMU_LONG": shared_state.current_pos.longitude = value

    for can_id, payload in messages.items():
      if (messages[id] < 0): continue
      # print(f"Sending {payload:x} on CAN ID {can_id:x} with endianness {self.params.endianness[can_id]}")
      self.params.can_interface.send(
        can.Message(
          arbitration_id=can_id,
          data=int.to_bytes(payload, 8, byteorder=self.params.endianness[can_id]),
          is_extended_id=False
        )
      )

    

  def player(self):
    for idx, _ in enumerate(self.params.time_points):
      #print(f"{self.params.time_points[idx]=}")
      lapctr = self.params.channel_samples["lapctr"][idx]
      #print(f"{lapctr=}")
      if idx != 0:
        dt = self.params.time_points[idx] - self.params.time_points[idx-1]
        sleep(dt/self.speed_factor)
      if self.killed: sys.exit()
      self.paused_busy_wait()
      self.send(idx)
    
  def start(self):
    print("START")
    if not self.tx_thread.is_alive():
      self.tx_thread.start()
  
  def stop(self):
    print("STOP")
    self.killed = True

  def pause(self):
    print("PAUSE")
    self.paused = True
  
  def play(self):
    print("PLAY")
    self.paused = False
  
  def speed_up(self):
    self.speed_factor = self.speed_factor+1
    print(f"{self.speed_factor=}")

  def slow_down(self):
    self.speed_factor = max(1, self.speed_factor-1)
    print(f"{self.speed_factor=}")