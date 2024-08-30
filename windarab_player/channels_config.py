from windarab_player.player import ChannelInfo
import windarab_player.utils as utils


CHANNELS_CONFIG = {
    'IMU_LAT': ChannelInfo(
        0x471,
        lambda data: utils.float_to_ecu_int(data, 16777216)
    ),
    'IMU_LONG': ChannelInfo(
        0x471,
        lambda data: utils.float_to_ecu_int(data, 8388608, 4)
    ),
    'nmot': ChannelInfo(
        0x702,
        lambda data: data
    ),
    'vwheel_fl': ChannelInfo(
        0x702,
        lambda data: utils.float_to_ecu_short(data, 100, 2)
    ),
    'ath': ChannelInfo(
        0x702,
        lambda data: utils.float_to_ecu_short(data, 100, 6)
    )
}