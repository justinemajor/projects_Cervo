from struct import *
import sys
import serial
from serial.tools.list_ports import comports
#sys.path.insert(0, "/Users/justinemajor/Documents/gph.doc/git/PyHardwareLibrary/hardwarelibrary/communication")
#from serialport import SerialPort
import time
import array
import os
import serial

#/dev/cu.usbserial-SI8YCLBE
class SutterDevice:
    def __init__(self):
        """
        SutterDevice represents a XYZ stage.  
        """
        
        self.port = serial.Serial("/dev/cu.usbserial-SI8YCLBE", timeout=5, baudrate=128000)

        #ajouter les instances nécessaires

        self.microstepsPerMicrons = 16

    def initializeDevice(self):
        """
        We do a late initialization: if the device is not present at creation, it can still be
        initialized later.
        """
        if self.port is not None:
            return
        
        self.port = serial.Serial("/dev/cu.usbserial-SI8YCLBE", timeout=5, baudrate=128000) 
        if self.port is None:
            raise IOError("Can't find Sutter device")

    def shutdownDevice(self):
        """
        If the device fails, we shut everything down. We should probably flush the buffers also.
        """
        self.port.close()

    def sendCommand(self, commandBytes):
        """ The function to write a command to the endpoint. It will initialize the device 
        if it is not alread initialized. On failure, it will warn and shutdown."""
        try:
            if self.port is None:
                self.initializeDevice()
            
            self.port.write(commandBytes)

        except Exception as err:
            print('Error when sending command: {0}'.format(err))
            self.shutdownDevice()

    def readReply(self, size, format) -> tuple:
        """ The function to read a reply from the endpoint. It will initialize the device 
        if it is not already initialized. On failure, it will warn and shutdown. 
        It will unpack the reply into a tuple.
        """
        try:
            if self.port is None:
                self.initializeDevice()

            replyBytes = self.port.read(size)
            #print(replyBytes)
            theTuple = unpack(format, replyBytes)
            #print(theTuple)
            return theTuple

        except Exception as err:
            print('Error when reading reply: {0}'.format(err))
            self.shutdownDevice()
            return None

    def positionInMicrosteps(self) -> (int,int,int):
        """ Returns the position in microsteps """
        commandBytes = pack('<cc', b'C', b'\r')
        self.sendCommand(commandBytes)
        return self.readReply(size=13, format='<clll')[1:]

    def moveInMicrostepsTo(self, position):
        """ Move to a position in microsteps """
        x,y,z  = position
        commandBytes = pack('<clllc', b'M', int(x), int(y), int(z), b'\r')
        self.sendCommand(commandBytes)
        self.readReply(size=1, format='<c')
    
    def position(self) -> (float, float, float):
        """ Returns the position in microns """

        position = self.positionInMicrosteps()
        if position is not None:
            return (position[0]/self.microstepsPerMicrons, 
                    position[1]/self.microstepsPerMicrons,
                    position[2]/self.microstepsPerMicrons)
        else:
            return None

    def moveTo(self, position):
        """ Move to a position in microns """
        #if not self.port.is_open:
            #self.port.open()
        x,y,z  = position
        positionInMicrosteps = (x*self.microstepsPerMicrons, 
                                y*self.microstepsPerMicrons,
                                z*self.microstepsPerMicrons)
        self.moveInMicrostepsTo(positionInMicrosteps)
        #self.port.close()

    """
    def moveBy(self, delta) -> bool:
        """ Move by a delta displacement (dx, dy, dz) from current position in microns """
        #if not self.port.is_open:
            #self.port.open()
        dx,dy,dz  = delta
        position = self.position()
        if position is not None:
            x,y,z = position
            self.moveTo((x+dx, y+dy, z+dz))
        #self.port.close()
    """


if __name__ == "__main__":
    device = SutterDevice()

    device.moveTo((16000, 16000, 16000))
    #print(device.position())