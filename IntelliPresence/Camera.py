"""
Camera object
"""

class Camera(object):

    def __init__(self, x1 = 0, y1 = 0, x2 = 0, y2 = 0, detected = True, name=None):
        self.point1 = (x1,y1)
        self.point2 = (x2,y2)
        self.detected = detected

        self.name = name

    def getPoint1(self):
        return self.point1

    def getPoint2(self):
        return self.point2

    def setPoint1(self, x, y):
        self.point1 = (x,y)
        
    def setPoint2(self, x, y):
        self.point2 = (x,y)

    def updateData( self, x1, y1, width, height ):
        """
        Updates the information about a detected face stored in this camera
        """
        self.point1 = ( int(x1), int(y1) )
        self.point2 = ( int(x1+width), int(y1+height) )
		

    def getWidth(self):
        """
        Returns the width of the camera face box thing
        """
        return self.point2[0] - self.point1[0]

    def getHeight(self):
        """
        Returns the height of the camera box
        """
        return self.point2[1] - self.point1[1]

    def getArea(self):
        
        return self.getWidth() * (self.point2[1]-self.point1[1])

    def __str__(self):
        return self.name + " Point 1 = "+str(self.point1)+", Point 2 = "+str(self.point2)
    def __repr__(self):
        if self.name is not None:
            return self.name
        else:
            return 'No name'

if __name__ == "__main__":

    cam = Camera(0, 5, 6, 10)
    print(cam)
    
    print(cam.getArea())

    cam.setPoint1(3,8)

    #print cam
