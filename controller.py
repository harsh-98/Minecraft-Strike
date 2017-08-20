from PodSixNet.Connection import ConnectionListener, connection
import player as plyr_
from time import sleep
class Controller(ConnectionListener):
    def __init__(self):
        self.Connect()
        self.plyr_arr=[]
        self.mainid=-1
        #self.i()
    def i(self):
        connection.Pump()
        self.Pump()
    def Network_init(self,data):
        for i in data["player_arr"]:
            self.player_arr.append(plyr_.Player(i))
        self.mainid=data["player"]

    def Network_add(self, data):
      #  self.hand = han_.Handler(data['gameID'], data['player'])
        self.player_arr.append(plyr_.Player(data["player"]))
       # self.hand.add_player(data['player'])

    def Network_keyPress(self, data):
        

