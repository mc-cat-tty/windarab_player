import sys, pygame
from can import Bus
from windarab_player.gps import compute_scale
from windarab_player.channels_config import CHANNELS_CONFIG
from windarab_player.endianness_config import ENDIANNESS_CONFIG
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
  samples = parser.get_samples()
  
  params = PlayerParams(
    time_points = samples['xtime'],
    channel_samples = samples,
    endianness = ENDIANNESS_CONFIG,
    channels = CHANNELS_CONFIG,
    can_interface = Bus(interface="socketcan", channel="vcan0", bitrate=1e6)
  )

  player = LogPlayer(params)

  pygame.init()
  WIN_SIZE = 500
  screen = pygame.display.set_mode((WIN_SIZE, WIN_SIZE))
  clock = pygame.time.Clock()

  sx, sy = compute_scale(
    min(samples["IMU_LAT"]),
    max(samples["IMU_LAT"]),
    min(samples["IMU_LONG"]),
    max(samples["IMU_LONG"]),
    WIN_SIZE
  )

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
