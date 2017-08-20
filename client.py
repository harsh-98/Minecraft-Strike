from PodSixNet.Connection import connection
from time import sleep
# connect to the server - optionally pass hostname and port like: ("mccormick.cx", 31425)
from PodSixNet.Connection import ConnectionListener
class j(ConnectionListener):
    def __init__(self):
        self.Connect()

        #self.i()
    def i(self):
        self.Send({"action":"d"})
        self.Send({"action":"d"})
        connection.Pump()

s=j()

s.i()
s.i()