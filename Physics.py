#Physics.py FILE

import phylib
import sqlite3
import os
import math
################################################################################
# import constants from phylib to global varaibles
BALL_RADIUS = phylib.PHYLIB_BALL_RADIUS

# add more here

BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH
SIM_RATE = phylib.PHYLIB_SIM_RATE
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON
DRAG = phylib.PHYLIB_DRAG
MAX_TIME = phylib.PHYLIB_MAX_TIME
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS
FRAME_RATE = 0.01

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
xmlns="http://www.w3.org/2000/svg"
xmlns:xlink="http://www.w3.org/1999/xlink">
<rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />"""

FOOTER = """</svg>\n"""

################################################################################
# the standard colours of pool balls
# if you are curious check this out:
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN
]


##############################################################################################################################################################
# A3 CREATING SQL TABLES AND STORING AS STRINGS STRINGS

ball = ("""CREATE TABLE IF NOT EXISTS Ball ( 
             		BALLID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             		BALLNO   INTEGER NOT NULL,
             		XPOS    REAL NOT NULL,
             		YPOS    REAL NOT NULL,
             		XVEL    REAL,
             		YVEL    REAL );""")

# Creating a table called TTable
tTable = ("""CREATE TABLE IF NOT EXISTS TTable ( 
             		TABLEID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             		TIME    REAL NOT NULL);""")

# Creating a table called BallTable
ballTable = ("""CREATE TABLE IF NOT EXISTS BallTable ( 
            BALLID INTEGER NOT NULL,
            TABLEID INTEGER NOT NULL,
            FOREIGN KEY (BALLID) REFERENCES Ball(BALLID),
            FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID) );""")

# Creating a table called Shot
Shot = ("""CREATE TABLE IF NOT EXISTS Shot ( 
        SHOTID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        PLAYERID   INTEGER NOT NULL,
        GAMEID    REAL NOT NULL,
        FOREIGN KEY (PLAYERID) REFERENCES Player,
        FOREIGN KEY (GAMEID)  REFERENCES Game         
        );""")

# Creating a table called TableShot
tableShot = ("""CREATE TABLE IF NOT EXISTS TableShot ( 
                SHOTID   INTEGER NOT NULL,
                TABLEID   INTEGER NOT NULL,
                FOREIGN KEY (SHOTID) REFERENCES Shot (SHOTID)
                FOREIGN KEY (TABLEID) REFERENCES TTable (TABLEID));""")

# Creating a table called Game
game = ("""CREATE TABLE IF NOT EXISTS Game ( 
             		GAMEID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             		GAMENAME    VARCHAR(64) NOT NULL);""")

# Creating a table called Player
player = ("""CREATE TABLE IF NOT EXISTS Player ( 
             		PLAYERID   INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
             		GAMEID   INTEGER NOT NULL,
             		PLAYERNAME    VARCHAR(64) NOT NULL,
               FOREIGN KEY (GAMEID) REFERENCES Game (GAMEID)
               
               );""")


tableArray = [ball, tTable, ballTable, Shot, tableShot, game, player]

################################################################################


class Coordinate(phylib.phylib_coord):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass


################################################################################
# Still Ball Python Class
class StillBall(phylib.phylib_object):
    """
    Python StillBall class.
    """

    def __init__(self, number, pos):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_STILL_BALL,
                                      number,
                                      pos, None, None,
                                      0.0, 0.0)

        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall

    def svg(self):
        return """ <circle id="%s_Ball" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (BALL_COLOURS[self.obj.still_ball.number], self.obj.still_ball.pos.x,
                                                                       self.obj.still_ball.pos.y,
                                                                       BALL_RADIUS,
                                                                       BALL_COLOURS[self.obj.still_ball.number])

# Rolling ball python class


class RollingBall(phylib.phylib_object):

    def __init__(self, number, pos, vel, acc):

        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_ROLLING_BALL,
                                      number,
                                      pos, vel, acc,
                                      0.0, 0.0)
        self.__class__ = RollingBall

    def svg(self):
        return """ <circle id="%s_Ball" cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (BALL_COLOURS[self.obj.rolling_ball.number], self.obj.rolling_ball.pos.x,
                                                                       self.obj.rolling_ball.pos.y,
                                                                       BALL_RADIUS,
                                                                       BALL_COLOURS[self.obj.rolling_ball.number])

 # Hole class


class Hole(phylib.phylib_object):

    def __init__(self, pos):

        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HOLE,
                                      0,
                                      pos, None, None,
                                      0.0, 0.0)
        self.__class__ = Hole

    def svg(self):
        return """ <circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x,
                                                                          self.obj.hole.pos.y,
                                                                          HOLE_RADIUS)

# Python class for the Horizontal Cushion


class HCushion(phylib.phylib_object):

    def __init__(self, y):

        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_HCUSHION,
                                      0,
                                      None, None, None,
                                      0.0, y)
        self.__class__ = HCushion

    def svg(self):

        # Set y to -25, automatically assuming cushion is at the top
        y = -25
        # If it turns out the cushion is on the bottom, set y to 2700
        if self.obj.hcushion.y > TABLE_LENGTH/2:
            y = 2700

        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (y)

 # Python class for the Verticle Cushion


class VCushion(phylib.phylib_object):

    def __init__(self, x):

        phylib.phylib_object.__init__(self,
                                      phylib.PHYLIB_VCUSHION,
                                      0,
                                      None, None, None,
                                      x, 0.0)
        self.__class__ = VCushion

    def svg(self):

        # Set x to -25, automatically assuming cushion is at the left
        # If it turns out the cushion is on the right, set x to 1350
        # Set y to -25, automatically assuming cushion is at the top
        x = -25
        if self.obj.vcushion.x > TABLE_WIDTH/2:
            x = 1350

        return """ <rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (x)

################################################################################


class Table(phylib.phylib_table):
    """
    Pool table class.
    """

    def __init__(self):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__(self)
        self.current = -1

    def __iadd__(self, other):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object(other)
        return self

    def __iter__(self):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self

    def __next__(self):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[self.current]  # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1    # reset the index counter
        raise StopIteration  # raise StopIteration to tell for loop to stop

    def __getitem__(self, index):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object(index)
        if result == None:
            return None
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion
        return result

    def __str__(self):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = ""    # create empty string
        result += "time = %6.1f;\n" % self.time    # append time
        for i, obj in enumerate(self):  # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i, obj)  # append object description
        return result  # return the string

    def segment(self):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment(self)
        if result:
            result.__class__ = Table
            result.current = -1
        return result

    # add svg method here

    def svg(self):
        result = HEADER
        for i in self:
            if i:
                result += i.svg()
        result += FOOTER
        return result

    def roll(self, t):
        new = Table()
        for ball in self:
            if isinstance(ball, RollingBall):
                new_ball = RollingBall(ball.obj.rolling_ball.number,
                                    Coordinate(0, 0),
                                    Coordinate(0, 0),
                                    Coordinate(0, 0))
                # Compute where it rolls to
                phylib.phylib_roll(new_ball, ball, t)
            elif isinstance(ball, StillBall):
                new_ball = StillBall(ball.obj.still_ball.number,
                                    Coordinate(ball.obj.still_ball.pos.x,
                                                ball.obj.still_ball.pos.y))
            else:
                # Handle other types of balls or log an error
                continue  # Skip to the next iteration if ball type is unrecognized
            # Add ball to table
            new += new_ball
        return new
    
    def cueBall(self, table):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 0 or obj.obj.rolling_ball.number == 0:
                    self.current = -1
                    return obj
        return None
    
    # Checking if the eightBall is on the table.
    def eightBall(self, table):
        for obj in self:
            if isinstance(obj, StillBall) or isinstance(obj, RollingBall):
                if obj.obj.still_ball.number == 8 or obj.obj.rolling_ball.number == 8:
                    self.current = -1
                    return obj
        return None
       

 ##################################################################################################################################################################################################################


class Database():

    # Since the connection has to be a class attribute rather than an instance, declare dbConnection at the begging of the class.
    dbConnection = None

    def __init__(self, reset=False):

        # if reset is true, we want to remove the data base file
        if reset and os.path.exists("phylib.db"):
            os.remove("phylib.db")
        Database.dbConnection = sqlite3.connect("phylib.db")

    def createDB(self):

        methodCursor = Database.dbConnection.cursor()
        methodCursor.execute(ball)
        methodCursor.execute(tTable)
        methodCursor.execute(ballTable)
        methodCursor.execute(Shot)
        methodCursor.execute(tableShot)
        methodCursor.execute(game)
        methodCursor.execute(player)

        methodCursor.close()
        Database.dbConnection.commit()

        
    def readTable(self, tableID):

        methodCursor = Database.dbConnection.cursor()

        try:
            # Adjust TABLEID for SQL which starts at 1
            sqlTableID = tableID + 1
            

            methodCursor.execute("""
                SELECT b.BALLNO, b.XPOS, b.YPOS, b.XVEL, b.YVEL, t.TIME
                FROM Ball b
                JOIN BallTable bt 
                ON b.BALLID = bt.BALLID
                JOIN TTable t 
                ON bt.TABLEID = t.TABLEID
                WHERE bt.TABLEID = ?
            """, (sqlTableID,))
            results = methodCursor.fetchall()
            
            if not results:
                print("No Data to Query in Table", sqlTableID)
                return None
            
            # Create the table object
            table = Table()
            table_time = None #This is so we can update
            row = None
            # Process the query results
            for row in results:

                ball_no, xpos, ypos, xvel, yvel, table_time = row
                pos = Coordinate(xpos, ypos)
                # If it is a still ball
                if ((xvel == 0.0 and yvel == 0.0) or (xvel == None and yvel == None)):
                    ball = StillBall(ball_no, pos)
                # If it is a rolling ball
                else:
                    vel = Coordinate(xvel, yvel)
                    acc = Coordinate(0.0, 0.0)
                    ball = RollingBall(ball_no, pos, vel, acc)

                    # Acceleration logic from A2
                    # Acceleration logic from A2
                    speedRB = phylib.phylib_length(ball.obj.rolling_ball.vel)
                    if speedRB > VEL_EPSILON:
                        ball.obj.rolling_ball.acc.y = ((yvel / speedRB) * -1) * DRAG 
                        ball.obj.rolling_ball.acc.x = ((xvel / speedRB) * -1) * DRAG  

                table += ball
            
            table.time = float(table_time)

            return table

        except sqlite3.Error as e:
            print(f"Error reading table: {e}")
            return None

        finally:
            methodCursor.close()
            Database.dbConnection.commit()

    
    def writeTable(self, table):
                
        try:
            methodCursor = Database.dbConnection.cursor()
            
            # Insert time of the table into the TTable
            methodCursor.execute("""
                                 INSERT INTO TTable (TIME) VALUES (?)
                                 """, (table.time,))
            
            #Get the 
            sqlTableID = methodCursor.lastrowid
            tableID = sqlTableID - 1
            
            for ball in table:
                if isinstance(ball, StillBall):
                    methodCursor.execute("""
                                        INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) 
                                        VALUES (?, ?, ?, 0.0, 0.0)
                                        """, (ball.obj.still_ball.number, ball.obj.still_ball.pos.x, ball.obj.still_ball.pos.y))
                    ballID = methodCursor.lastrowid
                    methodCursor.execute("""
                                        INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?) 
                                        """, (ballID, sqlTableID))      
                  
                elif isinstance(ball, RollingBall):
                    methodCursor.execute("""
                                        INSERT INTO Ball (BALLNO, XPOS, YPOS, XVEL, YVEL) 
                                        VALUES (?, ?, ?, ?, ?)
                                        """, (ball.obj.rolling_ball.number, ball.obj.rolling_ball.pos.x, ball.obj.rolling_ball.pos.y,
                                                ball.obj.rolling_ball.vel.x, ball.obj.rolling_ball.vel.y))
                    
                    ballID = methodCursor.lastrowid
                    methodCursor.execute("""
                                        INSERT INTO BallTable (BALLID, TABLEID) VALUES (?, ?) 
                                        """, (ballID, sqlTableID))

            return tableID
                
        except sqlite3.Error as e:
            print(f"Error reading table: {e}")
            return None
        
        finally:
            methodCursor.close()
            Database.dbConnection.commit() 

    def close(self):
        Database.dbConnection.commit();
        Database.dbConnection.close();       

    def getGame(self, gameIDPlusOne):
        methodCursor = Database.dbConnection.cursor()
        print("ENTERING getGAME")
        try:
            methodCursor.execute("""
                                SELECT Game.gameName, player1.PLAYERID as Player1ID, player1.PLAYERNAME as Player1Name, player2.PLAYERID as Player2ID, player2.PLAYERNAME as Player2Name
                                From Game 
                                JOIN Player player1 ON Game.GAMEID = player1.GAMEID
                                JOIN Player player2 ON Game.GAMEID = player2.GAMEID AND 
                                WHERE Game.GAMEID = ? AND player1.PLAYERID < player2.PLAYERID
                                """, (gameIDPlusOne,))
            
            return methodCursor.fetchall()
        
        except sqlite3.Error as e:
            print(f"Error Querying table: {e}")
            return None
        
        finally:
            methodCursor.close()
            Database.dbConnection.commit() #3TRY ADDING COMMIT AFTER RETURN
        
    def setGame(self, gameName, player1Name, player2Name):
        # print("ENTERING SETGAME FUNCTION")
        #Create a cursor in the method
        methodCursor = Database.dbConnection.cursor()
        
        try:
            # We're going to add the gameName into the Game Table
            methodCursor.execute("""
                                INSERT INTO Game (GAMENAME) VALUES (?)
                                """, (gameName,))
            
            # GameID is automatically created when we insert the new gameName above
            # we need the gameID to associate the gameID with the players that we will add in PLAYER table
            gameID = methodCursor.lastrowid
            # print("Currently in setGame after gettinig gameId", gameID)          
            #Insert the first player into PLAYER table
            methodCursor.execute("""
                                INSERT INTO PLAYER (GAMEID, PLAYERNAME) VALUES (?, ?)
                                """, (gameID, player1Name))               
            # print("WE ARE AFTER INSERTING PLAYER1")
            #Insert the second player into PLAYER table    
            methodCursor.execute("""
                                INSERT INTO PLAYER (GAMEID, PLAYERNAME) VALUES (?, ?)
                                """, (gameID, player2Name))               
            # print("WE ARE AFTER INSERTING PLAYER2")
            return gameID
        
        except sqlite3.Error as e:
            # print(f"Error INSERTING into table: {e}")
            return None
        
        finally:
            methodCursor.close()
            Database.dbConnection.commit() #3TRY ADDING COMMIT AFTER RETURN

    def getPlayerID(self, gameName, playerName):
        # print("ENTERING GETPLAYERID FUNCTION")
        #Create a cursor in the method
        methodCursor = Database.dbConnection.cursor()
        try:
            methodCursor.execute("""
                                SELECT Player.PLAYERID
                                FROM Player 
                                INNER JOIN Game ON Player.GAMEID = Game.GAMEID
                                WHERE Player.PLAYERNAME = ? AND Game.GAMENAME = ?
                                """, (playerName, gameName,))

            playerID = methodCursor.fetchone()[0]
            # print("GETPLAYERID FUNCTION: ", playerID)
            return playerID

        except sqlite3.Error as e:
            # print(f"Error fetching PlayerID: {e}")
            return None
        
        finally:
            methodCursor.close()
            Database.dbConnection.commit() 
            
    #Method adds a new entry to shot table for current game and current playerID and returns shotid        
    def newShot(self, gameID, playerID):     
                
        #Create a cursor in the method
        methodCursor = Database.dbConnection.cursor()
        
        print(playerID)
        
        try:
            methodCursor.execute("""
                                INSERT INTO SHOT (PlayerID, GameID) VALUES(?, ?)
                                """, (playerID, gameID,))

            # return the newly created shotid
            return methodCursor.lastrowid

        except sqlite3.Error as e:
            print(f"Error INSERTING shot: {e}")
            return None
        
        finally:
            methodCursor.close()
            Database.dbConnection.commit() 

    def writeTableShot(self, tableIDPlusOne, shotID):
        
        # print("in writetableshot ")
                #Create a cursor in the method
        methodCursor = Database.dbConnection.cursor()    
        methodCursor.execute("""
                            INSERT INTO TableShot (SHOTID, TABLEID) VALUES (?, ?)
                            """, (shotID, tableIDPlusOne,))

        # return the newly created shotid
        methodCursor.close()
        Database.dbConnection.commit() 

        
        return methodCursor.lastrowid

class Game():
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):
        # print("Entering Game Class")
        
        self.db = Database() #Create an instance of Database
        self.db.createDB()
        
        self.table = Table()
        self.gameID = gameID
        self.gameIDPlusOne = None
        self.gameName = gameName
        self.player1Name = player1Name
        self.player2Name = player2Name
        self.gameIDPlusOne = None
        
        #First constructor. We are given a gameID ONLY
        if gameID is not None and gameName is None and player1Name is None and player2Name is None: #and all(param is None for param in [gameName, player1Name, player2Name, table]):
            # print("IN FIRST CONSTRUCTOR")
            #add one because sql starts at one
            self.gameIDPlusOne = self.gameID + 1
            
            #retrieve the existing game
            gameData = self.db.getGame(self.gameIDPlusOne)
            
            #ensure that the function didn't return any empty variables
            if gameData: 
                self.gameName, self.player1ID, self.player1Name, self.player2ID, self.player2Name = gameData
            
            else:
                raise ValueError("gameID not found")
        
        #Second Constructor. We are basically creating a new game given a gameName and two players    
        elif gameID is None and gameName is not None and player1Name is not None and player2Name is not None:
            # print("IN SECOND CONSTRUCTOR")
            self.gameID = self.db.setGame(gameName, player1Name, player2Name)
            self.gameIDPlusOne = self.gameID + 1
            #Checking if a gameID is returned
            if not self.gameID: 
                raise ValueError("gameID not found") 
            
        else:
            raise TypeError("Error in Game Class Constructor Parameters")
            
    def shoot(self, gameName, playerName, table, xvel, yvel):
        # print("ENTERING SHOOT FUNCTION", playerName)
        #Getting the PlayerID
        
        playerID = self.db.getPlayerID(gameName, playerName)

        if not playerID:
            raise ValueError("Player ID not found")

        shotID = self.db.newShot(self.gameID, playerID)
        
        if not shotID:
            print("Error creating a new shot")
            return None
        
        cueBall = table.cueBall(table)

        if not cueBall:
            print("Error, Cue Ball not Found")
            return None
        
        #S tore the Original Positions of the cue ball
        xPos, yPos = cueBall.obj.still_ball.pos.x, cueBall.obj.still_ball.pos.y
                
        cueBall.type = phylib.PHYLIB_ROLLING_BALL
        cueBall.obj.rolling_ball.pos.x = xPos
        cueBall.obj.rolling_ball.pos.y = yPos
        cueBall.obj.rolling_ball.vel.x = xvel
        cueBall.obj.rolling_ball.vel.y = yvel
        cueBall.obj.rolling_ball.number = 0  
        
        # speedRB = phylib.phylib_length(cueBall.obj.rolling_ball.vel)
        speedRB = math.sqrt((xvel * xvel) + (yvel * yvel))
        if speedRB > VEL_EPSILON:
            cueBall.obj.rolling_ball.acc.y = ((yvel / speedRB) * -1) * DRAG #FOR REGRADE: fixedc acceleration logic in shoot OVER A DAMN > SIGN I HAD <
            cueBall.obj.rolling_ball.acc.x = ((xvel / speedRB) * -1) * DRAG #FOR REGRADE: Fixed acceleration logic in shoot
        else:
            cueBall.obj.rolling_ball.acc.y = 0.0
            cueBall.obj.rolling_ball.acc.x = 0.0            
            
        cumulativeTime = table.time

        while True:
            segment = table.segment()
            if segment is None:
                break

            startTime = cumulativeTime
            endTime = segment.time
            totalTime = endTime - startTime
            totalFrames = int(totalTime // FRAME_RATE)
            # print(totalFrames, totalTime, cumulativeTime)
            # Adjust cumulative time tracker
            cumulativeTime += totalTime

            for frame in range(totalFrames):
                frameTime = FRAME_RATE * frame
                tableRoll = table.roll(frameTime)
                tableRoll.time = startTime + frameTime

                tableID = self.db.writeTable(tableRoll)
                tableIDPlusOne = tableID + 1
                self.db.writeTableShot(tableIDPlusOne, shotID)

            table = segment  
# function to check if a table already exists

# def tableExist(tableName, Connection):

#     cur = Connection.cursor()
#     # The following command is from: https://stackoverflow.com/questions/1601151/how-do-i-check-in-sqlite-whether-a-table-exists
#     cur.execute(
#         """SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{tableName}'""")
#     count = cur.fetchone()[0]
#     # IF count is 1, meaning the table exists, then it will return true, else the table doesn't exist, it will return false.
#     return count == 1

