# This file is called bestsutter.py
import usb.core
import usb.util
from struct import *
import sys
sys.path.insert(0, "/Users/justinemajor/Documents/gph.doc/git/PyHardwareLibrary/hardwarelibrary/communication")
import serialport

class SutterDevice:
    def __init__(self):
      """
      SutterDevice represents a XYZ stage.  
      """
      self.device = usb.core.find(idVendor=4930, idProduct=1)
      self.configuration = None
      self.interface = None
      self.outputEndpoint = None
      self.inputEndpoint = None

      self.microstepsPerMicrons = 16

    def initializeDevice(self):
      """
      We do a late initialization: if the device is not present at creation, it can still be
      initialized later.
      """

      if self.device is not None:
        return
      
      self.device = usb.core.find(idVendor=4930, idProduct=1) 
      if self.device is None:
        raise IOError("Can't find Sutter device")

      self.device.set_configuration()        # first configuration
      self.configuration = self.device.get_active_configuration()  # get the active configuration
      self.interface = self.configuration[(0,0)]  # pick the first interface (0) with no alternate (0)

      self.outputEndpoint = self.interface[0] # First endpoint is the output endpoint
      self.inputEndpoint = self.interface[1]  # Second endpoint is the input endpoint
    
    def shutdownDevice(self):
      """
      If the device fails, we shut everything down. We should probably flush the buffers also.
      """
      
      self.device = None
      self.configuration = None
      self.interface = None
      self.outputEndpoint = None
      self.inputEndpoint = None
      
    def sendCommand(self, commandBytes):
      """ The function to write a command to the endpoint. It will initialize the device 
      if it is not alread initialized. On failure, it will warn and shutdown."""
      try:
        if self.outputEndpoint is None:
          self.initializeDevice()
          
        self.outputEndpoint.write(commandBytes)
      except Exception as err:
        print('Error when sending command: {0}'.format(err))
        self.shutdownDevice()
    
    def readReply(self, size, format) -> tuple:
      """ The function to read a reply from the endpoint. It will initialize the device 
      if it is not already initialized. On failure, it will warn and shutdown. 
      It will unpack the reply into a tuple, and will remove the b'\r' that is always present.
      """

      try:
        if self.outputEndpoint is None:
          self.initializeDevice()

        replyBytes = inputEndpoint.read(size_or_buffer=size)
        theTuple = unpack(format, replyBytes)
        if theTuple[-1] != b'\r':
           raise RuntimeError('Invalid communication')
        return theTuple[:-1] # We remove the last character
      except Exception as err:
        print('Error when reading reply: {0}'.format(err))
        self.shutdownDevice()
        return None
      
    def positionInMicrosteps(self) -> (int,int,int):
      """ Returns the position in microsteps """
      commandBytes = bytearray(b'C\r')
      self.outputEndpoint.write(commandBytes)
      return self.readReply(size=13, format='<lllc')
  
    def moveInMicrostepsTo(self, position):
      """ Move to a position in microsteps """
      x,y,z  = position
      commandBytes = pack('<clllc', ('M', x, y, z, '\r'))
      self.outputEndpoint.write(commandBytes)
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

      x,y,z  = position
      positionInMicrosteps = (x*self.microstepsPerMicrons, 
                              y*self.microstepsPerMicrons,
                              z*self.microstepsPerMicrons)
      
      self.moveInMicrostepsTo(self.positionInMicrosteps())

    def moveBy(self, delta) -> bool:
      """ Move by a delta displacement (dx, dy, dz) from current position in microns """

      dx,dy,dz  = delta
      position = self.position()
      if position is not None:
          x,y,z = position
          self.moveTo( (x+dx, y+dy, z+dz) )

if __name__ == "__main__":
    device = SutterDevice()

    #print(device.position())

    device.initializeDevice()
    #x,y,z = device.position()
    #device.moveTo( (x+10, y+10, z+10) )
    serialport.SerialPort().writeData(device.moveBy( (-10, -10, -10) ))
    device.sendCommand(device.moveBy( (-10, -10, -10) ))