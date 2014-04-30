from intellipresence.hal.mcs.camera import Camera
from intellipresence.hal.mcs.thread_server import NetworkThread
from intellipresence.hal.motor import Motor

class Armiture():
    """
    An armiture is the entire sensor platform assembly, which includes a tripod,
    MCS Camera and a Motor (both controlled over the network). This class
    models the real-world configuration of the hardware.
    """
    def __init__( self, int_id, camera, camera_ip, camera_port, motor, motor_ip, motor_port ):
        """
        Default constructor. As new sensors are added, this method should
        be updated.
        """
        self.int_id = int_id

        self.camera = camera
        self.camera_ip = camera_ip
        self.camera_port = camera_port

        self.motor = motor
        self.motor_ip = motor_ip
        self.motor_port = motor_port

        pi_thread = NetworkThread(self.camera_ip, self.camera_port, self.camera)
        pi_thread.start() 


    def getID(self):
        """
        Accessor for uniquie ID associated with this armiture
        """
        return self.int_id


    def isFaceDetected(self):
        """
        Returns true if a face has been detected by this Armiture. False otherwise.
        """
        return self.camera.isFaceDetected()


    def getMCSFaceArea(self):
        """
        Returns the area in pixels of the face detected by the MCS camera. Returns 0 
        if no face present.
        """
        return self.camera.getArea()


    def getMCSPoint1(self):
        """
        Accessor for upper left point of rectangle representing a detected face.
        """
        return self.camera.getPoint1()


    def getMCSPoint2(self):
        """
        Accessor for lower right point of rectangle representing a detected face.
        """
        return self.camera.getPoint2()


    def getMCSWidth(self):
        """
        Accessor for width of rectangle represeting a detected face.
        """
        return self.camera.getWidth()


    def getMCSHeight(self):
        """
        Accessor for height of rectangle represeting a detected face.
        """
        return self.camera.getHeight()
