class Settings:
    GRAVITY_DEFAULT = 300
    TERRAIN_SMOOTHNESS_DEFAULT = 7
    TERRAIN_SPACING_DEFAULT = 10
    TERRAIN_AMPLITUDE_DEFAULT = 0.5
    MAP_LENGTH_DEFAULT = 4000
    CAR_RATE_DEFAULT = 100
    CAR_MAX_FORCE_DEFAULT = 1000000

    def __init__(self, gravity=None, terrain_smoothness=None, terrain_spacing=None, terrain_amplitude=None, map_length=None, car_rate=None, car_max_force=None):
        if gravity:
            self.gravity = gravity
        else:
            self.gravity = Settings.GRAVITY_DEFAULT
        if terrain_smoothness:
            self.terrain_smoothness = terrain_smoothness
        else:
            self.terrain_smoothness = Settings.TERRAIN_SMOOTHNESS_DEFAULT
        if terrain_spacing:
            self.terrain_spacing = terrain_spacing
        else:
            self.terrain_spacing = Settings.TERRAIN_SPACING_DEFAULT
        if terrain_amplitude:
            self.terrain_amplitude = terrain_amplitude
        else:
            self.terrain_amplitude = Settings.TERRAIN_AMPLITUDE_DEFAULT
        if map_length:
            self.map_length = map_length
        else:
            self.map_length = Settings.MAP_LENGTH_DEFAULT
        if car_rate:
            self.car_rate = car_rate
        else:
            self.car_rate = Settings.CAR_RATE_DEFAULT
        if car_max_force:
            self.car_max_force = car_max_force
        else:
            self.car_max_force = Settings.CAR_MAX_FORCE_DEFAULT
