import traitlets
from .robot import Robot


class JetBot(Robot):

    camera_image = traitlets.Any()
    left_speed = traitlets.Float(min=0.0, max=0.0, value=0.0)
    right_speed = traitlets.Float(min=0.0, max=0.0, value=0.0)

    def set_motors(self, left_speed, right_speed):
        """Sets the left and right motor values synchronously.
        
        Because left_speed and right_speed generate events separately,
        this method is defined to enable synchronous motor control.  
        By default, this method will set left_speed and right_speed separately,
        to enable functionality if there is not an overloaded instance of this
        method.  If this method is overloaded by a platform, it should 
        
        1. Perform synchronous control of the motors
        2. Set the left_speed and right_speed values accordingly, to ensure 
        any methods linked to these traitlets are called.
        """
        self.left_speed = left_speed
        self.right_speed = right_speed

    def forward(self, speed=1.0):
        """Moves the robot forward."""
        self.set_motors(speed, speed)

    def backward(self, speed=1.0):
        """Moves the robot backward"""
        self.set_motors(-speed, -speed)
        
    def left(self, speed=1.0):
        """Moves the robot left"""
        self.set_motors(-speed, speed)
        
    def right(self, speed=1.0):
        """Moves the robot right."""
        self.set_motors(speed, -speed)

    def stop(self):
        """Stops the robot.
        
        By default, this method will call set_motors(0, 0).  In some instances,
        for example if a platform has braking capabilities, this method may be overloaded.
        If it is overloaded, the overloading function is reponsible for setting
        left_speed and right_speed accordingly, so that all callback functions attached
        to these attributes are updated.
        """
        self.set_motors(speed, -speed)
