import rospy
from std_msgs.msg import String

class GameServer:
    def __init__(self):
        rospy.init_node('game_server')
        self.player_a_hitpoints = {'Fire': 300, 'Water': 400, 'Earth': 500}
        self.player_b_hitpoints = {'Rock': 300, 'Thunder': 400, 'Wind': 500}
        self.current_player = 'A'
        self.player_a_moves = []
        self.player_b_moves = []
        self.winner = None
        self.c1=1

        # ROS subscribers for receiving moves from players
        rospy.Subscriber('player_a_moves', String, self.receive_player_a_moves)
        rospy.Subscriber('player_b_moves', String, self.receive_player_b_moves)

        # ROS publishers for sending monster hitpoints to players
        self.pub_player_a_hitpoints = rospy.Publisher('player_a_hitpoints', String, queue_size=1)
        self.pub_player_b_hitpoints = rospy.Publisher('player_b_hitpoints', String, queue_size=1)
        self.winpub = rospy.Publisher('winstat',String,queue_size=1)

    #printing moves of player a
    def amove(self):
        print(f"Round {self.c1}:\n")    #printing round no
        for i in range(3):
            if list(self.player_a_hitpoints.values())[i]<=0:
                continue
            else:
                if self.player_a_moves[i] == '1':
                    print(list(self.player_a_hitpoints.keys())[i]+" attacked all")
                else:
                    print(list(self.player_a_hitpoints.keys())[i]+" attacked "+self.player_a_moves[i][2:])
        print("\n")
        self.c1+=1

    #printing moves of player b
    def bmove(self):
        for i in range(3):
            if list(self.player_b_hitpoints.values())[i]<=0:
                continue
            else:
                if self.player_b_moves[i] == '1':
                    print(list(self.player_b_hitpoints.keys())[i]+" attacked all")
                else:
                    print(list(self.player_b_hitpoints.keys())[i]+" attacked "+self.player_b_moves[i][2:])
        print("\n")


    #calculating damage of player b after player a move
    def bdamage(self):
        damage={'Rock': 0, 'Thunder': 0, 'Wind': 0}
        for i in range(3):
            m= 300 if (i==0) else (400 if (i==1) else 500)
            if list(self.player_a_hitpoints.values())[i]<=0:
                continue
            else:
                if self.player_a_moves[i] == '1':
                    damage['Rock']+=0.1*m
                    damage['Thunder']+=0.1*m
                    damage['Wind']+=0.1*m
                else:
                    x=self.player_a_moves[i].split()
                    damage[x[1]]+=0.2*m
        return(damage)
    
    #calculating damage of player a after player b move
    def adamage(self):
        damage={'Fire': 0, 'Water': 0, 'Earth': 0}
        for i in range(3):
            m= 300 if (i==0) else (400 if (i==1) else 500)
            if list(self.player_b_hitpoints.values())[i]<=0:
                continue
            else:
                if self.player_b_moves[i] == '1':
                    damage['Fire']+=0.1*m
                    damage['Water']+=0.1*m
                    damage['Earth']+=0.1*m
                else:
                    x=self.player_b_moves[i].split()
                    damage[x[1]]+=0.2*m
        return(damage)

    def receive_player_a_moves(self, data):
        moves = data.data.split(',')
        self.player_a_moves = moves
        # Update hitpoints based on moves received
        self.update_hitpoints()
        self.amove()
        # Switch players
        self.current_player = 'B'

    def receive_player_b_moves(self, data):
        moves = data.data.split(',')
        self.player_b_moves = moves
        # Update hitpoints based on moves received
        self.update_hitpoints()
        self.bmove()
        self.current_player = 'A'

    def update_hitpoints(self):
        if self.current_player == 'A':
            bdamage=self.bdamage()
            for element,damage in bdamage.items():
                self.player_b_hitpoints[element]-=damage
        else:
            adamage=self.adamage()
            for element,damage in adamage.items():
                self.player_a_hitpoints[element]-=damage

    def check_winner(self):
        if all(hp <= 0 for hp in self.player_a_hitpoints.values()):
            self.winner = 'Player B'
            return True
        elif all(hp <= 0 for hp in self.player_b_hitpoints.values()):
            self.winner = 'Player A'
            return True
        return False

    def play_game(self):
        rate = rospy.Rate(0.5)
        while not rospy.is_shutdown():
            # Send hitpoints to players
            if self.current_player == 'A':
                self.pub_player_a_hitpoints.publish(str(self.player_a_hitpoints)+'\n'+str(self.player_b_hitpoints))
            else:
                self.pub_player_b_hitpoints.publish(str(self.player_a_hitpoints)+'\n'+str(self.player_b_hitpoints))
            rate.sleep()
            # Check for winner
            if self.check_winner():
                print(f'{self.winner} wins!')
                self.winpub.publish(self.winner)
                break
                
        rospy.spin()
            
if __name__ == '__main__':
    server = GameServer()
    server.play_game()
    
