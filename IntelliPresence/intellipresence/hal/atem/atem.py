from intellipresence.hal.atem.atem_com import AtemCom

class Atem():
    """
    Facade class for interacting with the BlackMagic Design ATEM. Lets you
    change the channel.
    """
    def __init__( self, socket_ip, atem_ip, port ):
        """
        Default constructor.
        socket_ip - The IP address that the ATEM listener socket
                    will be bound to. 
        atem_ip - The IP address of the ATEM switch.
        port - The port the ATEM listener socket will bind to.
        """
        self.socket_ip = socket_ip
        self.atem_ip = atem_ip
        self.port = port
        self.com = AtemCom( socket_ip, port ) 

    def connect( self ):
        """
        Initiate a connection with the ATEM.
        """
        # Connect to the ATEM.
        self.com.connectToSwitcher( ( self.atem_ip, self.port ) )

        # The connection doesn't work until we've recieved a few pings
        # from the ATEM.
        for i in range( 0, 9 ):
            self.com.waitForPacket()

    def set_preview_channel( self, channel ):
        """
        Change the preview channel to the indicated channel.
        channel - Integer number identifying the channel to switch to.
        """
        pass

    def set_program_channel( self, channel ):
        """
        Change the program channel to the indicated channel.
        channel - Integer number identifying the channel to switch to.
        """
        pass
