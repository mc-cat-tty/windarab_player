import math

class LapCounter:

    __isInsideStartingZone = True
    #__rpmEngineOnThreshold = 2000
    __startingZoneSquaredRadius = 1

    def __init__(self, starting_lat = 0, starting_lon = 0):
        self.starting_lat = starting_lat
        self.starting_lon = starting_lon
        self.lap_count = 0
    
    def __to_rad(degAngle):
        return degAngle * math.pi / 180

    def __gps_distance_from_start(self, lat, lon):
        R = 6373000.0

        
        latx = self.__to_rad(self.starting_lat)
        laty = self.__to_rad(lat)

        dlon = self.__to_rad(lon)  - self.__to_rad(self.starting_lon)
        dlat = laty - latx

        a = pow(math.sin(dlat / 2), 2) + math.cos(latx) * math.cos(laty) * pow(math.sin(dlon / 2), 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def process_lap_trigger_manual(self, curr_lat, curr_lon):

        if (
            self.starting_lat == 0
            and self.starting_lon == 0):
            self.starting_lon = curr_lon
            self.starting_lat = curr_lat

        if (
            self.__isInsideStartingZone
            and self.__gps_distance_from_start(curr_lat, curr_lon) > self.__startingZoneSquaredRadius
        ):
                self.__isInsideStartingZone = False
                self.lap_count += 1


        if(
            not self.__isInsideStartingZone
            and  self.__gps_distance_from_start(curr_lat, curr_lon) < self.__startingZoneSquaredRadius
        ):
            self.__isInsideStartingZone = True