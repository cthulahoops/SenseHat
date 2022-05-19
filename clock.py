import math
import datetime
import time
from sense_hat import SenseHat

CLOCK_SIZE = 8
MIDPOINT = (CLOCK_SIZE - 1) / 2

hat = SenseHat()
hat.clear()

def main():
    while True:
        buffer = Buffer()
        now = datetime.datetime.now()
        print(now, now.hour, now.minute, now.second)

        hour_amount = (now.hour + now.minute / 60) % 12
        hour_angle = 2 * math.pi * hour_amount / 12
        minute_amount = (now.minute + now.second / 60) % 60
        minute_angle = 2 * math.pi * minute_amount / 60
        second_angle = 2 * math.pi * now.second / 60

        print(hour_angle, minute_angle)
        for x in range(CLOCK_SIZE):
            for y in range(CLOCK_SIZE):
                distance = math.sqrt((x - MIDPOINT) ** 2 + (y - MIDPOINT) ** 2)
                for (channel, angle, length) in [(0, hour_angle, 3), (1, minute_angle, 5), (2, second_angle, 5)]:
                    if distance > length:
                        continue

                    extent = 1.0 / (distance + 0.1)

                    intensity = 255 * (extent - pixel_angle_delta((x, y), angle)) / extent
                    buffer[(x, y)][channel] = clamp(int(intensity), 0, 256)


        time.sleep(0.5)

        buffer.draw()

def pixel_angle_delta(pixel, angle):
    simple_angle = abs(math.atan2(pixel[1] - MIDPOINT, pixel[0] - MIDPOINT) % (2 * math.pi) - angle)
    return min(simple_angle, 2 * math.pi - simple_angle)

def pixel_closest_to_angle(pixels, angle):
    return min(pixels, key=lambda pos: pixel_angle_delta(pos, angle))

def clamp(value, min_value, max_value):
    return min(max(value, min_value), max_value)

def clamp_rgb(rgb):
    return [clamp(int(rgb[0]), 0, 255), clamp(int(rgb[1]), 0, 255), clamp(int(rgb[2]), 0, 255)]

class Buffer:
    DISPLAY_SIZE = 8
    def __init__(self):
        self.buffer = [[0, 0, 0] for x in range(64)]

    def __setitem__(self, key, value):
        self.buffer[key[1] * self.DISPLAY_SIZE + key[0]] = clamp_rgb(value)

    def __getitem__(self, key):
        return self.buffer[key[1] * self.DISPLAY_SIZE + key[0]]

    def draw(self):
        hat.set_pixels(self.buffer)


if __name__ == '__main__':
    main()
