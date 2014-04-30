import time

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

    def camera_ranks2(self):
        pass

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

    def start( self ):
        """
        Connect to the ATEM and run MCS.
        """
        self.atem.connect()

        while( True ):
            arm1 = self.armitures[0]
            arm2 = self.armitures[1]
            arm3 = self.armitures[2]
            arm4 = self.armitures[3]

            arm1Det = arm1.isFaceDetected()
            arm1Val = arm1.getMCSFaceArea()
            arm2Det = arm2.isFaceDetected()
            arm2Val = arm2.getMCSFaceArea()
            arm3Det = arm3.isFaceDetected()
            arm3Val = arm3.getMCSFaceArea() 
            arm4Det = arm4.isFaceDetected()
            arm4Val = arm4.getMCSFaceArea() 

            print( "Armiture 1: {0} {1}, Armiture 2: {2} {3}, Armiture 3 {4} {5}, Armiture 4 {6} {7}".format(arm1Det, arm1Val, arm2Det, arm2Val, arm3Det, arm3Val, arm4Det, arm4Val ) )
            camRanks = self.camera_ranks()
            #print( camRanks )
            best_arm = camRanks[0][1] 
            print( "ARM {0} BEST".format( best_arm ) )
            self.atem.set_program_channel( best_arm )
            time.sleep(2)
