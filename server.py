#My server.py file
import sys
import cgi
import os
import glob
import math
import phylib
import Physics
import re
import json
from datetime import datetime
import random 
from http.server import HTTPServer, BaseHTTPRequestHandler
from http.server import HTTPServer, BaseHTTPRequestHandler;
from urllib.parse import urlparse, parse_qsl;

global_current_game_name = None
global_current_shooter = None
global_player_high = None
global_player_low = None
global_balls_high_left = list(range(9, 16))  
global_balls_low_left = list(range(1, 8))  
global_game = Physics.Game #Initialize these
global_table = Physics.Table
global_svg_array = []
global_player1Name = None
global_player2Name = None
global_last_table_SVG = None
global_eightBall_sunk = "No, the eight ball has not been sunk yet! Game on!"

#This basis of this code was provided by Lab 2 found in the course 
#content of CIS 2750 specifically labserver.py 

class MyHandler(BaseHTTPRequestHandler):
    #Responses to GET requests
    def do_GET(self):
        global global_current_game_name, global_current_shooter, global_player_high, global_player_low, global_balls_high_left, global_balls_low_left, global_game, global_table, global_svg_array, global_player1Name, global_player2Name, global_last_table_SVG, global_eightBall_sunk
        parsed = urlparse(self.path)
        
        if parsed.path in ['/startPage.html']:
        
            fp = open('.'+parsed.path)
            content = fp.read();

            # generate the headers
            self.send_response( 200 ); # OK
            self.send_header( "Content-type", "text/html" );
            self.send_header( "Content-length", len( content ) );
            self.end_headers();

            # send it to the browser
            self.wfile.write( bytes( content, "utf-8" ) );
            fp.close();
            
        elif parsed.path.startswith('/script.js'):
            # Attempt to serve static files
            filepath = '.' + parsed.path  # Adjust according to your directory structure
            if os.path.isfile(filepath):
                # File exists, serve it
                with open(filepath, 'rb') as file:
                    self.send_response(200)  # OK
                    self.send_header('Content-type', 'application/javascript')
                    self.end_headers()
                    self.wfile.write(file.read())
        
        elif parsed.path in ['/animateShot']:
        
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            global_last_table_SVG = global_svg_array[len(global_svg_array) - 1]
            print(global_last_table_SVG)
            self.wfile.write(json.dumps(global_svg_array).encode('utf-8'))  
            global_svg_array = [] # reset the svg array
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )   
        
    def do_POST(self):

        global global_current_game_name, global_current_shooter, global_player_high, global_player_low, global_balls_high_left, global_balls_low_left, global_game, global_table, global_svg_array, global_player1Name, global_player2Name, global_last_table_SVG, global_eightBall_sunk
        
        # hanle post request
        # parse the URL to get the path and form data
        parsed  = urlparse( self.path );
        if parsed.path in [ '/startGame.html' ]:
            
            #1. Receiving form data from shoot.html
            
            cueBallSunk = "No"
            
            if global_current_game_name == None:
                form = cgi.FieldStorage( fp=self.rfile,
                                        headers=self.headers,
                                        environ = { 'REQUEST_METHOD': 'POST',
                                                    'CONTENT_TYPE': 
                                                    self.headers['Content-Type'],
                                                } 
                                    ); 
            
                global_current_game_name = "Game " + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                global_player1Name = form.getvalue('player1Name')
                global_player2Name = form.getvalue('player2Name')
                
                #Here we will create the table with all the balls in the correct starting position
                global_table = createStartingTable()  
                #Here we will create a new game with the player names that were inputted from the forum page startPage.html
                global_game = Physics.Game(gameName=global_current_game_name, player1Name=global_player1Name, player2Name=global_player2Name)

                # Randomly decide who shoots first
                global_current_shooter = random.choice([global_player1Name, global_player2Name])
                
                #Generate the SVG string for the initial table
                global_last_table_SVG = global_table.svg()
                
            #Logical to check if eightball sunk
            if global_table.eightBall(global_table) == None:
                winner = global_player1Name if global_current_shooter == global_player2Name else global_player2Name
                loser = global_player1Name if global_current_shooter == global_player1Name else global_player2Name
                global_eightBall_sunk = f"Yes, the eight ball has been sunk! Winner Identified! \n Winner: {winner} \n Loser: {loser}"
            
            #Logic for if the cue ball is sunk
            if global_table.cueBall(global_table) == None:
                cueBallSunk = "Yes, resetting cue ball position!"
                global_table += Physics.StillBall(0, Physics.Coordinate(675, 2025))
                global_last_table_SVG = global_table.svg()
            else:
                cueBallSunk = "No"
                     
            #Logic for Switching Player
            if global_current_shooter == global_player1Name:
                global_current_shooter = global_player2Name       
            else:
                global_current_shooter = global_player1Name
                    
            print()   
            htmlContent = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Make a Shot</title>
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.3/jquery.min.js"></script>
                <script src="script.js?"></script>
                <style>
                    body {{
                        font-family: 'Arial', sans-serif;
                        background-color: #f4f4f4;
                        color: #333;
                        text-align: center;
                        margin: 0;
                        padding: 0;
                        box-sizing: border-box;
                    }}

                    #svg-container {{
                        margin: 20px auto;
                        transform: scale(0.5);
                        transform-origin: top left;
                        position: relative;
                        overflow: visible;
                        border: 5px solid #333;
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                        background-color: #fff;
                        display: inline-block;
                    }}

                    div {{
                        margin-bottom: 10px;
                        padding: 10px;
                    }}

                    #firstShooter {{
                        font-weight: bold;
                        color: #d35400;
                    }}

                    #is_cueball_sunk, #is_eightball_sunk {{
                        font-style: italic;
                        color: #2980b9;
                    }}

                    .info-div {{
                        background-color: #ecf0f1;
                        border: 1px solid #bdc3c7;
                        border-radius: 5px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        max-width: 600px;
                        margin: 20px auto;
                        padding: 15px;
                    }}

                    .info-div:not(:last-child) {{
                        margin-bottom: 20px;
                    }}

                    .title {{
                        margin: 0;
                        padding: 0;
                        font-size: 24px;
                        color: #2c3e50;
                        margin-bottom: 10px;
                    }}

                </style>
            <body">
                <!-- Player names placeholders -->
                <div id="player1Name" style="margin-bottom: 20px;">Player 1: {global_player1Name} - HIGH/LOW:  {global_player_high}</div>
                <div id="player2Name" style="margin-bottom: 20px;">Player 2: {global_player2Name} - HIGH/LOW:  {global_player_low}</div>
                <div id="firstShooter" style="font-weight: bold; margin-bottom: 20px;">Current Shooter: {global_current_shooter}</div>
                <div id="is_cueball_sunk" style="margin-bottom: 20px;">Has the cue ball been sunk?: {cueBallSunk}</div>
                <div id="is_eightball_sunk" style="margin-bottom: 20px;">Has the eightball been sunk? {global_eightBall_sunk}</div>
                <div id="svg-container">
                    {global_last_table_SVG}
                </div>              
            </body>
            </html>
            """
            
            
            # Send 200 response
            self.send_response(200)  
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length", str(len(htmlContent)))
            self.end_headers()
            self.wfile.write(bytes(htmlContent, "utf-8"))
            #Reset the last table svg so it can be written again.
            global_last_table_SVG = None
            #Error send 404 response
            
        elif parsed.path == '/make-shot':
            content_length = int(self.headers['Content-Length'])  # Get the size of the data
            post_data = self.rfile.read(content_length)  # Read the incoming data
            
            data = json.loads(post_data.decode('utf-8'))  # Parse the JSON data
            
            #Get the velocity from javascript after mouse up
            velocityX = data.get('velocityX')
            velocityY = data.get('velocityY')
            
            # Update the table with the shot
            
            cueBall = global_table.cueBall(global_table)
            if not cueBall:
                print("Error, Cue Ball not Found in server.py make-shot post request")
                return None
            
            # print(global_table)
            
            #Temporary positions of the cue ball before converting it to rolling ball
            xPos, yPos = cueBall.obj.still_ball.pos.x, cueBall.obj.still_ball.pos.y
            
            #Convert the cueball to a rolling baall
            cueBall.type = phylib.PHYLIB_ROLLING_BALL
            
            #Add the positions and velocities to the new rolling cueball
            cueBall.obj.rolling_ball.pos.x, cueBall.obj.rolling_ball.pos.y = xPos, yPos
            cueBall.obj.rolling_ball.vel.x, cueBall.obj.rolling_ball.vel.y = velocityX, velocityY    
            #Add the ball number to the new rolling ball
            cueBall.obj.rolling_ball.number = 0  
            
            # Calculate the speed of the cueball    
            speedRB = math.sqrt((velocityX * velocityX) + (velocityY * velocityY))    
            
            # Calculate acceleration
            if speedRB > Physics.VEL_EPSILON:
                cueBall.obj.rolling_ball.acc.y = ((velocityX / speedRB) * -1) * Physics.DRAG #FOR REGRADE: fixedc acceleration logic in shoot OVER A DAMN > SIGN I HAD <
                cueBall.obj.rolling_ball.acc.x = ((velocityX / speedRB) * -1) * Physics.DRAG #FOR REGRADE: Fixed acceleration logic in shoot
            else:
                cueBall.obj.rolling_ball.acc.y = 0.0
                cueBall.obj.rolling_ball.acc.x = 0.0                  

            while global_table is not None:

                newTable = global_table.segment()
                
                if newTable is None:
                    break                
                global_svg_array.append(newTable.svg())
                global_table = newTable
            
            if global_player_high == None:
                global_player_high = random.choice(["HIGH", "LOW"])
                if global_player_high == "HIGH":
                    global_player_low = "LOW"
                else:
                    global_player_low = "HIGH"    

                    
            #Add the shot to the database
            # global_game.shoot(global_current_game_name, global_current_shooter, global_table, velocityX, velocityY)
            # Respond to the client
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            response = {'status': 'success'}
            self.wfile.write(json.dumps(response).encode('utf-8'))
                
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) )             

##################################################################################################################################################################################################################

#This function creates the Starting Table
def createStartingTable():
    table = Physics.Table()

    ballPositions = [
                Physics.Coordinate(675, 2025), # Cue Ball (White) 0
                Physics.Coordinate(675, 675),  # Yellow 1
                Physics.Coordinate(645, 622),  # Blue 2
                Physics.Coordinate(614, 569),  # Red 3
                Physics.Coordinate(584, 516),  # Purple 4  
                Physics.Coordinate(797, 463),  # Orange 5
                Physics.Coordinate(614, 463),  # Green   6          
                Physics.Coordinate(706, 516),  # Brown 7
                Physics.Coordinate(675, 569),  # Black  8
                Physics.Coordinate(706, 622),  # Light Yellow 9
                Physics.Coordinate(736, 569),  # Light Blue 10
                Physics.Coordinate(767, 516),  # Pink 11
                Physics.Coordinate(553, 463),  # Medium Purple 12
                Physics.Coordinate(736, 463),  # Light Salmon 13
                Physics.Coordinate(645, 516),  # Light Green 14
                Physics.Coordinate(675, 463),  # Sandy Brown 15
                ]
         
    for ballNum in range(len(ballPositions)):
        table += Physics.StillBall(ballNum, ballPositions[ballNum])        
    
    return table     
####################################################################################################################################################################################################################################################################   
def reset_game_state():
    global global_current_game_name, global_current_shooter, global_player_high, global_player_low, global_balls_high_left, global_balls_low_left, global_game, global_table, global_svg_array, global_player1Name, global_player2Name
    global_current_game_name = None
    global_current_shooter = None
    global_player_high = None
    global_player_low = None
    global_balls_high_left = list(range(9, 16))
    global_balls_low_left = list(range(1, 8))   
    global_game = None
    global_table = None
    global_svg_array = []
    global_player1Name = None
    global_player2Name = None
    print("GLOBAL VARIABLES RESET")
 #Same main found in lab2      
if __name__ == "__main__":
    reset_game_state()
    httpd = HTTPServer( ( 'localhost', int(sys.argv[1]) ), MyHandler );
    print( "Server listing in port:  ", int(sys.argv[1]) );
    httpd.serve_forever();


