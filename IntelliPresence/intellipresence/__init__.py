"""
This file contains the entry point and signal handlers for the program.
"""
import signal
import sys
import time

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
