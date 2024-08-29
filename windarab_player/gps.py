import utm

def compute_scale(min_lat, max_lat, min_lon, max_lon, win_size) -> (float, float):
  min_pos = utm.from_latlon(min_lat, min_lon)
  max_pos = utm.from_latlon(max_lat, max_lon)
  scale_x = win_size/(max_pos[0]-min_pos[0])
  scale_y = win_size/(max_pos[1]-min_pos[1])
  return (scale_x, scale_y)

draw = lambda lat, lon: ...

def painter(canvas, lat, lon):
    pygame.draw(canvas, "red", (lat, lon), 1)

def create_painter(canvas):
    return lambda lat, lon: painter(canvas, lat, lon)