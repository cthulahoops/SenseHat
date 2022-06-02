from dataclasses import dataclass
import time
from sense_hat import SenseHat

@dataclass
class Vector:
    x: float
    y: float

    def __add__(self, other):
        return self.__class__(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return self.__class__(self.x * other, self.y * other)

    def __rmul__(self, other):
        return self * other

print("Started")

hat = SenseHat()

hat.clear()

ball = Vector(4, 4)
ball_velocity = Vector(0, 0)

last = (0, 0)

while True:
    acc = hat.get_accelerometer_raw()
#    acc = hat.get_gyroscope_raw()
    acc = Vector(acc['x'], acc['y'])
    ball_velocity += 0.8 * acc
    ball_velocity *= 0.9
    ball += ball_velocity

    if ball.x < 0:
        ball.x = 0
        ball_velocity.x *= -0.7
    if ball.y < 0:
        ball.y = 0
        ball_velocity.y *= -0.7
    if ball.x > 7:
        ball.x = 7
        ball_velocity.x *= -0.7
    if ball.y > 7:
        ball.y = 7
        ball_velocity.y *= -0.7

    this = (round(ball.x), round(ball.y))
    if this != last:
        hat.set_pixel(last[0], last[1], (0, 0, 0))
        last = this
        hat.set_pixel(this[0], last[1], (0, 0, 255))
    time.sleep(0.1)
