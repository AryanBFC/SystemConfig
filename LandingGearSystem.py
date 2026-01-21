from enum import Enum, auto
import time


class GearState(Enum):
    UP_LOCKED = auto()
    TRANSITIONING_DOWN = auto()
    DOWN_LOCKED = auto()


class SensorStatus(Enum):
    OK = auto()
    FAILED = auto()


class LandingGearController:
    def __init__(self):
        self.state = GearState.UP_LOCKED

        self.on_ground = True
        self.airspeed_valid = True

        self.primary_sensor = SensorStatus.OK
        self.backup_sensor = SensorStatus.OK

        self.active_sensor = "PRIMARY"
        self.system_degraded = False

    def log(self, message):
        print(f"[{self.state.name} | {self.active_sensor} | DEGR:{self.system_degraded}] {message}")


    def read_sensor(self):
        """Attempt to use primary sensor. If failed, switch to backup."""
        if self.primary_sensor == SensorStatus.OK:
            self.active_sensor = "PRIMARY"
            return True

        #Primary failed and triees switching to backup
        self.log("Primary sensor failure detected. Switching to backup...")

        if self.backup_sensor == SensorStatus.OK:
            self.active_sensor = "BACKUP"
            self.system_degraded = True
            self.log("Backup sensor active. System running in degraded mode.")
            return True

        #Both failed
        self.active_sensor = "NONE"
        self.system_degraded = True
        self.log("CRITICAL: Both sensors failed. Unable to determine gear state.")
        return False


    def command_gear_down(self):
        self.log("Gear down command received")

        if not self.read_sensor():
            self.log("Sensor read failed. Aborting deployment.")
            return

        if not self.on_ground:
            self.log("Unsafe to deploy gear while airborne")
            return

        if self.state != GearState.UP_LOCKED:
            self.log("Command rejected due to invalid state")
            return

        self.log("Initiating gear deployment sequence")
        self.state = GearState.TRANSITIONING_DOWN
        self.log("Gear deploying...")

        time.sleep(1.5)

        self.state = GearState.DOWN_LOCKED
        self.log("Gear locked down successfully")



controller = LandingGearController()

#Simulate whether the sensors fail or not
controller.primary_sensor = SensorStatus.OK
controller.backup_sensor = SensorStatus.OK

controller.command_gear_down()

