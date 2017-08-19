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
        # Current (x, y, z) position in the world, specified with floats. Note
        # that, perhaps unlike in math class, the y-axis is the vertical axis.
        self.position = (0, 0, 0)
        self.t()

    def t(self):
        image = pyglet.image.load("images.jpg")
  
        sprites = [pyglet.sprite.Sprite(image,image.width/2, image.height/2, batch=self.batch)]
        sprites[0].x = 0
        sprites[0].y = 0
        sprites[0].z = 0

