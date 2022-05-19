import math
import datetime
import time
from sense_hat import SenseHat

hat = SenseHat()
hat.clear()

def pixel_angle_delta(pixel, angle):
    simple_angle = abs(math.atan2(pixel[1] - 3.5, pixel[0] - 3.5) % (2 * math.pi) - angle)
    return min(simple_angle, 2 * math.pi - simple_angle)

def pixel_closest_to_angle(pixels, angle):
    return min(pixels, key=lambda pos: pixel_angle_delta(pos, angle))

class Buffer:
    def __init__(self):
        self.buffer = [[0, 0, 0] for x in range(64)]

    def __setitem__(self, key, value):
        self.buffer[key[1] * 8 + key[0]] = value

    def __getitem__(self, key):
        return self.buffer[key[1] * 8 + key[0]]

    def draw(self):
        hat.set_pixels(self.buffer)


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

        hour_pixel = pixel_closest_to_angle(inner, hour_angle)
        minute_pixel = pixel_closest_to_angle(outer, minute_angle)
        second_pixel = pixel_closest_to_angle(outer, second_angle)

        print(hour_angle, minute_angle)
        for x in range(8):
            for y in range(8):
                distance = math.sqrt((x - 3.5) ** 2 + (y - 3.5) ** 2)
                for (channel, angle, length) in [(0, hour_angle, 3), (1, minute_angle, 5), (2, second_angle, 5)]:
                    if distance > length:
                        continue

                    extent = 1.0 / distance

                    intensity = 255 * (extent - pixel_angle_delta((x, y), angle)) / extent
                    buffer[(x, y)][channel] = max(int(intensity), 0)


        time.sleep(0.5)

        buffer.draw()

if __name__ == '__main__':
    main()
