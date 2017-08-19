import pyglet 
class Player:
    def __init__(self,batch):
        # When flying var_.GRAVITY has no effect and speed is increased.
        self.flying = False
        self.power_time=0
        # Strafing is moving lateral to the direction you are facing,
        # e.g. moving to the left or right while continuing to face forward.
        #
        # First element is -1 when moving forward, 1 when moving back, and 0
        # otherwise. The second element is -1 when moving left, 1 when moving
        # right, and 0 otherwise.
        self.strafe = [0, 0]
        self.batch = batch

        self._shown1 = {}
        # Current (x, y, z) position in the world, specified with floats. Note
        # that, perhaps unlike in math class, the y-axis is the vertical axis.
        self.position = (0, 0, 0)


        self.WALKING_SPEED = 5
        self.FLYING_SPEED = 15       

        self.GRAVITY = 20.0
        self.MAX_JUMP_HEIGHT = 1.0 # About the height of a block.
        # To derive the formula for calculating jump speed, first solve
        #    v_t = v_0 + a * t
        # for the time at which you achieve maximum height, where a is the acceleration
        # due to gravity and v_t = 0. This gives:
        #    t = - v_0 / a
        # Use t and the desired MAX_JUMP_HEIGHT to solve for v_0 (jump speed) in
        #    s = s_0 + v_0 * t + (a * t^2) / 2
    #    self.JUMP_SPEED = math.sqrt(2 * GRAVITY * MAX_JUMP_HEIGHT)
        self.TERMINAL_VELOCITY = 50
        self.pos_dev = {}
        self.previous = None
#      self.t()
#    def t(self):
#        image = pyglet.image.load("images.jpg")
  #
#        sprites = [pyglet.sprite.Sprite(image,image.width/2, image.height/2, batch=self.batch)]
#        sprites[0].x = 3
#        sprites[0].y = 3
#        sprites[0].z = 3
#
