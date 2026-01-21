from enum import Enum, auto
import time

class GearState(Enum):
    UP_LOCKED = auto()
    TRANSITIONING_DOWN = auto()
    DOWN_LOCKED = auto()

class LandingGearController:
    def __init__(self):
        self.state = GearState.UP_LOCKED
        self.on_ground = True
        self.sensor_ok = False

    def log(self, message):
        print(f"[{self.state.name}] {message}")

    def command_gear_down(self):
        self.log("Gear down command received")

        #Fault detection
        if not self.sensor_ok:
            self.log("Sensor fault detected. Aborting gear deployment.")
            return

        #Safety guard
        if not self.on_ground:
            self.log("Unsafe to deploy gear while airborne")
            return

        if self.state == GearState.UP_LOCKED:
            self.log("Transition initiated")
            self.state = GearState.TRANSITIONING_DOWN
            self.log(f"State changed to {self.state.name}")
            self.log("Gear deploying")

            time.sleep(1.5)

            self.state = GearState.DOWN_LOCKED
            self.log(f"State changed to {self.state.name}")
            self.log("Gear locked down")
        else:
            self.log("Command rejected due to invalid state")


controller = LandingGearController()
controller.command_gear_down()
