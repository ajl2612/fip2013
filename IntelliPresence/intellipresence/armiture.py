from hal.mcs_camera import Camera
from hal.motor import Motor

class Armiture():
    """
    An armiture is the entire sensor platform assembly, which includes a tripod,
    MCS Camera and a Motor (both controlled over the network). This class
    models the real-world configuration of the hardware.
    """
    def __init__( self, motor, camera ):
        """
        Default constructor. As new sensors are added, this method should
        be updated.
        """
        self.motor = motor
        self.camera = camera

