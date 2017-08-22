from PodSixNet.Channel import Channel
import time
import random
player_arr=[]
player_name={}
class ClientChannel(Channel):

    def Network(self, data):
        pass
      #  print data

#    def Network_key(self, data):
#        print "ker_p"
#        self._server.key_handle(data,"keyPress")
#    def Network_keyR(self, data):
#        print "ker_r"
#        self._server.key_handle(data,"keyPR")
#    def Network_mouse(self, data):
#        print "mouse"
#        self._server.key_handle(data,"mouse_")
#    def Network_mouse_m(self, data):
#        print "mouse"
#        self._server.key_handle(data,"mouse_r")
    def Network_add(self, data):
       # print "add"
        self._server.key_handle2(data, "add_b")
    def Network_rem(self, data):
       # print "remove"
        if  data["texture"] != -1:
            player_arr.remove(data["texture"])
            data["texture"]=[data["texture"],player_name[data["player"]]]
        self._server.key_handle2(data, "remove")
    def Network_coor(self,data):
        self._server.key_handle3(data, "visible")
    def Network_username(self, data):
        print data
        player_name[data["player"]] = data["position"]
        self._server.key_handle3(data, "user")


from PodSixNet.Server import Server
def check(arr_):
        t=random.randint(-10,10)
        if t in arr_ :
            return check(arr_)
        return t

class MyServer(Server):
    
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        #Call the super constructor
        ip,port = "127.0.0.1", 31425
        if 1 == input("yes = 1 or no = 0"):
            ip=raw_input("ip")
            port=input("port")
        Server.__init__(self,None,(ip, port),*args, **kwargs)

        #Create the objects to hold our game ID and list of running games
        self.games = []
        player_arr=[]
        self.queue = None
        self.gameIndex = 0
        self.plyr_id=0
        self.coor = []
        #Set the velocity of our player
      #  self.velocity = 5

    #Function to deal with new connections
    def Connected(self, channel, addr):
      #  print player_arr
        player_arr.append(self.plyr_id)

        print("New connection: {}".format(channel))
        t=check(player_arr)
        self.coor.append(t)
        player_name[self.plyr_id] = None
        print player_name
        channel.Send({"action":"init","player":self.plyr_id,"player_arr":player_arr,"coor":(t,2,t),"name_dict":player_name})
        self.plyr_id+=1
        print (t,15,t)
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
        print player_arr
        for i in range(0, len(self.queue.player_channels)-1):
            self.queue.player_channels[i].Send({"action":"add","player":self.plyr_id})
             #   self.queue.player_channels[i].Send({"action":"add","player":self.plyr_id,"gameID":self.queue.gameID})

            #add the game to the end of the game list
            #self.games.append(self.queue)

            #Empty the queue ready for the next connection
            #Increment the game index for the next game




    def key_handle(self, data,action):
#        g = self.games[data["gameID"]]#
#        for i in range(len(g.player_channels)):
#                g.player_channels[i].Send({"action":"keyPress","player":data["player"],"type":data["type"],"extras":data["extras"]})
        for i in range(len(self.queue.player_channels)):
            if not i == data["player"]:
                self.queue.player_channels[i].Send({"action":action,"player":data["player"],"type":data["type"],"extras":data["extras"]})

    def key_handle2(self, data,action):
        for i in range(len(self.queue.player_channels)):
            if not i == data["player"]:
                self.queue.player_channels[i].Send({"action":action,"player":data["player"],"position":data["position"],"texture":data["texture"]})

    def key_handle3(self, data,action):
        for i in range(len(self.queue.player_channels)):
            if not i == data["player"]:
                self.queue.player_channels[i].Send({"action":action,"player":data["player"],"position":data["position"]})



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

