# Python Stepper Motor Controller

A lightweight Python class for controlling stepper motors using GPIO on a Raspberry Pi via the `gpiozero` library. Supports 2-pin, 4-pin, and 5-pin motors.

It essentially implements the same `Stepper` class logic as described in the [Arduino Stepper library](https://docs.arduino.cc/libraries/stepper/).

## Features

- Compatible with 2-pin, 4-pin, and 5-pin stepper motors  
- Forward and reverse movement  
- Adjustable stepping delay (speed)  
- Arduino-style stepping logic  
- Easy integration with `gpiozero`
- Non-blocking and blocking modes
- Async mode and version

## Requirements

- Raspberry Pi with GPIO  
- Python 3.9+  
- `gpiozero` library

## Video Tutorial with Electronics

[![Video Tutorial](https://img.youtube.com/vi/T8thjPohz5g/mqdefault.jpg)](https://www.youtube.com/watch?v=T8thjPohz5g)

## Installation

Place the `stepper.py` file containing the `Stepper` class in your project directory.  
For asynchronous applications, place the `async_stepper.py` with `AsyncStepper` class file in your project directory.

Install dependencies if not already available. For example:
```bash
pip install gpiozero
```
or
```bash
sudo apt install python3-gpiozero
```

## Usage

### Standard methods
Initialize the object (example for 4-pin motor with 2048 steps):  
`step_motor = Stepper(2048, 5, 6, 13, 19)`

Set the motor speed in rotations per minute (RPM):  
`step_motor.set_speed(8)`

Move the motor one step forward:  
`step_motor.step(1)`

Move the motor one step backward:  
`step_motor.step(-1)`

Stop the motor immediately:  
`step_motor.stop()`

### Additional non-blocking methods:
Set the motor to move in a main loop:  
`step_motor.start(steps_to_move)`

Call this in each iteration of the main loop:  
`step_motor.tick()`

### Async methods in async_stepper module:
Same as above, but class name is `AsyncStepper`, and without start() and tick() as they are not needed in async mode.

## Examples

```python
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
```

```python
# Non-blocking mode example
from stepper import Stepper

motor = Stepper(2048, 5, 6, 13, 19)
motor.set_speed(10)
motor.start(1024) # can call in the main loop on event like sensor data

while True:
    t = motor.tick()
    # run other code while the motor works
    # or sleep(max(t, 0.0001))
    if motor.steps_left <= 0:
        break
```

```python
# Acynchronous mode example
import asyncio
from async_stepper import AsyncStepper

async def run():
    motor = AsyncStepper(2048, 5, 6, 13, 19)
    motor.set_speed(8)
    await motor.step(2048)

asyncio.run(run())
```

## Help the Creator

If you find this useful, consider supporting the developer.

[![Donate](https://exoimages.pages.dev/buttons/donate-ora.svg)](https://www.gofundme.com/f/keep-my-science-journey-alive-with-support)
