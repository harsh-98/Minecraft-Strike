from PodSixNet.Channel import Channel
import time
class ClientChannel(Channel):

    def Network(self, data):
        print data
    
    def Network_myaction(self, data):
        print "myaction:", data
    def Network_key(self, data):
        print "ker_p"
        self._server.key_handle(data,"keyPress")
    def Network_keyR(self, data):
        print "ker_r"
        self._server.key_handle(data,"keyPR")
    def Network_mouse(self, data):
        print "mouse"
        self._server.key_handle(data,"mouse_")
    def Network_mouse_m(self, data):
        print "mouse"
        self._server.key_handle(data,"mouse_r")

from PodSixNet.Server import Server

class MyServer(Server):
    
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):

        #Call the super constructor
        Server.__init__(self, *args, **kwargs)

        #Create the objects to hold our game ID and list of running games
        self.games = []
        self.player_arr=[]
        self.queue = None
        self.gameIndex = 0
        self.plyr_id=0
        #Set the velocity of our player
      #  self.velocity = 5

    #Function to deal with new connections
    def Connected(self, channel, addr):
        self.player_arr.append(self.plyr_id)
        print("New connection: {}".format(channel))
        channel.Send({"action":"init","player":self.plyr_id,"player_arr":self.player_arr})
        self.plyr_id+=1
        print "init sent"
        #When we receive a new connection
        #Check whether there is a game waiting in the queue
        if self.queue == None:
            #If there isn't someone queueing
            #Set the game ID for the player channel
            #Add a new game to the queue
            self.queue = Game(channel, self.gameIndex)
            channel.gameID = self.gameIndex

        else:

            #Set the game index for the currently connected channel
            channel.gameID = self.gameIndex
            #Set the second player channel
            self.queue.player_channels.append(channel)
        print self.player_arr
        for i in range(0, len(self.queue.player_channels)-1):
            self.queue.player_channels[i].Send({"action":"add","player":self.plyr_id})
             #   self.queue.player_channels[i].Send({"action":"add","player":self.plyr_id,"gameID":self.queue.gameID})

            #add the game to the end of the game list
            #self.games.append(self.queue)

            #Empty the queue ready for the next connection
            #Increment the game index for the next game
            


    def key_handle(self, data,action):
#        g = self.games[data["gameID"]]#
#

#        for i in range(len(g.player_channels)):
#                g.player_channels[i].Send({"action":"keyPress","player":data["player"],"type":data["type"],"extras":data["extras"]})
        for i in range(len(self.queue.player_channels)):
            if not i == data["player"]:
                self.queue.player_channels[i].Send({"action":action,"player":data["player"],"type":data["type"],"extras":data["extras"]})




#Create the game class to hold information about any particular game
class Game(object):

    #Constructor
    def __init__(self, player, gameIndex):

        #Store the network channel of the first client
        self.player_channels = [player]

        #Set the game id
        self.gameID = gameIndex

myserver = MyServer()
while True:
    myserver.Pump()
    time.sleep(0.0001)

