class MCSCamera():
    """
    Abstraction of a MCS Camera node on the network. 
    """
    def __init__( self, ip_addr, port ):
        self.ip_addr = ip_addr
        self.port = port

