import threading
import traitlets
import sys
import zmq
import numpy as np
import atexit
from adafruit_servokit import ServoKit


def recv_topic_numpy(socket):
    
    topic, dtype, shape, data = socket.recv_multipart(copy=True)
    import pdb
    shape = tuple([int(s) for s in bytes(shape).decode('utf-8').split(',')])
    buf = memoryview(data)
    array = np.frombuffer(buf, dtype=bytes(dtype).decode('utf-8'))
    return bytes(topic).decode('utf-8'), array.reshape(shape)


class JetRacer(traitlets.HasTraits):
    
    camera_image = traitlets.Any(value=np.zeros((224, 224, 3), dtype=np.uint8), default_value=np.zeros((224, 224, 3), dtype=np.uint8))
    throttle = traitlets.Float(default_value=0.0, value=0.0)
    steering = traitlets.Float(default_value=0.0, value=0.0)
    
    def __init__(self, *args, **kwargs):
        
        # motors
        self._servo_kit = ServoKit(channels=16, address=0x40)
        self._steering_motor = self.kit.continuous_servo[0]
        self._throttle_motor = self.kit.continuous_servo[1]
        self._steering_gain = -0.65
        self._throttle_gain = 0.8
        
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
    
    def _set_steering(self, value):
        self._steering_motor.throttle = value * self._steering_gain
    
    def _set_throttle(self, value):
        self._throttle_motor.throttle = value * self._throttle_gain
        
    @traitlets.observe('steering')
    def _on_steering(self, change):
        self._set_steering(change['new'])
        
    @traitlets.observe('throttle')
    def _on_throttle(self, change):
        self._set_throttle(change['new'])