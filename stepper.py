# Stepper Motors on Raspberry Pi
from time import time, sleep
from gpiozero import OutputDevice

class Stepper:
    """
    Class to control a stepper motor connected to the GPIO pins.

    Args:
        number_of_steps: The number of steps per revolution for the motor. If
                         the value is given as the number of degrees per step,
                         then divide 360 by that number to get the number of
                         steps (for example, 360 / 1.8 gives 200 steps).
        motor_pins: The GPIO pins to use to control the motor.
    """

    def __init__(self, number_of_steps, *motor_pins):
        self.step_number = 0
        self.direction = 0
        self.last_step_time = 0
        self.number_of_steps = number_of_steps
        self.step_delay = 0
        self.stop_mode = False
        self.pin_count = len(motor_pins)
        if self.pin_count not in (2, 4, 5):
            raise ValueError("Unsupported number of pins. Use 2, 4, or 5 pins.")

        self.pins = [OutputDevice(pin) for pin in motor_pins]
        
        self.motor_pin_1 = self.pins[0]
        self.motor_pin_2 = self.pins[1]
        
        if self.pin_count >= 4:
            self.motor_pin_3 = self.pins[2]
            self.motor_pin_4 = self.pins[3]
            
        if self.pin_count == 5:
            self.motor_pin_5 = self.pins[4]

    def set_speed(self, speed):
        """
        Sets the speed of the motor. This does not move the motor, just
        specifies how fast it moves when you call `step()`.

        Args:
            speed: The motor speed in rotations per minute (RPM).
        """

        if speed <= 0:
            return
        self.step_delay = 60.0 / (self.number_of_steps * speed)

    def step(self, steps_to_move):
        """
        Make the motor turn the specified number of steps. The speed of
        the steps is determined by the most recent call of `speed()`.

        Note: this function is blocking; it does not return until all 
        the steps have been completed, which could be a long time for
        a large number of steps (or a low speed).

        Args:
            steps_to_move: The number of steps to turn. A negative value turns
                           in the opposite direction.
        """

        self.stop_mode = False
        self.direction = 1 if steps_to_move > 0 else -1
        steps_left = abs(steps_to_move)
        while steps_left > 0:
            if self.stop_mode:
                break
            current_time = time()
            elapsed_time = current_time - self.last_step_time
            if elapsed_time >= self.step_delay:
                self.last_step_time = current_time
                self.step_number += self.direction
                self.step_number %= self.number_of_steps
                if self.pin_count == 5:
                    self.step_motor(self.step_number % 10)
                else:
                    self.step_motor(self.step_number % 4)
                steps_left -= 1
            else:
                sleep(self.step_delay - elapsed_time)

    def step_motor(self, cur_step):
        """
        Internal method to implement a single step by toggling the GPIO pins.
        """

        if self.pin_count == 2:
            if cur_step == 0:    # 01
                self.motor_pin_1.off()
                self.motor_pin_2.on()
            elif cur_step == 1:  # 11
                self.motor_pin_1.on()
                self.motor_pin_2.on()
            elif cur_step == 2:  # 10
                self.motor_pin_1.on()
                self.motor_pin_2.off()
            elif cur_step == 3:  # 00
                self.motor_pin_1.off()
                self.motor_pin_2.off()
        elif self.pin_count == 4:
            if cur_step == 0:    # 1010
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
            if cur_step == 0:    # 01101
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
        """
        Stop the motor by setting all the GPIO pins low.
        """

        self.stop_mode = True
        for pin in self.pins:
            pin.off()