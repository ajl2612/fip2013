# Configuration for the ATEM.
# adapter refers to the physical adapter that the ATEM is attached to (ie. eth1). 
# port is the port that will be used for the socket that is created at that address.
# atem_addr is the address of the ATEM on the network that adapter is attached to. 
atem = {
    "adapter": "en0",
    "port": 9910,
    "atem_addr": "192.168.10.240",
    "atem_timeout": 30,
}

# Configuration for the motors. TODO: Add this.
motors = {
}

# Configuration for MCS. TODO: Add this.
mcs = {
}
