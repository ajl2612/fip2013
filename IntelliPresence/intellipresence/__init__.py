"""
This file contains the entry point and signal handlers for the program.
"""
import signal
import sys
import time
import logging
import intellipresence.config
import intellipresence.util
from intellipresence.controller import Controller
from intellipresence.hal.atem.atem import Atem

def main():
    """
    The starting point for the program.
    """
    # Configure the logger. This is done first because everything else uses
    # the logger.
    configure_logger()
    
    # Validate some of the options that were added to the configuration.
    validate_configuration()

    # Register handlers for various Unix signals. Signals are used to perform
    # Interprocess Communication in Unix-like operating systems; In this case,
    # we're handling IPC from a bash shell (ie. The user killing the program).
    register_signal_handlers()

    # Configure the armatures.
    armatures = configure_armatures()

    # Configure the ATEM subsystem.
    atem = configure_atem()
    atem.connect()

    # Configure the controller.
    controller = Controller( armatures, atem )

    # TODO: Kick things off here.

    # Put the thread to sleep until the user hits ctrl-C.
    while( True ):
        time.sleep(1)

def validate_configuration():
    """
    Validate the configuration in config.py. 
    """
    logger = logging.getLogger(__name__)

    # Make sure that a valid network interface was provided for the ATEM.
    interface_name = config.atem['adapter']
    if not util.is_valid_network_interface( interface_name ):
        logging.error( str( interface_name ) + " isn't a valid network interface." )
        sys.exit( -1 )

def configure_logger():
    """
    Configure the logger. By default we only care to have the output sent to
    standard out for now. In the future we could have this log to disk
    really easily.
    """
    root = logging.getLogger()
    root.setLevel( logging.DEBUG )
    formatter = logging.Formatter("[%(asctime)s][%(name)s][%(levelname)s]: %(message)s")

    # Create and configure the standard out logging handler.
    std_out_handler = logging.StreamHandler( sys.stdout )
    std_out_handler.setLevel( logging.DEBUG )
    std_out_handler.setFormatter( formatter )

    # Add it to the root logger so all loggers can write to standard out.
    root.addHandler( std_out_handler )

def configure_atem():
    """
    Build an return an instance of the ATEM facade class.
    The ATEM is an HDMI switch that is controlled over ethernet using a protocol
    that was kinda-sorta reverse engineered. The ATEM facade class uses a thread
    and a socket to perform I/O operations with the ATEM hardware.
    """
    adapter = config.atem['adapter']
    atem_ip = config.atem['atem_addr']
    port = config.atem['port']
    
    socket_ip = util.get_interface_ip_addr( adapter )
    return Atem( socket_ip, atem_ip, port )

def configure_armatures():
    """
    An armature in the context of this system is an MCS Camera and Motor pair
    on a tripod. The system consists of several of these armatures.
    The MCS Camera and Motor both use a Thread with a Socket to communicate
    with the physical Raspberry Pi hardware that the classes are modeled after. 
    """
    # TODO: Write me!
    return []

def register_signal_handlers():
    """
    Register the signal handlers used by the application. These are functions
    that perform some action when a unix signal is sent to the main thread.
    """
    signal.signal( signal.SIGINT, handle_sigint )
    if hasattr( signal, 'SIGINFO' ):
        signal.signal( signal.SIGINFO, handle_siginfo )

def handle_sigint( signum, stack ):
    """
    This function is called when a sigint signal (Ctrl-C) is sent to
    this thread. Any kind of cleanup that's needed before shutting
    down should occur here.
    """
    logger = logging.getLogger( __name__ )
    logger.info( "SIGINT received." )

    # TODO: Kill other threads, write out anything that needs to be persisted, etc.

    # Kill the main thread.
    sys.exit( 0 )

def handle_siginfo( signum, stack ):
    """
    This function is called when the user sends a SIGINFO message to
    the main thread. SIGINFO is sent when a user on a Mac OS X or FreeBSD
    system hits Ctrl-T while the program is running. It is supposed to
    return some information about the process of a long running task, or
    information about the program being run.
    """
    logger = logging.getLogger( __name__ )
    logger.info( "SIGINFO received." )

    pass
