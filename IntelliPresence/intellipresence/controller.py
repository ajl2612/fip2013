class Controller():
    """
    The controller is responsible for orchestrating the activities of the
    armatures and the ATEM hardware. It acts as a mediator between the
    different pieces of hardware. 
    """
    def __init__( self, armatures, atem ):
        self.armatures = armatures
        self.atem = atem

