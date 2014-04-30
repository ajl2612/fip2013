class Controller():
    """
    The controller is responsible for orchestrating the activities of the
    armatures and the ATEM hardware. It acts as a mediator between the
    different pieces of hardware. 
    """
    def __init__( self, armitureList, atem ):
        #list of Armiture objects
        self.armitures = armitureList
	self.atem = atem

    def camera_ranks(self):
        """
        Determines capture camera with the largest percentage of face
        as given by Facial Detection
        returns the ,ist fo MCS cameras odered by largest face value.
        Face value currently area, to be refined later.
        If no faces are detected, returns an empty list. 
        """
        camList = []
        for arm in self.armitures:
            if arm.isFaceDetected():
                camList.append( (arm.getMCSFaceArea() , arm.getID() ))
            else:
                camList.append( ( 0 , arm.getID() ))

        camList.sort(reverse = True)
        return camList

    def best_angle(self, cam, mcs=False):
        """
        Finds the best angle for camera 'cam'
        Depends on IR Code for input for now. Waiting for them.
        mcs = (bool) if method should run based on mcs input. False by default. 
        """
        #IR_code.getAngle or whatever they use
        bestAngle = self.default_camera_angle
        currentAngle = self.angles[cam]
        temp = self.mcsCams[cam]
        if temp.getX2() <= 133 or currentAngle == 3 and temp.getX1() <= 167:
            bestAngle = 2
        elif currentAngle == 2:
            if temp.getX1() >= 233:
                bestAngle = 1
            elif temp.getX2() <= 67:
                bestAngle = 3
            elif currentAngle == 3:
                pass
            else:
                pass
        else:
            pass
        return bestAngle

