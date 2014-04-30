from intellipresence.hal.mcs.camera import Camera

def updateData_test():
    # Note, move this into a unit test later
    cam = Camera( 0,0,0,0,"Red2", 0, False)
    cam.updateData( 5, 5, 10, 20, True )
    assert cam.getPoint1()[0] == 5
    assert cam.getPoint1()[1] == 5
    assert cam.getPoint2()[0] == 15
    assert cam.getPoint2()[1] == 25
    assert cam.isFace()

