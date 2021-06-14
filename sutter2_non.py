# This file is called bettersutter.py
import usb.core
import usb.util
from struct import *

class SutterDevice:
    def __init__(self):
        self.device = usb.core.find(idVendor=4930, idProduct=1) 

        if device is None:
    	    raise IOError("Can't find Sutter device")

        self.device.set_configuration()        # first configuration
        self.configuration = self.device.get_active_configuration()  # get the active configuration
        self.interface = self.configuration[(0,0)]  # pick the first interface (0) with no alternate (0)

        self.outputEndpoint = self.interface[0] # First endpoint is the output endpoint
        self.inputEndpoint = self.interface[1]  # Second endpoint is the input endpoint

        self.microstepsPerMicrons = 16

    def positionInMicrosteps(self) -> (int,int,int):
        commandBytes = bytearray(b'C\r')
        outputEndpoint.write(commandBytes)

        replyBytes = inputEndPoint.read(size_or_buffer=13)
        x,y,z, lastChar = unpack('<lllc', replyBytes)

        if lastChar == b'\r':
            return (x,y,z)
        else:
            return None
  
    def moveInMicrostepsTo(self, position) -> bool:
        x,y,z = position
        commandBytes = pack('<clllc', ('M', x, y, z, '\r'))
        outputEndpoint.write(commandBytes)

        replyBytes = inputEndPoint.read(size_or_buffer=1)
        lastChar = unpack('<c', replyBytes)

        if lastChar != b'\r':
            return True

        return False
    
    def position(self) -> (float, float, float):
        position = self.positionInMicrosteps()
        if position is not None:
            return (position[0]/self.microstepsPerMicrons, 
                    position[1]/self.microstepsPerMicrons,
                    position[2]/self.microstepsPerMicrons)
        else:
            return None
      
    def moveTo(self, position) -> bool:
        x,y,z  = position
        positionInMicrosteps = (x*self.microstepsPerMicrons, 
                                y*self.microstepsPerMicrons,
                                z*self.microstepsPerMicrons)
        
        return self.moveInMicrostepsTo( positionInMicrosteps)

    def moveBy(self, delta) -> bool:
        dx,dy,dz  = delta
        position = self.position()
        if position is not None:
            x,y,z = position
            return self.moveTo( (x+dx, y+dy, z+dz) )
        return True

if __name__ == "__main__":
    device = SutterDevice()

    print(device.device)

    x,y,z = device.position()
    device.moveTo((x+10, y+10, z+10))
    device.moveBy((-10, -10, -10))
