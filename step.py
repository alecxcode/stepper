# 4-pin Stepper Motor on Raspberry Pi
from time import sleep
from stepper import Stepper

step_motor = Stepper(2048, 5, 6, 13, 19)
step_motor.set_speed(10)

try:
    while True:
        step_motor.step(1024)
        print("rotated half")
        sleep(2)
        step_motor.step(1024)
        print("rotated half more")
        sleep(2)
        step_motor.step(-1024)
        print("rotated half back")
        sleep(2)
        step_motor.step(-1024)
        print("rotated half more back")
        sleep(2)
except KeyboardInterrupt:
    pass
finally:
    step_motor.stop()