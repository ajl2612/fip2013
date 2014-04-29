import netifaces

def is_valid_network_interface( name ):
    """
    Check to see if the network interface exists.
    """
    return name in netifaces.interfaces()

def get_interface_ip_addr( name ):
    """
    Get the IP Address of the interface with the given name.
    """
    interface = netifaces.ifaddresses( name )
    return interface[netifaces.AF_INET][0]['addr']
