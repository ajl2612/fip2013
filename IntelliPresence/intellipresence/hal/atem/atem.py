from intellipresence.hal.atem.atem_thread import AtemThread

class Atem():
    """
    Facade class for interacting with the BlackMagic Design ATEM. Lets you
    change the channel.
    """

    def __init__( self, atem_thread ):
        """
        Default constructor.
        atem_thread - Thread which performs IO to the BlackMagic Design device.
        """
        self.thread = atem_thread

    def setChannel( self, channel ):
        """
        Change the channel to the indicated channel.
        channel - Integer number identifying the channel to switch to.
        """

