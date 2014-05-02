"""Uses PyATEM to easily connect python to ATEM switcher, allonwing for easy program changing
Developed explicitly for the Freshman Imaging Project at RIT, 2013-2014.

Author: Noah Kram
copyright: 2014
"""
import atem
import config
import time
import camera
import armiture

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

def camera_ranks(armList):
    """
    Requires the list of armitures
    Determines capture camera with the largest percentage of face
    as given by Facial Detection
    returns the ,ist fo MCS cameras odered by largest face value.
    Face value currently area, to be refined later.
    If no faces are detected, returns an empty list. 
    """
    camList = []
    for arm in armList:
        if arm.isFaceDetected():
            camList.append( (arm.getMCSFaceArea() , arm.getID() ))
        else:
            camList.append( ( 0 , arm.getID() ))
    camList.sort(reverse = True)
    return camList

    
    
if __name__== '__main__':

    #change_program_input(2)
    #change_preview_input(1)
    
    cam1 = camera.Camera(0,0,0,0,"Red2", False) 
    cam2 = camera.Camera(0,0,0,0,"Red3", False)
    cam3 = camera.Camera(0,0,0,0,"Red4", False)
    cam4 = camera.Camera(0,0,0,0,"Red5", False)

    arm1 = armiture.Armiture(1, cam1, "", 8091, None, None, None)
    arm2 = armiture.Armiture(2, cam2, "", 8092, None, None, None)
    arm3 = armiture.Armiture(3, cam3, "", 8093, None, None, None)
    arm4 = armiture.Armiture(4, cam4, "", 8094, None, None, None)
    
    armList = [arm1, arm2, arm3, arm4]

    best_arm = 1

    while(True):
        arm1Det = arm1.isFaceDetected()
        arm1Val = arm1.getMCSFaceArea()
        arm2Det = arm2.isFaceDetected()
        arm2Val = arm2.getMCSFaceArea()
        arm3Det = arm3.isFaceDetected()
        arm3Val = arm3.getMCSFaceArea() 
        arm4Det = arm4.isFaceDetected()
        arm4Val = arm4.getMCSFaceArea() 

        print "Armiture 1: {0} {1}, Armiture 2: {2} {3}, Armiture 3 {4} {5}, Armiture 4 {6} {7}".format(arm1Det, arm1Val, arm2Det, arm2Val, arm3Det, arm3Val, arm4Det, arm4Val ) 
        camRanks = camera_ranks(armList)

        print camRanks
        if( not camRanks[0][0] == 0 ):
            new_best_arm = camRanks[0][1]
            if( not new_best_arm == best_arm ):
                best_arm = new_best_arm
                change_program_input( best_arm)
        print best_arm          
        
        time.sleep(1)
    """ 
    num = 1
    while(True):
        change_program_input(num)
        if (num >= 4):
            num = 1
        else:
            num += 1
        time.sleep(1)
    """
