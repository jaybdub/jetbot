import threading
import traitlets
import sys
import zmq
import numpy as np
from Adafruit_MotorHAT import Adafruit_MotorHAT
import atexit


def recv_topic_numpy(socket):
    
    topic, dtype, shape, data = socket.recv_multipart(copy=True)
    import pdb
    shape = tuple([int(s) for s in bytes(shape).decode('utf-8').split(',')])
    buf = memoryview(data)
    array = np.frombuffer(buf, dtype=bytes(dtype).decode('utf-8'))
    return bytes(topic).decode('utf-8'), array.reshape(shape)


class JetBot(traitlets.HasTraits):
    
    camera_image = traitlets.Any(value=np.zeros((224, 224, 3), dtype=np.uint8), default_value=np.zeros((224, 224, 3), dtype=np.uint8))
    left_motor_value = traitlets.Float(default_value=0.0, value=0.0)
    right_motor_value = traitlets.Float(default_value=0.0, value=0.0)
    
    def __init__(self, *args, **kwargs):
        
        # motors
        self._motor_driver = Adafruit_MotorHAT(i2c_bus=1)
        self._left_motor = self._motor_driver.getMotor(1)
        self._right_motor = self._motor_driver.getMotor(2)
        atexit.register(self._release_motors)
        
        # camera
        self._camera_running = False
        self._port = 1807
        self._topic = "image"
        self.start_camera()
        atexit.register(self.stop_camera)
        
    def __del__(self):
        self.stop()
        
    def _run_camera(self):
        
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self._topic)
        self.socket.connect("tcp://localhost:%d" % self._port)
        
        while self._camera_running:
            topic, image = recv_topic_numpy(self.socket)
            self.camera_image = image
            
        self.socket.close()
            
    def start_camera(self):
        if self._camera_running:
            return
        self._camera_running = True
        self._camera_thread = threading.Thread(target=self._run_camera)
        self._camera_thread.start()
        
    def stop_camera(self):
        if not self._camera_running:
            return
        self._camera_running = False
        self._camera_thread.join()
        
    def _release_motors(self):
        self._left_motor.run(Adafruit_MotorHAT.RELEASE)
        self._right_motor.run(Adafruit_MotorHAT.RELEASE)
    
    def _set_left_motor_value(self, value):
        mapped_value = int(255.0 * value)
        speed = min(max(abs(mapped_value), 0), 255)
        self._left_motor.setSpeed(speed)
        if mapped_value < 0:
            self._left_motor.run(Adafruit_MotorHAT.FORWARD)
        else:
            self._left_motor.run(Adafruit_MotorHAT.BACKWARD)
            
    def _set_right_motor_value(self, value):
        mapped_value = int(255.0 * value)
        speed = min(max(abs(mapped_value), 0), 255)
        self._right_motor.setSpeed(speed)
        if mapped_value < 0:
            self._right_motor.run(Adafruit_MotorHAT.FORWARD)
        else:
            self._right_motor.run(Adafruit_MotorHAT.BACKWARD)
        
    def _set_motors(self, left_motor_value, right_motor_value):
        self._set_left_motor(left_motor_value)
        self._set_right_motor_value(right_motor_value)
        
    @traitlets.observe('left_motor_value')
    def _on_left_motor_value(self, change):
        self._set_left_motor_value(change['new'])
        
    @traitlets.observe('right_motor_value')
    def _on_right_motor_value(self, change):
        self._set_right_motor_value(change['new'])
        
    def set_motors(self, left_motor_value, right_motor_value):
        self.left_motor_value = left_motor_value
        self.right_motor_value = right_motor_value
        
    def forward(self, value=1.0, duration=None):
        self.left_motor_value = value
        self.right_motor_value = value

    def backward(self, value=1.0):
        self.left_motor_value = -value
        self.right_motor_value = -value

    def left(self, value=1.0):
        self.left_motor_value = -value
        self.right_motor_value = value

    def right(self, value=1.0):
        self.left_motor_value = value
        self.right_motor_value = -value

    def stop(self):
        self.left_motor_value = 0
        self.right_motor_value = 0