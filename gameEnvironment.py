import gym
from gym import spaces
import loggers
import numpy as np

class VexEnv(gym.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self):
    super(VexEnv, self).__init__()

    # Set up the gameState as a default
    self.gameState = GameState(np.array([0,1,0,5, 0,0,0, 0,0,0, 0,0,0], dtype=np.int),0)
    self.actionSpace = np.array([0,0,0,0,0,0], dtype=np.int)
    self.pieces = {'1':'X', '0':'-', '-1':'O'}
    self.grid_shape = (33,1)
    self.input_shape = (1,1,13)
    self.name = 'vex-changeup'
    self.state_size = len(self.gameState.binary)
    self.action_size = len(self.actionSpace)

    self.action_names = {
        0: 'MOVE RIGHT',
        1: 'MOVE DOWN',
        2: 'MOVE LEFT',
        3: 'MOVE UP',
        4: 'PLACE BALL',
        5: 'DESCORE BALL'
    }

    # Each cell on the board is provided: 0=empty (1-3)=number of balls 4=player
    # self.observation_space = spaces.Discreet(13)
    # Set max rewards / rewards range to be total max currentPlayerPoints
    # self.reward_range = (0,75)

  def step(self, actions):
    # Execute one time step within the environment
    next_state, value, done = self.gameState.takeAction(actions[0],0)
    self.gameState = next_state
    next_state, value, done = self.gameState.takeAction(actions[1],1)
    self.gameState = next_state
    self.gameState.turn += 1
    info = None
    return ((next_state, value, done, info))

  def reset(self):
      self.gameState = GameState(np.array([0,1,0,5, 0,0,0, 0,0,0, 0,0,0], dtype=np.int),0)
      return self.gameState

  def render(self, logger, mode='human', close=False):
    # Render the environment to the screen
    self.gameState.render(logger)

  def identities(self, state, actionValues):
    identities = []
    currentBoard = state.board
    currentAV = actionValues
    for n in range(5):
        currentBoard = np.array([
                    currentBoard[20], currentBoard[15],currentBoard[10], currentBoard[5],currentBoard[0]
                    , currentBoard[21], currentBoard[16],currentBoard[11], currentBoard[6],currentBoard[1]
                    , currentBoard[22], currentBoard[17],currentBoard[12], currentBoard[7],currentBoard[2]
                    , currentBoard[23], currentBoard[18],currentBoard[13], currentBoard[8],currentBoard[3]
                    , currentBoard[24], currentBoard[19],currentBoard[14], currentBoard[9],currentBoard[4]
                    ])
        currentAV = np.array([
                    currentAV[20], currentAV[15],currentAV[10], currentAV[5],currentAV[0]
                    , currentAV[21], currentAV[16],currentAV[11], currentAV[6],currentAV[1]
                    , currentAV[22], currentAV[17],currentAV[12], currentAV[7],currentAV[2]
                    , currentAV[23], currentAV[18],currentAV[13], currentAV[8],currentAV[3]
                    , currentAV[24], currentAV[19],currentAV[14], currentAV[9],currentAV[4]
                    ])
        identities.append((GameState(currentBoard, state.turn), currentAV))

    currentBoard = np.array([
                currentBoard[4], currentBoard[3],currentBoard[2], currentBoard[1],currentBoard[0]
                , currentBoard[9], currentBoard[8],currentBoard[7], currentBoard[6],currentBoard[5]
                , currentBoard[14], currentBoard[13],currentBoard[12], currentBoard[11],currentBoard[10]
                , currentBoard[19], currentBoard[18],currentBoard[17], currentBoard[16],currentBoard[15]
                , currentBoard[24], currentBoard[23],currentBoard[22], currentBoard[21],currentBoard[20]
                ])

    currentAV = np.array([
                currentAV[4], currentAV[3],currentAV[2], currentAV[1],currentAV[0]
                , currentAV[9], currentAV[8],currentAV[7], currentAV[6],currentAV[5]
                , currentAV[14], currentAV[13],currentAV[12], currentAV[11],currentAV[10]
                , currentAV[19], currentAV[18],currentAV[17], currentAV[16],currentAV[15]
                , currentAV[24], currentAV[23],currentAV[22], currentAV[21],currentAV[20]
                ])
    for n in range(5):
        currentBoard = np.array([
					  currentBoard[20], currentBoard[15],currentBoard[10], currentBoard[5],currentBoard[0]
					, currentBoard[21], currentBoard[16],currentBoard[11], currentBoard[6],currentBoard[1]
					, currentBoard[22], currentBoard[17],currentBoard[12], currentBoard[7],currentBoard[2]
					, currentBoard[23], currentBoard[18],currentBoard[13], currentBoard[8],currentBoard[3]
					, currentBoard[24], currentBoard[19],currentBoard[14], currentBoard[9],currentBoard[4]
					])

        currentAV = np.array([
					  currentAV[20], currentAV[15],currentAV[10], currentAV[5],currentAV[0]
					, currentAV[21], currentAV[16],currentAV[11], currentAV[6],currentAV[1]
					, currentAV[22], currentAV[17],currentAV[12], currentAV[7],currentAV[2]
					, currentAV[23], currentAV[18],currentAV[13], currentAV[8],currentAV[3]
					, currentAV[24], currentAV[19],currentAV[14], currentAV[9],currentAV[4]

					])

        identities.append((GameState(currentBoard, state.turn), currentAV))

    return identities

class GameState():
    def __init__(self,board,turn):
        self.board = board
        self.pieces = {'1':'X','0':'-','-1':'O'}
        self.winners = [
            {'points': 6, 'tiles' : [
                [4,5,6],
                [7,8,9],
                [10,11,12],
                [4,7,10],
                [5,8,11],
                [6,9,12],
                [4,8,12],
                [6,8,10]
            ]}
        ]

        # Binary storage of tower data being converted into useful control / counts
        self.currentplayer_controls = [42,38,26,22,40,24,32]
        self.currentplayer_count = {
            42:3,
            38:2,
            22:1,
            26:2,
            40:2,
            24:1,
            32:1,
            21:0,
            25:1,
            41:2,
            37:1,
            20:0,
            36:1,
            16:0,
            0:0
        }
        self.otherplayer_controls = [21,25,41,37,20,36,16]
        self.otherplayer_count = {
            42:0,
            38:1,
            22:2,
            26:1,
            40:0,
            24:1,
            32:0,
            21:3,
            25:2,
            41:1,
            37:2,
            20:2,
            36:1,
            16:1,
            0:0
        }
        self.turn = turn;
        self.binary = self._binary()
        self.id = self._convertStateToId()
        self.allowedActions = self._allowedActions()
        self.is_end_game = self._checkForEndGame()
        self.value = self._getValue()
        self.score = self._getScore()

    def _allowedActions(self):
        return [0,1,2,3,4,5]
    def _binary(self):
        # binary x and y are just (0-6) numbers so a 3 digit binary works
        binary_length = (4)*3+(len(self.board)-4)*6
        binary = np.zeros(binary_length, dtype=np.int)

        for i,coordinate in enumerate(self.board[:4]):
            x = str(bin(coordinate))
            # Ignoring the '0b' at the start of every binary number
            y = x[2:]

            # Clean up binary string: Add zeros in front if we have to
            while len(y)<3:
            	y = '0' + y

            # Copy bits from y to binary array
            for b in range(3):
                binary[3*i+b] = int(y[b])
        # For all the towers, turn the stats into binary
        # NOTE: self.board[4:] just ignores the first 4 board numbers which are the two players x and y
        for i,tower in enumerate(self.board[4:]):
            x = str(bin(tower))
            # Ignoring the '0b' at the start of every binary number
            y = x[2:]

            # Clean up binary string: Add zero in front if we have to
            while len(y)<6:
            	y = '0' + y
            # Copy bits from y to binary array
            for b in range(6):
                binary[6*i+b] = int(y[b])

        return (binary)

    def _convertStateToId(self):
        b = self._binary()
        id = ''.join(map(str,b))
        return id

    def _checkForEndGame(self):
        if (self.turn >=50):
            return 1
        return 0


    def _getValue(self):

        # Finds how many points each vex team has

        # Check each type of line, in this case there's only 1, 3 in a row
        # Adds 6 points for each row / column / diagonal
        currentPlayerPoints = 0
        for lineType in self.winners:
            points = lineType['points']
            # For each combination of tiles that could be 3 in a row, check each tile
            # If any tile breaks the 3 in a row, check the flag and don't add points
            # A tower breaks the 3 in a row if it's not controled, not in controls list
            # If the flag never gets checked and stays 0, add the extra 6 points
            for tiles in lineType['tiles']:

                checkFlag = 0
                tilenum = 0
                while tilenum < 3 and checkFlag ==0:
                    if not self.board[tiles[tilenum]] in self.currentplayer_controls:
                        checkFlag = 1
                    tilenum += 1
                if checkFlag == 0:
                    currentPlayerPoints += points

        # Adds a point for each ball in a tower
        for tower in self.board[4:]:
            # print("TOWER:  ",tower)
            currentPlayerPoints += self.currentplayer_count[tower]

        otherPlayerPoints = 0
        for lineType in self.winners:
            points = lineType['points']
            # For each combination of tiles that could be 3 in a row, check each tile
            # If any tile breaks the 3 in a row, check the flag and don't add points
            # A tower breaks the 3 in a row if it's not controled, not in controls list
            # If the flag never gets checked and stays 0, add the extra 6 points
            for tiles in lineType['tiles']:

                checkFlag = 0
                tilenum = 0
                while tilenum < 3 and checkFlag ==0:
                    if not self.board[tiles[tilenum]] in self.otherplayer_controls:
                        checkFlag = 1
                    tilenum += 1
                if checkFlag == 0:
                    otherPlayerPoints += points

        # Adds a point for each ball in a tower
        for tower in self.board[4:]:
            otherPlayerPoints += self.otherplayer_count[tower]

        # return scores as well as the current winner
        if currentPlayerPoints > otherPlayerPoints:
            return (1, currentPlayerPoints, otherPlayerPoints)
        elif currentPlayerPoints < otherPlayerPoints:
            return (-1, currentPlayerPoints, otherPlayerPoints)
        else:
            return (0, currentPlayerPoints, otherPlayerPoints)

    def _getScore(self):
        # Quick access to points, same as _getValue but without the winner
        tmp = self.value
        return (tmp[1],tmp[2])

    def _touchingWall(self,x,y,dx,dy):
        if(x+dx<0 or x+dx>6): return True
        if(y+dy<0 or y+dy>6): return True

        # Check if hitting a tower, all towers are on squares divisible by 3
        # ex: (0,3) (0,0) (3,6)
        if (x+dx)%3==0 and (y+dy)%3==0: return True

        return False


    def calculateAction(self,action):
        return
    def takeAction(self,action,player):

        newBoard = np.array(self.board)
        if player == 0:
            x = newBoard[0]
            y = newBoard[1]
            id = '10'
        else:
            x = newBoard[2]
            y = newBoard[3]
            id = '01'

        dx,dy = 0,0

        # NOTE: smaller dy means going up, larger means going down
        if action == 0: dx = 1
        if action == 1: dy = 1
        if action == 2: dx = -1
        if action == 3: dy = -1

        # Move the player by dx dy
        if not self._touchingWall(x,y,dx,dy):
            if player == 0:
                newBoard[0] += dx
                newBoard[1] += dy
            else:
                newBoard[2] += dx
                newBoard[3] += dy
            # print(x,dx,' ',y,dy, 'not into wall')
        else:
            # print('player:', player, x,dx,'into wall')
            pass
        #Check for nearby Tower
        tower = -1
        # Check right / left
        if (x+1)%3==0 and y%3==0: tower = (x+1)/3 + y
        if (x-1)%3==0 and y%3==0: tower = (x-1)/3 + y

        # Check above and below
        if x%3==0 and (y+1)%3==0: tower = x/3 + (y+1)
        if x%3==0 and (y-1)%3==0: tower = x/3 + (y-1)


        if action == 4:
            # If a tower was found nearby, place a ball into the tower
            if tower!=-1:
                # print('found tower ',tower)
                tower = int(tower)
                balls_bin = str(bin(newBoard[4+tower]))[2:]
                while len(balls_bin)<6:
                    balls_bin = '0'+ balls_bin
                # Split balls_bin into list containing each ball
                balls = [balls_bin[i:i+2] for i in range(0, len(balls_bin), 2)]

                # Find the top_most ball, and add a ball on top, if its full do nothing
                for i,b in enumerate(balls):
                    if b == '00':
                        balls[i] = id
                        break
                else:
                    # Tower is full
                    pass
                # Save changes

                # print(balls,int(''.join(balls),2))
                newBoard[4+tower] = int(''.join(balls),2)
            else:
                # print('tower not found',x,y)
                pass

        if action == 5:
            # If a tower was found nearby, take a ball out of the tower
            if tower!=-1:
                # print('found tower ',tower)
                tower = int(tower)
                balls_bin = str(bin(newBoard[4+tower]))[2:]
                while len(balls_bin)<6:
                    balls_bin = '0'+ balls_bin
                balls_bin = balls_bin[2:] + '00'

                # Split balls_bin into list containing each ball
                balls = [balls_bin[i:i+2] for i in range(0, len(balls_bin), 2)]
                # print(balls,int(''.join(balls),2))

                # Save changes
                newBoard[4+tower] = int(''.join(balls),2)
            else:
                # print('tower not found: ',x,y,dx,dy)
                pass

        newState = GameState(newBoard,self.turn)
        value = 0
        done = 0

        if newState.is_end_game:
            value = newState.value
            print("ENDING", value)
            done = 1

        # print(newState.board)
        return (newState, value, done)

    def render(self, logger):
        # print(logger)
        for row in range(7):
            row_str = []
            for col in range(7):
                # If the cell is a tower, write the dec number depicting the binary
                if row%3==0 and col%3==0:
                    row_str.append(str(self.board[int(4+row + col/3)]))
                # If cell is player1 fill with x
                elif col==self.board[0] and row==self.board[1]:
                    row_str.append(self.pieces['1'])
                # If cell is player2 fill with o
                elif col==self.board[2] and row==self.board[3]:
                    row_str.append(self.pieces['-1'])
                # If cell is empty fill with dash
                else:
                    row_str.append(self.pieces['0'])
            # After looping through all the columns, log the row_str
            logger.info(row_str)
        # Astheticc
        logger.info('-------------------------------------------')
