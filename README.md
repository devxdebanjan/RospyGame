## AIM
 Design multiplayer game architecture using ROS communication where each player 
has three components (monsters) and attacks each other through two modes 1 and 2. Here 
you will find three files **one for the server**, and **two for clients A and B** respectively.
## OS 
Linux (Distro: Ubuntu)
## LIBRARIES USED
- rospy from ROS Noetic 

## INSTRUCTIONS
- Run the roscore 
- **First run the server node.** 
- Next open clients A and B in any order you would like. Player A will get chance to input 
their moves first and then Player B. 
- This way the game will go on alternatively until winner 
is found. Most important precaution while running the game is that when using move 2 you 
should follow the exact format "2 opponent_monster_name". Here the opponent’s name is case 
sensitive and the program will malfunction if you give any wrong inputs as error handling is yet to be done.
 
For any other discrepancies, please hit me up on my [email](debanjannaskar1@gmail.com)

