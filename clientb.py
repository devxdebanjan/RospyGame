import rospy
from std_msgs.msg import String

class PlayerA:
    def __init__(self):
        rospy.init_node('player_b')
        self.player_b_monsters=['Rock','Thunder','Wind']
        self.moves = {}
        self.turn=0
        self.sign=1
        self.row={}
        self.row2={}
        # ROS subscriber for receiving opponent's hitpoints
        rospy.Subscriber('player_b_hitpoints', String, self.receive_opponent_hitpoints)
        rospy.Subscriber('winstat', String, self.receive_winner)

        # ROS publisher for sending moves to the server
        self.pub_moves = rospy.Publisher('player_b_moves', String, queue_size=1)

    #winning message
    def receive_winner(self, data):
        if (data.data=='Player B'):
            print("\nYou Win!!!")
        else:
            print("\nYou Lose:(")

    #receiving data from server of hitpoints of both players
    def receive_opponent_hitpoints(self, data):
        dim=data.data.split("\n")
        self.row=eval(dim[1])
        self.row2=eval(dim[0])
        if(self.sign):
            print('\n')
            for i in range(3):
                if  list(self.row2.values())[i]>0:
                    print(f'{list(self.row2.keys())[i]}:{list(self.row2.values())[i]}')
            print('\n')
            for i in range(3):
                if  list(self.row.values())[i]>0:
                    print(f'{list(self.row.keys())[i]}:{list(self.row.values())[i]}')
            self.sign=0 # Convert string to dictionary

    #asking users to input their moves
    def take_moves_input(self):
        self.turn = self.turn+1
        print('\n')
        print("ROUND ",self.turn)
        if list(self.row.values())[0]<=0:
            a=""
        else:
            a=input("Rock's turn: ")
        if list(self.row.values())[1]<=0:
            b=""
        else:
            b=input("Thunder's turn: ")
        if list(self.row.values())[2]<=0:
            c=""
        else:
            c=input("Wind's turn: ")
    
        moves = a + "," + b + "," + c + ","
        return moves

    #sending moves to server
    def send_moves_to_server(self):
        moves = self.take_moves_input()
        self.pub_moves.publish(moves)

    def play(self):
        rate = rospy.Rate(0.5)
        while not rospy.is_shutdown():
            if not self.sign:
                self.send_moves_to_server()
                self.sign=1
            rate.sleep()

if __name__ == '__main__':
    player_b = PlayerA()
    player_b.play()
