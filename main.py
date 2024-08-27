import sys
from can import Bus
from lib.parser import ParserTxt
from lib.player import LogPlayer, PlayerParams
from time import sleep

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print("Pass data log filename as first and only argument")
    sys.exit(1)

  filename = sys.argv[1]
  parser = ParserTxt(filename)
  
  params = PlayerParams(
    (1, 6, 16),
    {'a': (1, 2, 3)},
    {'a': 0x00},
    {'a': lambda x: x},
    # Bus(interface="socketcan", channel="vcan0", bitrate=1e6)
  )
  player = LogPlayer(params)
  player.start()
  while (True): ...