import sys
import math
import random
import time
import threading
import variable as var_
from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup
from pyglet.window import key, mouse
import  model as mod_
import player as plyr_
from PodSixNet.Connection import ConnectionListener#, connection
import pyglet.app as app_
#player health is defined in three files player,server,window
class Window(pyglet.window.Window, ConnectionListener):

    def __init__(self,ip = "127.0.0.1",port = 31425, *args, **kwargs):
        print kwargs
        print (ip,port)
        super(Window, self).__init__(*args, **kwargs)

#######################################
        self.Connect((ip, port))
        self.player_arr={}
        self.mainid=-1
#######################################




        # Whether or not the window exclusively captures the mouse.
        self.exclusive = False


        # First element is rotation of the player in the x-z plane (ground
        # plane) measured from the z-axis down. The second is the rotation
        # angle from the ground plane up. Rotation is in degrees.
        #
        # The vertical plane rotation ranges from -90 (looking straight down) to
        # 90 (looking straight up). The horizontal rotation range is unbounded.
        self.rotation = (0, 0)

        # health of the player
        self.health = 6
        # Which sector the player is currently in.
        self.sector = None

        # The crosshairs at the center of the screen.
        self.reticle = None

        # Velocity in the y (upward) direction.
        self.dy = 0
        self.pointer=0
        # A list of blocks the player can place. Hit num keys to cycle.
        self.inventory = [var_.BRICK, var_.GRASS, var_.SAND]
        # The current block the user can place. Hit num keys to cycle.
        self.block = self.inventory[0]
        #position for the player stored
        self.position_dict={}
        # Convenience list of num keys.
        self.num_keys = [
            key._1, key._2, key._3, key._4, key._5,
            key._6, key._7, key._8, key._9, key._0]

        # Instance of the model that handles the world.
        self.model = mod_.Model()
       # self.player_arr[self.mainid] = [plyr_.Player(),plyr_.Player()]

        self.running= False

        # The label that is displayed in the top left of the canvas.
        self.label = pyglet.text.Label('', font_name='Arial', font_size=18,
            x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
            color=(0, 0, 0, 255))
        while not self.running:
       #     print self.running
            self.connection.Pump()
            self.Pump()
        # This call schedules the `update()` method to be called
        # var_.TICKS_PER_SEC. This is the main game event loop.
        pyglet.clock.schedule_interval(self.update, 1.0 / var_.TICKS_PER_SEC)
        self.news = None
        self.newh = None
        self.newp = None


    def i(self):
        self.connection.Pump()
        self.Pump()
    def Network_init(self,data):
    #    print "asdfghjk"
        for i in data["player_arr"]:
            self.player_arr[i] = plyr_.Player(i,data["coor"],data["name_dict"][i][0])
            self.pointer=i
        self.mainid=data["player"]
        self.position_dict[data["player"]] = data["coor"]
        self.running = True
        print self.mainid
        print self.player_arr

    def Network_add(self, data):
      #  self.hand = han_.Handler(data['gameID'], data['player'])
        self.pointer+=1
        self.player_arr[self.pointer] = plyr_.Player(data["player"])
       # self.hand.add_player(data['player'])

    def Network_keyPress(self, data):
        self.on_key_press(data['type'],data['extras'],1)
    def Network_keyPR(self, data):
        self.on_key_release(data['type'],data['extras'],1)
    def Network_mouse_(self, data):
        self.on_mouse_press(-1,-1,data['type'],data['extras'],1)
    def Network_mouse_r(self, data):
        self.on_mouse_motion(data['type']["x"],data['type']["y"],data['extras']["dx"],data['extras']["dy"],1)
    def Network_add_b(self, data):
        self.model.add_block(data["position"],data["texture"])
    def Network_remove(self, data):
#        print self.player_arr[data["texture"][0]].health
        if self.mainid == data["texture"][0]:
          #  print data
            self.health-=1
            if self.health == 0:
                pyglet.app.exit()
                self.killer = data["texture"][1]
                self.killed_by = data["player"]
        if data["texture"][0]!=self.mainid :
            self.model.remove_block(data["position"],True,0,self)
        if data["texture"][0] != -1 :
            if self.player_arr[data["texture"][0]].health == 0:
                print("harsh")
                self.news = str(self.player_arr[data["texture"][0]].name)+" was killed by "+data["texture"][1]
            #del self.player_arr[ data["killed_id"]]
    def Network_visible(self, data):
       # self.player_arr[data["player"]].position = data["position"]
      #  print data["position"][0],data["position"][1],data["position"][2],data["player"]
        self.position_dict[data["player"]] = (float(data["position"][0]),data["position"][1]-.25,float(data["position"][2]))
        self.position_render(data["position"][0],data["position"][1],data["position"][2],data["player"])

    def Network_user(self, data):
        self.player_arr[data["player"]].name = data["position"]
    def add_input(self,data):
        self.player_arr[self.mainid].name = data
        self.Send({"action":"username","player":self.mainid,"position":data})


    def set_exclusive_mouse(self, exclusive):
        """ If `exclusive` is True, the game will capture the mouse, if False
        the game will ignore the mouse.

        """
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive


    def get_sight_vector(self):
        """ Returns the current line of sight vector indicating the direction
        the player is looking.

        """
        x, y = self.rotation
        # y ranges from -90 to 90, or -pi/2 to pi/2, so m ranges from 0 to 1 and
        # is 1 when looking ahead parallel to the ground and 0 when looking
        # straight up or down.
        m = math.cos(math.radians(y))
        # dy ranges from -1 to 1 and is -1 when looking straight down and 1 when
        # looking straight up.
        dy = math.sin(math.radians(y))
        dx = math.cos(math.radians(x - 90)) * m
        dz = math.sin(math.radians(x - 90)) * m
        return (dx, dy, dz)

    def get_motion_vector(self):
        """ Returns the current motion vector indicating the velocity of the
        player.

        Returns
        -------
        vector : tuple of len 3
            Tuple containing the velocity in x, y, and z respectively.

        """
        if any(self.player_arr[self.mainid].strafe):
            x, y = self.rotation
            strafe = math.degrees(math.atan2(*self.player_arr[self.mainid].strafe))
            y_angle = math.radians(y)
            x_angle = math.radians(x + strafe)
            if self.player_arr[self.mainid].flying:
                m = math.cos(y_angle)
                dy = math.sin(y_angle)
                if self.player_arr[self.mainid].strafe[1]:
                    # Moving left or right.
                    dy = 0.0
                    m = 1
                if self.player_arr[self.mainid].strafe[0] > 0:
                    # Moving backwards.
                    dy *= -1
                # When you are flying up or down, you have less left and right
                # motion.
                dx = math.cos(x_angle) * m
                dz = math.sin(x_angle) * m
            else:
                dy = 0.0
                dx = math.cos(x_angle)
                dz = math.sin(x_angle)
        else:
            dy = 0.0
            dx = 0.0
            dz = 0.0
        return (dx, dy, dz)

    def update(self, dt):
        """ This method is scheduled to be called repeatedly by the pyglet
        clock.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        """
        self.i()
        self.model.process_queue()
        sector = var_.sectorize(self.player_arr[self.mainid].position)
        if sector != self.sector:
            self.model.change_sectors(self.sector, sector)
            if self.sector is None:
                self.model.process_entire_queue()
            self.sector = sector
        m = 8
        dt = min(dt, 0.2)
        for _ in range(m):
            self._update(dt / m)

    def _update(self, dt):
        """ Private implementation of the `update()` method. This is where most
        of the motion logic lives, along with var_.GRAVITY and collision detection.

        Parameters
        ----------
        dt : float
            The change in time since the last call.

        """
        # walking
        speed = var_.FLYING_SPEED if self.player_arr[self.mainid].flying else var_.WALKING_SPEED
        d = dt * speed # distance covered this tick.
        dx, dy, dz = self.get_motion_vector()
        # New position in space, before accounting for var_.GRAVITY.
        dx, dy, dz = dx * d, dy * d, dz * d
        # var_.GRAVITY
        if not self.player_arr[self.mainid].flying:
            # Update your vertical speed: if you are falling, speed up until you
            # hit terminal velocity; if you are jumping, slow down until you
            # start falling.
            self.dy -= dt * var_.GRAVITY
            self.dy = max(self.dy, -var_.TERMINAL_VELOCITY)
            dy += self.dy * dt
        # collisions
        x, y, z = self.player_arr[self.mainid].position
        x, y, z = self.collide((x + dx, y + dy, z + dz), var_.PLAYER_HEIGHT)

      #  vertex_data = var_.cube_vertices(x+4, y+4, z+4, 0.5)
        self.player_arr[self.mainid].position = (x, y, z)
        #print self.position_dict[self.mainid],self.player_arr[self.mainid].position

        if self.position_dict[self.mainid] != self.player_arr[self.mainid].position:
            self.checker((x,y,z))
        #    self.position_render(x, y, z,self.mainid)
            self.Send({"action":"coor","player":self.mainid,"position":(x, y, z)})
            self.position_dict[self.mainid]=self.player_arr[self.mainid].position

    def position_render(self,x,y,z,id_):

      #  print(self.player_arr[id_].previous)
        vertex_data = var_.cube_vertices(x, y, z, 0.5)
        if self.player_arr[id_].previous != None :
            self.player_arr[id_]._shown1.pop(self.player_arr[id_].previous).delete()
            del self.model.world[var_.normalize(self.player_arr[id_].previous)]
            del self.model.tmp[var_.normalize(self.player_arr[id_].previous)]
         #   print(self.player_arr[self.mainid].previous)
          #  self.model.remove_block(self.player_arr[self.mainid].previous, True, 2)
        self.model.world[var_.normalize((x,y,z))] = var_.arr
        self.player_arr[id_]._shown1[(x, y, z)] = self.model.batch.add(24, GL_QUADS, self.model.group,
            ('v3f/static', vertex_data),
            ('t2f/static', var_.arr))
        self.model.tmp[var_.normalize((x,y,z))] = [(x, y, z),id_]
        self.player_arr[id_].previous = (x, y, z)


    def collide(self, position, height):
        """ Checks to see if the player at the given `position` and `height`
        is colliding with any blocks in the world.

        Parameters
        ----------
        position : tuple of len 3
            The (x, y, z) position to check for collisions at.
        height : int or float
            The height of the player.

        Returns
        -------
        position : tuple of len 3
            The new position of the player taking into account collisions.

        """
        # How much overlap with a dimension of a surrounding block you need to
        # have to count as a collision. If 0, touching terrain at all counts as
        # a collision. If .49, you sink into the ground, as if walking through
        # tall var_.GRASS. If >= .5, you'll fall through the ground.
        pad = 0.25
        p = list(position)
        np = var_.normalize(position)
        for face in var_.FACES:  # check all surrounding blocks
            for i in range(3):  # check each dimension independently
                if not face[i]:
                    continue
                # How much overlap you have with this dimension.
                d = (p[i] - np[i]) * face[i]
                if d < pad:
                    continue
                for dy in range(height):  # check each height
                    op = list(np)
                    op[1] -= dy
                    op[i] += face[i]
                    if tuple(op) not in self.model.world:
                        continue
                    p[i] -= (d - pad) * face[i]
                    if face == (0, -1, 0) or face == (0, 1, 0):
                        # You are colliding with the ground or ceiling, so stop
                        # falling / rising.
                        self.dy = 0
                    break
        return tuple(p)

    def on_mouse_press(self, x, y, button, modifiers,tmp = 0):
        """ Called when a mouse button is pressed. See pyglet docs for button
        amd modifier mappings.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        button : int
            Number representing mouse button that was clicked. 1 = left button,
            4 = right button.
        modifiers : int
            Number representing any modifying keys that were pressed when the
            mouse button was clicked.

        """
        if(tmp == 0):
            self.Send({"action":"mouse","player":self.mainid,"type":button,"extras":modifiers})
        if self.exclusive:
            vector = self.get_sight_vector()
            block, previous = self.model.hit_test(self.player_arr[self.mainid].position, vector)
            if (button == mouse.RIGHT) or \
                    ((button == mouse.LEFT) and (modifiers & key.MOD_CTRL)):
                # ON OSX, control + left click = right click.
                if previous:
                    self.model.add_block(previous, self.block,True,1,self)
            elif button == pyglet.window.mouse.LEFT and block:
                texture = self.model.world[block]
                if texture != var_.STONE:
                    self.model.remove_block(block,True,1,self)
        else:
            self.set_exclusive_mouse(True)

    def on_mouse_motion(self, x, y, dx, dy,tmp =0):
        """ Called when the player moves the mouse.

        Parameters
        ----------
        x, y : int
            The coordinates of the mouse click. Always center of the screen if
            the mouse is captured.
        dx, dy : float
            The movement of the mouse.

        """
        if(tmp == 0):
            self.Send({"action":"mouse_m","player":self.mainid,"type":{"x":x,"y":y},"extras":{"dx":dx,"dy":dy}})
        if self.exclusive:
            m = 0.15
            x, y = self.rotation
            x, y = x + dx * m, y + dy * m
            y = max(-90, min(90, y))
            self.rotation = (x, y)

    def checker(self, position):
       # print(position)
       # print(self.player_arr[self.mainid].flying)
        for  k, v in var_.FEATURES.iteritems():
        #    print(k," ",v)
            if k[0] -2 <position[0]< k[0] + 4 and k[1] -2 <position[1]< k[1] + 4 and k[2] -2 <position[2]< k[2] + 4 and v== "fly":
                self.player_arr[self.mainid].flying = True

                thread=var_.RepeatEvery(self.model,self.player_arr[self.mainid])
                thread.start()
                del var_.FEATURES[k]
                print self
                self.model.remove_block(k,True,1,self)
                break

    def on_key_press(self, symbol, modifiers,tmp=0):
        """ Called when the player presses a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """
        if(tmp == 0):
            self.Send({"action":"key","player":self.mainid,"type":symbol,"extras":modifiers})
        if symbol == key.W:
            self.player_arr[self.mainid].strafe[0] -= 1
        elif symbol == key.S:
            self.player_arr[self.mainid].strafe[0] += 1
        elif symbol == key.A:
            self.player_arr[self.mainid].strafe[1] -= 1
        elif symbol == key.D:
            self.player_arr[self.mainid].strafe[1] += 1
        elif symbol == key.SPACE:
            if self.dy == 0:
                self.dy = var_.JUMP_SPEED
        elif symbol == key.ESCAPE:
            self.set_exclusive_mouse(not self.exclusive)
        elif symbol == key.TAB:
            self.player_arr[self.mainid].flying = not self.player_arr[self.mainid].flying
        elif symbol in self.num_keys:
            index = (symbol - self.num_keys[0]) % len(self.inventory)
            self.block = self.inventory[index]
        #self.checker()

    def on_key_release(self, symbol, modifiers,tmp = 0):
        """ Called when the player releases a key. See pyglet docs for key
        mappings.

        Parameters
        ----------
        symbol : int
            Number representing the key that was pressed.
        modifiers : int
            Number representing any modifying keys that were pressed.

        """
        if(tmp == 0):
            self.Send({"action":"keyR","player":self.mainid,"type":symbol,"extras":modifiers})
        if symbol == key.W:
            self.player_arr[self.mainid].strafe[0] += 1
        elif symbol == key.S:
            self.player_arr[self.mainid].strafe[0] -= 1
        elif symbol == key.A:
            self.player_arr[self.mainid].strafe[1] += 1
        elif symbol == key.D:
            self.player_arr[self.mainid].strafe[1] -= 1

    def on_resize(self, width, height):
        """ Called when the window is resized to a new `width` and `height`.

        """
        # label
        self.label.y = height - 10
        # reticle
        if self.reticle:
            self.reticle.delete()
        x, y = self.width // 2, self.height // 2
        n = 10
        self.reticle = pyglet.graphics.vertex_list(4,
            ('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
        )

    def set_2d(self):
        """ Configure OpenGL to draw in 2d.

        """
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_3d(self):
        """ Configure OpenGL to draw in 3d.

        """
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        x, y = self.rotation
        glRotatef(x, 0, 1, 0)
        glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
      #  print self.mainid
       # print self.player_arr
        x, y, z = self.player_arr[self.mainid].position
        glTranslatef(-x, -y, -z)

    def on_draw(self):
        """ Called by pyglet to draw the canvas.

        """
        self.clear()
        self.set_3d()
        glColor3d(1, 1, 1)
        self.model.batch.draw()
        self.draw_focused_block()
        self.set_2d()
        self.draw_label()
        self.draw_reticle()

    def draw_focused_block(self):
        """ Draw black edges around the block that is currently under the
        crosshairs.

        """
        vector = self.get_sight_vector()
        block = self.model.hit_test(self.player_arr[self.mainid].position, vector)[0]
        if block in self.model.tmp:
            block=self.model.tmp[block]
            t = self.player_arr[block[1]]
            self.newh = str(t.name)+":"+str(t.health)
            block=block[0]
        else:
            self.newh = None
        if block:
            x, y, z = block
            vertex_data = var_.cube_vertices(x, y, z, 0.51)
            glColor3d(0, 0, 0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            self.newp = block

    def draw_label(self):
        """ Draw the label in the top left of the screen.

        """
        x, y, z = self.player_arr[self.mainid].position

#        self.label.text = '%02d (%.2f, %.2f, %.2f) %d / %d   Power : %d sec  %d ,%s' % (
#            pyglet.clock.get_fps(), x, y, z,
#            len(self.model._shown), len(self.model.world),self.model.power_time,self.health,self.player_arr[self.mainid].name)
        self.label.text = ' %s(%.2f, %.2f, %.2f) (Power: %d sec) [Health: %d] %s %s %s' % (
                self.player_arr[self.mainid].name,x, y, z,self.model.power_time,self.health,self.news, self.newh, self.newp)

        self.label.draw()

    def draw_reticle(self):
        """ Draw the crosshairs in the center of the screen.

        """
        glColor3d(0, 0, 0)
        self.reticle.draw(GL_LINES)


