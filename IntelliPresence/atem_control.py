"""Uses PyATEM to easily connect python to ATEM switcher, allonwing for easy program changing
Developed explicitly for the Freshman Imaging Project at RIT, 2013-2014.

Author: Noah Kram
copyright: 2014
"""
import atem
import config
import time


def change_program_input(camInput):
    if (camInput < 1 or camInput > 6):
        raise ValueError(str(camInput),' is an invalid camera number')
    #num = ('0'+str(camInput)).decode('hex')
    send_command("CPgI", "\x00"+chr(camInput)+"\x00\x00")


def change_preview_input(camInput):
    if (camInput < 1 or camInput > 6):
        raise ValueError(str(camInput),' is an invalid camera number')
    #num = ('0'+str(camInput)).decode('hex')
    send_command("CPvI", "\x00"+chr(camInput)+"\x00\x00")


def auto_transition():
    send_command("DAut","\x00\x00\x00\x00")

def send_command(command, payload):
    a = atem.Atem()
    a.connectToSwitcher((config.address, 9910))
    #No idea why, but it only works after waiting for all of these packets.
    a.waitForPacket()
    a.waitForPacket()
    a.waitForPacket()
    a.waitForPacket()
    a.waitForPacket()
    a.waitForPacket()
    a.waitForPacket()

    print('sending command')
    a.sendCommand(command, payload)
    a.waitForPacket()
    time.sleep(1)
    
    
if __name__== '__main__':

    #change_program_input(2)
    #change_preview_input(1)
    #auto_transition()
    
##    import time
##    num = 1
##    while(True):
##        change_program_input(num)
##        if (num >= 3):
##            num = 1
##        else:
##            num += 1
##        time.sleep(1)

    change_program_input(1)
    change_program_input(2)
    change_program_input(3)
    change_preview_input(1)
    auto_transition()
