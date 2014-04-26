class Motor():
    """
    Abstraction of a Motor control node on the network.
    """
    def __init__( self, ip_addr, port ):
        self.ip_addr = ip_addr
        self.port = port
