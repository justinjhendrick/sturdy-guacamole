class Config:
    def __init__(self, args):
        with open(self.args.map_file) as f:
            top = json.loads(f.read())
            width_m = top['width']
            # TODO: actually use these
            self.pixels_per_meter = SCREEN_WIDTH / width_m
            self.meters_per_pixel = 1.0 / self.pixels_per_meter