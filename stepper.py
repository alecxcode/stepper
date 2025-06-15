# Stepper Motors on Raspberry Pi
from gpiozero import OutputDevice
from time import time


class Stepper:
    def __init__(self, number_of_steps, *motor_pins):
        self.step_number = 0
        self.direction = 0
        self.last_step_time = 0
        self.number_of_steps = number_of_steps
        self.step_delay = 0.004
        self.pin_count = len(motor_pins)
        if self.pin_count < 2 or self.pin_count > 5:
            raise ValueError("Unsupported number of pins")

        self.motor_pin_1 = OutputDevice(motor_pins[0])
        self.motor_pin_2 = OutputDevice(motor_pins[1])
        if self.pin_count > 3:
            self.motor_pin_3 = OutputDevice(motor_pins[2])
            self.motor_pin_4 = OutputDevice(motor_pins[3])
        if self.pin_count > 4:
            self.motor_pin_5 = OutputDevice(motor_pins[5])

        self.pins = [self.motor_pin_1, self.motor_pin_2]
        if self.pin_count > 3:
            self.pins.extend([self.motor_pin_3, self.motor_pin_4])
        if self.pin_count > 4:
            self.pins.append(self.motor_pin_5)

    def set_speed(self, speed):
        self.step_delay = 60.0 / (self.number_of_steps * speed)

    def step(self, steps_to_move):
        self.direction = 1 if steps_to_move > 0 else -1
        steps_left = abs(steps_to_move)
        while steps_left > 0:
            current_time = time()
            if (current_time - self.last_step_time) >= self.step_delay:
                self.last_step_time = current_time
                self.step_number += self.direction
                self.step_number %= self.number_of_steps
                if self.pin_count == 5:
                    self.step_motor(self.step_number % 10)
                else:
                    self.step_motor(self.step_number % 4)
                steps_left -= 1

    def step_motor(self, cur_step):
        if self.pin_count == 2:
            if cur_step == 0:  # 01
                self.motor_pins[0].off()
                self.motor_pins[1].on()
            elif cur_step == 1:  # 11
                self.motor_pins[0].on()
                self.motor_pins[1].on()
            elif cur_step == 2:  # 10
                self.motor_pins[0].on()
                self.motor_pins[1].off()
            elif cur_step == 3:  # 00
                self.motor_pins[0].off()
                self.motor_pins[1].off()
        elif self.pin_count == 4:
            if cur_step == 0:  # 1010
                self.motor_pin_1.on()
                self.motor_pin_2.off()
                self.motor_pin_3.on()
                self.motor_pin_4.off()
            elif cur_step == 1:  # 0110
                self.motor_pin_1.off()
                self.motor_pin_2.on()
                self.motor_pin_3.on()
                self.motor_pin_4.off()
            elif cur_step == 2:  # 0101
                self.motor_pin_1.off()
                self.motor_pin_2.on()
                self.motor_pin_3.off()
                self.motor_pin_4.on()
            elif cur_step == 3:  # 1001
                self.motor_pin_1.on()
                self.motor_pin_2.off()
                self.motor_pin_3.off()
                self.motor_pin_4.on()
        elif self.pin_count == 5:
            if cur_step == 0:  # 01101
                self.motor_pin_1.off()
                self.motor_pin_2.on()
                self.motor_pin_3.on()
                self.motor_pin_4.off()
                self.motor_pin_5.on()
            elif cur_step == 1:  # 01001
                self.motor_pin_1.off()
                self.motor_pin_2.on()
                self.motor_pin_3.off()
                self.motor_pin_4.off()
                self.motor_pin_5.on()
            elif cur_step == 2:  # 01011
                self.motor_pin_1.off()
                self.motor_pin_2.on()
                self.motor_pin_3.off()
                self.motor_pin_4.on()
                self.motor_pin_5.on()
            elif cur_step == 3:  # 01010
                self.motor_pin_1.off()
                self.motor_pin_2.on()
                self.motor_pin_3.off()
                self.motor_pin_4.on()
                self.motor_pin_5.off()
            elif cur_step == 4:  # 11010
                self.motor_pin_1.on()
                self.motor_pin_2.on()
                self.motor_pin_3.off()
                self.motor_pin_4.on()
                self.motor_pin_5.off()
            elif cur_step == 5:  # 10010
                self.motor_pin_1.on()
                self.motor_pin_2.off()
                self.motor_pin_3.off()
                self.motor_pin_4.on()
                self.motor_pin_5.off()
            elif cur_step == 6:  # 10110
                self.motor_pin_1.on()
                self.motor_pin_2.off()
                self.motor_pin_3.on()
                self.motor_pin_4.on()
                self.motor_pin_5.off()
            elif cur_step == 7:  # 10100
                self.motor_pin_1.on()
                self.motor_pin_2.off()
                self.motor_pin_3.on()
                self.motor_pin_4.off()
                self.motor_pin_5.off()
            elif cur_step == 8:  # 10101
                self.motor_pin_1.on()
                self.motor_pin_2.off()
                self.motor_pin_3.on()
                self.motor_pin_4.off()
                self.motor_pin_5.on()
            elif cur_step == 9:  # 00101
                self.motor_pin_1.off()
                self.motor_pin_2.off()
                self.motor_pin_3.on()
                self.motor_pin_4.off()
                self.motor_pin_5.on()

    def stop(self):
        for pin in self.pins:
            pin.off()
