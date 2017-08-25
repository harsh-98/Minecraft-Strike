# Minecraft-Strike

>Inspired by the [project](https://github.com/fogleman/Minecraft). 

This game is developed using python and [pyglet](https://bitbucket.org/pyglet/pyglet/wiki/Home) just like the original project by [fogleman](https://github.com/fogleman/).
Now the game is multiplayer and new levels have been added.
![Air view](https://raw.githubusercontent.com/h4r5h-ja1n/Minecraft-Strike/city/MC-Srtike.png)
![Ground view](https://raw.githubusercontent.com/h4r5h-ja1n/Minecraft-Strike/city/MC-Strike2.png)

For client-server scripting, I have used a self-modified version of [PodSixNet](https://github.com/chr15m/PodSixNet).

## How to install

>git clone https://github.com/h4r5h-ja1n/Minecraft-Strike.git

>cd Minecraft-Strike

>pip install -r requirements.txt (__PodSixNet default code will not, since I am using a slightly modified version of it you can refer this [PR](https://github.com/chr15m/PodSixNet/pull/7)__)


## How to run the Game

    python server.py `#for starting the server`
    python main_new.py `#for starting the client, the default ip and port are 127.0.0.1 and 31425`

## Just wanted to play the Game
   
### FOR LINUX

    git clone -b distro git@github.com:h4r5h-ja1n/Minecraft-Strike.git
    python server.py 
    
The client-side game is available in `main_new` folder by the name `main_new`.
In the distro branch, there is the compiled game with all the python libs required the game.

__This compiled code only works on the LINUX not on WINDOWS and haven't been tested on the MAC__


## How to Play

### Moving

- W: forward
- S: back
- A: strafe left
- D: strafe right
- Mouse: look around
- Space: jump
- Tab: toggle flying mode

### Building

- Selecting type of block to create:
    - 1: brick
    - 2: grass
    - 3: sand
- Mouse left-click: remove block
- Mouse right-click: create block

### Quitting

- ESC: release mouse, then close window
