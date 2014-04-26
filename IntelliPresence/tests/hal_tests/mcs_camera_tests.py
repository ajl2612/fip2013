from intellipresence.hal.mcs_camera import MCSCamera

def updateData_test():
    # Note, move this into a unit test later
    cam = MCSCamera( 0,0,0,0,"Red2", 0, False)
    cam.updateData( 5,5, 10, 20, True )
    assert False
