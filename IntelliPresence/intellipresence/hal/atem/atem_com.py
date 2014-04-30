#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import socket
import struct
import sys
import collections
import logging
import binascii

def dumpHex (buffer):
    logger = logging.getLogger( __name__ )

    s = ''
    for c in buffer:
        s += str( hex( c ) ) + ' '
    logger.debug(s)

def dumpAscii (buffer):
    logger = logging.getLogger( __name__ )

    s = ''
    for c in buffer:
        if (c>=0x20)and(c<=0x7F):
            s+=str(c)
        else:
            s+='.'
    logger.debug(s)

def byte_to_hex_string( byte_array ):
    return "".join( map( lambda b: format( b, "02x" ), byte_array ) )

# implements communication with atem switcher
class AtemCom :

    # size of header data
    SIZE_OF_HEADER = 0x0c

    # packet types
    CMD_NOCOMMAND   = 0x00
    CMD_ACKREQUEST  = 0x01
    CMD_HELLOPACKET = 0x02
    CMD_RESEND      = 0x04
    CMD_UNDEFINED   = 0x08
    CMD_ACK         = 0x10

    # initializes the class
    def __init__ (self, socket_ip, socket_port) :
        self.socket = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking (0)
        self.socket.bind((socket_ip, socket_port))
   
    # hello packet
    def connectToSwitcher (self, address) :
        logger = logging.getLogger( __name__ )
        logger.info( "Attempting connection to ATEM Switch @ {}".format( address ) )

        self.address = address
        self.packetCounter = 0
        self.isInitialized = False
        self.currentUid = 0x1337 # Arbitrary
       
        payload_size = 8
        datagram = self.createCommandHeader( self.CMD_HELLOPACKET, payload_size, self.currentUid, 0x0 )
        struct.pack_into( '!I', datagram, self.SIZE_OF_HEADER, 0x01000000 )
        struct.pack_into( '!I', datagram, self.SIZE_OF_HEADER + 4, 0x00 )

        self.sendDatagram( datagram )

    # reads packets sent by the switcher
    def handleSocketData (self) :
        logger = logging.getLogger( __name__ )

        # network is 100Mbit/s max, MTU is thus at most 1500
        try :
            d = self.socket.recvfrom (2048)
        except socket.error:
            return False
        
        datagram, server = d
        logger.info('Received datagram from ATEM: {}'.format( datagram ) )

        header = self.parseCommandHeader(datagram)
        if header :
            self.currentUid = header['uid']
            
            if header['bitmask'] & self.CMD_HELLOPACKET :
                logger.info('not initialized, received HELLOPACKET, sending ACK packet')
                self.isInitialized = False
                ackDatagram = self.createCommandHeader (self.CMD_ACK, 0, header['uid'], 0x0)
                self.sendDatagram (ackDatagram)
            elif self.isInitialized and (header['bitmask'] & self.CMD_ACKREQUEST) :
                logger.info('initialized, received ACKREQUEST, sending ACK packet')
                ackDatagram = self.createCommandHeader( self.CMD_ACK, 0, header['uid'], header['packageId'] )
                self.sendDatagram (ackDatagram)
            
            if ((len(datagram) > (self.SIZE_OF_HEADER + 2)) and (not (header['bitmask'] & self.CMD_HELLOPACKET))) :
                self.parsePayload (datagram)

        return True        

    def waitForPacket(self):
        logger = logging.getLogger( __name__ )

        logger.debug(">>> waiting for packet")
        while (not self.handleSocketData()) :
            pass
        logger.debug(">>> packet obtained")

    # generates packet header data
    def createCommandHeader (self, bitmask, payloadSize, uid, ackId) :
        data = bytearray( payloadSize + self.SIZE_OF_HEADER )
        packageId = 0

        if (not (bitmask & (self.CMD_HELLOPACKET | self.CMD_ACK))) :
            self.packetCounter+=1
            packageId = self.packetCounter
    
        val = bitmask << 11
        val |= (payloadSize + self.SIZE_OF_HEADER)
        
        struct.pack_into( '!H', data, 0, val )
        struct.pack_into( '!H', data, 2, uid )
        struct.pack_into( '!H', data, 4, ackId )
        struct.pack_into( '!I', data, 6, 0 )
        struct.pack_into( '!H', data, 10, packageId )

        return data

    # parses the packet header
    def parseCommandHeader (self, datagram) :
        logger = logging.getLogger( __name__ )
        header = {}

        if (len(datagram)>=self.SIZE_OF_HEADER) :
            logger.debug( str( len( datagram ) ) )
            header['bitmask'] = struct.unpack('B',datagram[0:1])[0] >> 3
            header['size'] = struct.unpack('!H',datagram[0:2])[0] & 0x07FF
            header['uid'] = struct.unpack('!H',datagram[2:4])[0]
            header['ackId'] = struct.unpack('!H',datagram[4:6])[0]
            header['packageId']=struct.unpack('!H',datagram[10:12])[0]
            logger.info( "Received header: " + str( header ) )
            return header
        return False

    def parsePayload (self, datagram) :
        logger = logging.getLogger( __name__ )
        logger.debug('parsing payload')

        # eat up header
        datagram = datagram[self.SIZE_OF_HEADER:]
        
        # handle data
        while (len(datagram)>0) :
            size = struct.unpack('!H',datagram[0:2])[0]
            packet = datagram[0:size]
            datagram = datagram[size:]
            # skip size and 2 unknown bytes
            packet = packet[4:]
            ptype = packet[:4]
            payload = packet[4:]
            # find the approporiate function in the class
            method = 'pkt' + ptype.decode( 'ascii' )
            if method in dir(self) :
                func = getattr(self, method)
                if isinstance(func, collections.Callable) :
                    logger.debug( "Method: " +  method )
                    func(payload)
                else:
                    logger.warning( 'problem, member {} not callable'.format( method ) )
            else :
                logging.warning( 'unknown type ' + ptype.decode( 'utf-8' ) )
                #dumpAscii(payload)

        #sys.exit()

    def sendCommand (self, command, payload) :
        logger = logging.getLogger( __name__ )
        logger.info( "Sending command to ATEM: {}:{}".format( command, payload ) )

        size = len(command) + len(payload) + 4
        logger.info( "Size: {}".format( size ) )
        dg = self.createCommandHeader( self.CMD_ACKREQUEST, size, self.currentUid, 0 )
        
        struct.pack_into( '!H', dg, self.SIZE_OF_HEADER, size )
        struct.pack_into( '!H', dg, self.SIZE_OF_HEADER + 2, 0 )

        offset = self.SIZE_OF_HEADER + 4
        for c in command:
            struct.pack_into( '!c', dg, offset, bytes( c, 'ascii' ) )
            offset += 1

        for c in payload:
            struct.pack_into( '!c', dg, offset, bytes( c, 'ascii' ) )
            offset += 1

        logger.warning( byte_to_hex_string( dg ) )

        #dg += struct.pack('!H', size)
        #dg += "\x00\x00".encode( 'utf-8' )
        #dg += command.encode( 'utf-8' )
        #dg += payload.encode( 'utf-8' ) 
        
        self.sendDatagram( dg )

    # sends a datagram to the switcher
    def sendDatagram (self, datagram) :
        logger = logging.getLogger( __name__ )
        logger.info( "Sending datagram to ATEM: {}".format( byte_to_hex_string( datagram ) ) )
        self.socket.sendto( datagram, self.address )

    def pkt_ver (self, data) :
        logger = logging.getLogger( __name__ )

        major, minor = struct.unpack('!HH', data)
        self.version = str(major)+'.'+str(minor)
        logger.debug('version '+self.version)

    def pkt_pin (self, data) :
        self.productInformation = data

    def pkt_top (self, data) :
        pass

    def pkt_MeC (self, data) :        
        pass

    def pkt_mpl (self, data) :
        pass

    def pkt_MvC (self, data) :
        pass         
    
    def pkt_AMC (self, data) :
        pass

    def pktPowr (self, data) :
        pass

    def pktDskS (self, data) :
        pass

    def pktColV (self, data) :
        pass

    def pktMPSE (self, data) :
        pass

    def pktVidM (self, data) :
        dumpHex (data)
        dumpAscii (data)
        self.videoFormat = data

    def pktInPr (self, data) :
        logger = logging.getLogger( __name__ )
        dumpHex (data)
        dumpAscii (data)
        input_ = {}
        input_['index'] = struct.unpack('B', data[0:1])[0]
        pos = data[1:].find(b'\0')
        if (pos==-1) :
            logger.info( "can\'t find \'\\x0\'" )
        input_['longText'] = data[1:pos+1]
        input_['shortText'] = data[21:27]
        logger.debug(input_)

if __name__ == '__main__':
    a = Atem()
    import config
    a.connectToSwitcher ((config.address,9910))
    #while (True):   
    import time
    a.waitForPacket()
    a.waitForPacket()
    a.waitForPacket()
    a.waitForPacket()
    a.waitForPacket()
    a.waitForPacket()
    a.waitForPacket()
    print("sending command")
    a.sendCommand ("DCut", "\x00\x00\x00\x00"); 
    a.waitForPacket()    
        
