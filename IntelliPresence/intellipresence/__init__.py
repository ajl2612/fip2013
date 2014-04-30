"""
This file contains the entry point and signal handlers for the program.
"""
import signal
import sys
import time
from intellipresence.hal.mcs.camera import Camera
from intellipresence.hal.mcs.thread_server import NetworkThread
from intellipresence.armiture import Armiture
from intellipresence.controller import Controller

def main():
    """
    The starting point for the program.
    """
    # Register handlers for various Unix signals. Signals are used to perform
    # Interprocess Communication in Unix-like operating systems; In this case,
    # we're handling IPC from a bash shell (ie. The user killing the program).
    register_signal_handlers()

    # TODO: Perform armiture configuration here.

    # TODO: Configure AMET here.

    # TODO: Configure the controller here.

    # TODO: Kick things off here.

    # Put the thread to sleep until the user hits ctrl-C.
    while( True ):
        time.sleep(1)

def thread_test():
        cam1 = Camera(0, 0, 0, 0, "RED2", "", 8091 )
        cam2 = Camera(0, 0, 0, 0, "RED6", "", 8092 )
        cam3 = Camera(0, 0, 0, 0, "RED3", "", 8093 )
        cam4 = Camera(0, 0, 0, 0, "RED5", "", 8094 )
        
        arm1 = Armiture( 1, cam1, "", 8091, None, None, None)
        arm2 = Armiture( 2, cam2, "", 8092, None, None, None)
        arm3 = Armiture( 3, cam3, "", 8093, None, None, None)
        arm4 = Armiture( 4, cam4, "", 8094, None, None, None)
        
        armList = {arm1, arm2, arm3, arm4}

        controller = Controller( armList )
        
        while( True ):
            arm1Det = arm1.isFaceDetected()
            arm1Val = arm1.getMCSFaceArea()
            arm2Det = arm2.isFaceDetected()
            arm2Val = arm2.getMCSFaceArea()
            arm3Det = arm3.isFaceDetected()
            arm3Val = arm3.getMCSFaceArea() 
            arm4Det = arm4.isFaceDetected()
            arm4Val = arm4.getMCSFaceArea() 

            print( "Armiture 1: {0} {1}, Armiture 2: {2} {3}, Armiture 3 {4} {5}, Armiture 4 {6} {7}".format(arm1Det, arm1Val, arm2Det, arm2Val, arm3Det, arm3Val, arm4Det, arm4Val ) )
            camRanks = controller.camera_ranks()
            #print( camRanks )
            print( "ARM {0} BEST".format(camRanks[0][1] ) )
            time.sleep(1)
       



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
    print( "\nReceived SIGINT - Shutting down!" )

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
    print( "sup." )
    pass
