import traitlets


class JetBot(Platform):

    camera_image = traitlets.Any()
    left_speed = traitlets.Float(min=0.0, max=0.0, value=0.0)
    right_speed = traitlets.Float(min=0.0, max=0.0, value=0.0)

    def set_motors(self, left_speed, right_speed):
        self.left_speed = left_speed
        self.right_speed = right_speed

    def forward(self, speed=1.0):
        self.left_speed = speed
        self.right_speed = speed

    def backward(self, speed=1.0):
        self.left_speed = -speed
        self.right_speed = -speed

    def left(self, speed=1.0):
        self.left_speed = -speed
        self.right_speed = speed

    def right(self, speed=1.0):
        self.left_speed = speed
        self.right_speed = -speed

    def stop(self):
        self.left_speed = 0.0
        self.right_speed = 0.0
