import signal
import sys
import logging
from intellipresence.hal.atem.atem_com import AtemCom

class Atem():
    """
    Facade class for interacting with the BlackMagic Design ATEM. Lets you
    change the channel.
    """
    def __init__( self, socket_ip, atem_ip, port, timeout ):
        """
        Default constructor.
        socket_ip - The IP address that the ATEM listener socket
                    will be bound to. 
        atem_ip - The IP address of the ATEM switch.
        port - The port the ATEM listener socket will bind to.
        timeout - The number of seconds to attempt to connect to the ATEM.
                  If a connection cannot be made within this time, the
                  program will be closed.
        """
        self.socket_ip = socket_ip
        self.atem_ip = atem_ip
        self.port = port
        self.timeout = timeout
        self.com = AtemCom( socket_ip, port ) 

    def connect( self ):
        """
        Initiate a connection with the ATEM.
        """
        def handle_sigalrm( signum, stack ):
            logger = logging.getLogger( __name__ )
            logger.error( "Timeout while attempting to connect to ATEM @ {}".format( self.atem_ip ) )
            sys.exit( -1 )

        # Register a sigalarm handler so that if the connection to the ATEM
        # times out, the handler will be called.    
        signal.signal( signal.SIGALRM, handle_sigalrm )

        # Attempt to connect to the ATEM.
        signal.alarm( self.timeout )
        self.com.connectToSwitcher( ( self.atem_ip, self.port ) )

        # The connection doesn't work until we've recieved a few pings
        # from the ATEM.
        for i in range( 0, 9 ):
            self.com.waitForPacket()
        
        # If we've made it this far, we can get rid of the timeout alarm.
        signal.alarm(0)
    
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
