import sys, can
from typing import Any, Callable
from dataclasses import dataclass
from threading import Thread
from time import sleep
from collections import defaultdict

@dataclass(frozen=True)
class ChannelInfo:
  can_id: int
  can_fmt_fn: Callable

@dataclass(frozen=True)
class PlayerParams:
  time_points: list[float]
  channels: dict[str, ChannelInfo]
  channel_samples: dict[str, list[Any]]
  # can_interface: can.Bus

class LogPlayer:
  def __init__(self, params: PlayerParams):
    self.params = params
    self.tx_thread = Thread(target=self.player, name="player_thread")
    self.killed = False
    self.paused = False

  def paused_busy_wait(self):
    while self.paused:
      sleep(1e-2)

  def send(self, idx):
    messages = defaultdict(int)

    for channel_label, channel_info in self.params.channels.items():
      id = channel_info.can_id
      format_fn = channel_info.can_fmt_fn
      messages[id] |= format_fn(self.params.channel_samples[channel_label][idx])

    for can_id, payload in messages.items():
      print(f"Sending {payload} on CAN ID {can_id}")
      # self.params.can_interface.send(
      #   can.Message(
      #     arbitration_id=can_id,
      #     data=int.to_bytes(payload),
      #     is_extended_id=False
      #   )
      # )

  def player(self):
    for idx, _ in enumerate(self.params.time_points):
      if idx != 0:
        sleep(self.params.time_points[idx] - self.params.time_points[idx-1])
      if self.killed: sys.exit()
      self.paused_busy_wait()
      self.send(idx)
    
  def start(self):
    self.tx_thread.start()
  
  def stop(self):
    self.killed = True

  def pause(self):
    self.paused = True
  
  def play(self):
    self.paused = False