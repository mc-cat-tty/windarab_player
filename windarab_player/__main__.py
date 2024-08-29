import sys
import pygame
from can import Bus
from windarab_player.channels_config import CHANNELS_CONFIG
from windarab_player.parser import ParserTxt
from windarab_player.player import LogPlayer, PlayerParams

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
    channels = CHANNELS_CONFIG,
    can_interface = Bus(interface="socketcan", channel="can0", bitrate=1e6)
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
    if keys[pygame.K_UP]: player.speed_up()
    if keys[pygame.K_DOWN]: player.slow_down()
