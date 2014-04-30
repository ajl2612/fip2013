class Camera():
    """
    This class acts as the Hardware Abstraction layer between MCS Cameras and the centeral
    logic systems. This class is responsible for creating container variables for holding 
    camera information, creating an IO thread for monitoring a port for incoming data and 
    provinging a means for the rest of the system to accerss this data. This class will
    also have some logic for remembering past faces for a given set of time, to account
    for poor camera quality and some inconsistency in the facial detection algorithym.  
    """

    def __init__(self, x1, y1, x2, y2, name, ip_addr, port, detected = False):
        """
        Default constructor for MCSCamera. The only requirement is a name. All values 
        are zeroed out by default. 
        """
        self.ip_addr = ip_addr        
        self.port = port
        self.point1 = (x1,y1)
        self.point2 = (x2,y2)
        self.detected = detected 
        self.name = name

    def getPoint1(self):
        """
        Accessor for point representing the upper left corner of the face that has 
        been detected.
        """
        return self.point1

    def getPoint2(self):
        """
        Accessor for point representing the lower right corner of the face that has 
        been detected.
        """
        return self.point2

    def setPoint1(self, x, y):
        """
        Mutator for point representing the upper left corner of the face that has 
        been detected.
        """
        self.point1 = (x,y)

    def setPoint2(self, x, y):
        """
        Mutator for point representing the lower right corner of the face that has 
        been detected.
        """
        self.point2 = (x,y)

    def updateData( self, x1, y1, width, height, detect ):
        """
        More general update method that allows all data about a face to be updated 
        at once. 
        """
        self.point1 = ( int(x1), int(y1) )
        self.point2 = ( int(x1+width), int(y1+height) )
        self.detected = detect

    def getWidth(self):
        """
        Accessor for the width in pixels of the current face detected by this camera.
        """
        return self.point2[0] - self.point1[0]

    def getHeight(self):
        """
        Returns the height of the camera box
        """
        return self.point2[1] - self.point1[1]

    def getArea(self):
        """
        Accessor for area of face detection box in pixels
        """
        return self.getWidth() * (self.point2[1]-self.point1[1])

    def getName(self):
        """
        Accessor for name of this camera/
        """
        return self.name

    def isFaceDetected(self):
        """
        Returns true if this camera has detected a face and fals eif otherwise
        """
        return self.detected

    def __str__(self):
        return self.name + " Point 1 = " +str(self.point1) + ", Point 2 = "+ str(self.point2)

    def __repr__(self):
        return "({0}, {1}))".format( self.getPoint1(), self.getPoint2() )
