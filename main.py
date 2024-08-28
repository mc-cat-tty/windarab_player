import sys
#from can import Bus
from windarab_player.parser import ParserTxt
from windarab_player.player import LogPlayer, PlayerParams, ChannelInfo
from struct import pack
import time

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
        lambda data: (int)(((int)(data * 100000000)) / 100000000) * 16777216
      ),
      'IMU_LONG': ChannelInfo(
        0x471,
        lambda data: (int)(((int)(data * 100000000) * 8388608) / 100000000) << 32
      ),
      'nmot': ChannelInfo(
        0x702,
        lambda data: data
      )
    },
    # Bus(interface="socketcan", channel="vcan0", bitrate=1e6)
  )
  player = LogPlayer(params)
  
  player.start()
  time.sleep(5)
  player.stop()
  while (True): ...
