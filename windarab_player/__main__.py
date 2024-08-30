import sys, pygame
from can import Bus
from windarab_player.gps import compute_scale
from windarab_player.channels_config import CHANNELS_CONFIG
from windarab_player.endianness_config import ENDIANNESS_CONFIG
from windarab_player.parser import ParserTxt
from windarab_player.player import LogPlayer, PlayerParams
from math import sqrt, pi, sin, cos, atan2
from windarab_player import shared_state
from windarab_player.shared_state import GpsPoint
import copy

def dispatch_event(event):
  if event.type == pygame.QUIT: sys.exit(1)

def to_rad(degAngle: float) -> float:
  return degAngle * pi / 180

def gps_distance(x: GpsPoint, y: GpsPoint) -> float:
  R = 6373000.0

  latx = to_rad(x.latitude)
  laty = to_rad(y.latitude)

  dlon = to_rad(y.longitude)  - to_rad(x.longitude)
  dlat = laty - latx

  a = pow(sin(dlat / 2), 2) + cos(latx) * cos(laty) * pow(sin(dlon / 2), 2)
  c = 2 * atan2(sqrt(a), sqrt(1 - a))

  return R * c


startPoint = GpsPoint(0, 0)
isInsideStartingZone = True

def process_lap_trigger_manual(currentPoint: GpsPoint):
  global startPoint, isInsideStartingZone
  rpmEngineOnThreshold = 2000
  startingZoneRadius = 3
  
  if (
    startPoint.latitude == 0
    and startPoint.longitude == 0
    and shared_state.rpm > rpmEngineOnThreshold
  ):
    print("Set start point")
    startPoint = copy.deepcopy(currentPoint)

  if (
    startPoint.latitude != 0
    and startPoint.longitude != 0
    and isInsideStartingZone
    and gps_distance(startPoint, currentPoint) > startingZoneRadius
  ):
    print("Increment lap")
    isInsideStartingZone = False
    shared_state.lap += 1

  if(
    not isInsideStartingZone
    and gps_distance(startPoint, currentPoint) < startingZoneRadius
  ):
    isInsideStartingZone = True
  
  print(f"Distance {gps_distance(startPoint, currentPoint)}")


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
    channels = CHANNELS_CONFIG,
    endianness = ENDIANNESS_CONFIG,
    can_interface = Bus(interface="socketcan", channel="can0", bitrate=1e6)
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

    pygame.draw.circle(screen, (1, 0, 0), pygame.mouse.get_pos(), 10, 10)
    
    process_lap_trigger_manual(shared_state.current_pos)
    print(f"{shared_state.rpm=}")
    print(f"{shared_state.lap=}")