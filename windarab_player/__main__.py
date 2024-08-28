import sys
import windarab_player.utils as utils
from can import Bus
from windarab_player.parser import ParserTxt
from windarab_player.player import LogPlayer, PlayerParams, ChannelInfo
import pygame

def dispatch_event(event):
  if event.type == pygame.QUIT: sys.exit(1)

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Pass data log filename as first and only argument")
    sys.exit(1)

  filename = sys.argv[1]
  parser = ParserTxt(filename)
  
  params = PlayerParams(
    time_points = parser.get_samples()['xtime'],
    channel_samples = parser.get_samples(),
    channels = {
      'IMU_LAT': ChannelInfo(
        0x471,
        lambda data: utils.float_to_ecu_int(data, 16777216) << 32
      ),
      'IMU_LONG': ChannelInfo(
        0x471,
        lambda data: utils.float_to_ecu_int(data, 8388608)
      ),
      'nmot': ChannelInfo(
        0x702,
        lambda data: data
      )
    },
    # Bus(interface="socketcan", channel="vcan0", bitrate=1e6)
  )

  player = LogPlayer(params)

  pygame.init()
  screen = pygame.display.set_mode((500, 500))
  clock = pygame.time.Clock()

  while (True):
    clock.tick(10)

    for e in pygame.event.get():
      dispatch_event(e)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]: player.start()
    if keys[pygame.K_RETURN]: player.play()
    if keys[pygame.K_BACKSPACE]: player.pause()
