import random

#global variables
wallTypes = [-1,0]





#the Room class defines a singular room that can be placed in a Maze;
#it stores the information of where the player can travel from this room
class Room():

    def __init__(self,position,neighbours):

        self.position = position #position in maze, starting at 1
        self.neighbours = neighbours
        self.routes = list(neighbours) #make routes array mutable



    def editWall(self,direction,update):

        self.routes[direction] = update





#the Maze class defines a grid of Rooms that can be rendered and played
class Maze():

    def __init__(self,length,height):

        self.length = length
        self.height = height
        self.area = length * height
        self.structure = self.generateStructure()
        self.corners = self.getCorners()



    def generateStructure(self):

        structure = []


        for mazePosition in range(1,self.area + 1):

            neighbours = self.calculateNeighbours(mazePosition)
            structure.append(Room(mazePosition,neighbours))


        return structure



    def calculateNeighbours(self,position):

        neighbours = [-1]*4

        #if room is not on the... 
        
        #...west side of the maze
        if position % self.length != 1: 
            neighbours[3] = position - 1

        #...east side of the maze
        if position % self.length != 0: 
            neighbours[1] = position + 1

        #... north side of the maze
        if position > self.length: 
            neighbours[0] = position - self.length

         #... south side of the maze
        if position < self.area - self.length + 1:
            neighbours[2] = position + self.length


        return tuple(neighbours) #make neighbour array immutable
    


    def addWall(self,roomPosition,direction):

        targetRoom = self.structure[roomPosition - 1]


        #if no wall exists at this direction
        if targetRoom.routes[direction] not in wallTypes:

            targetRoom.editWall(direction,0) #create initial wall

            #create identical wall in same place on opposite room
            converseRoom = self.structure[targetRoom.neighbours[direction] - 1]
            converseRoom.editWall(directionCorrector(direction + 2),0)
            


    def removeWall(self,roomPosition,direction):

        targetRoom = self.structure[roomPosition - 1]


        #if an inner wall exists at this direction
        if targetRoom.routes[direction] == 0: 

            targetRoom.editWall(direction,targetRoom.neighbours[direction]) #revert initial route

            #revert identical route in same place on opposite room
            converseRoom = self.structure[targetRoom.neighbours[direction] - 1]
            converseRoom.editWall(directionCorrector(direction + 2),targetRoom.position)



    #creates a list of all the spaces in the maze where there are no walls present
    def noWallRoutes(self): 

        noWallCoordinates = []

        for room in self.structure:

            for direction, route in enumerate(room.routes):

                if route not in wallTypes:

                    noWallCoordinates.append([room.position,direction])


        return noWallCoordinates



    def getCorners(self):

        corners = []
        corners.append(self.length)
        corners.append((self.area - self.length) + 1)
        corners.append(self.area)

        return tuple(corners)





#this function calculates the maximum amount of walls you can fit in a maze will still allowing maneuverability
def optimumWallCountFinder(length,height):

    return (length - 1) * (height - 1)





#this function corrects direction if it is outwith the range of 0 to 3 inclusive
def directionCorrector(direction): 

    if direction > 3:
        return direction - 4
    
    elif direction < 0:
        return direction + 4
    

    return direction





#this function returns false if a room has 3 walls
def wallCountChecker(room): 

    wallCount = 0
    
    for route in room.routes:
        
        if route in wallTypes:
            wallCount += 1


    return wallCount != 3





#this function makes coordinates for a wall
def wallCoordinatesMaker(room,direction): 

    currentWall = [room.position,direction]
    converseWall = [room.neighbours[direction],directionCorrector(direction + 2)]

    return [currentWall, converseWall]





#this function checks the coordinates of one wall pair is not in a set of walls coordinate pairs
def wallCoordinatesVerify(room,direction,otherWalls): 

    wallPair = wallCoordinatesMaker(room,direction)

    #return false if there is any intersection between the lists
    return not any(item in otherWalls for item in wallPair)





#this function orchestrates the wallChainFinder function and tell it what wall to check next
def wallChainFinderBranch(maze,currentRoom,direction,pastWalls,presentWalls,futureWalls,outerWallCount): 

    if outerWallCount > 1:
        return outerWallCount


    futureWalls.extend(wallCoordinatesMaker(currentRoom,direction))


    routes = currentRoom.routes
    neighbours = currentRoom.neighbours
    #get the room accross from where the current wall being checked is
    converseRoom = maze.structure[neighbours[direction] - 1] 

    sideDirection1 = directionCorrector(direction - 1)
    sideDirection2 = directionCorrector(direction + 1)


    #if there is an outer wall to the first side of this room
    if neighbours[sideDirection1] == -1: 

        outerWallCount += 1
        #get the room to the opposite side of the outer wall
        sideRoom2 = maze.structure[neighbours[sideDirection2] - 1] 

        futureWalls.extend(wallCoordinatesMaker(converseRoom,sideDirection2))
        futureWalls.extend(wallCoordinatesMaker(sideRoom2,direction))
        futureWalls.extend(wallCoordinatesMaker(currentRoom,sideDirection2))


        #if there is a wall to the second side of the converse room and room not already considered
        if converseRoom.routes[sideDirection2] == 0 and wallCoordinatesVerify(converseRoom,sideDirection2,presentWalls): 
            outerWallCount = wallChainFinder(maze,converseRoom,sideDirection2,pastWalls,futureWalls,[],outerWallCount)

        #if there is a wall inline with the current wall on the room to the second side and room not already considered
        if sideRoom2.routes[direction] == 0 and wallCoordinatesVerify(sideRoom2,direction,presentWalls): 
            outerWallCount = wallChainFinder(maze,sideRoom2,direction,pastWalls,futureWalls,[],outerWallCount)

        if routes[sideDirection2] == 0 and wallCoordinatesVerify(currentRoom,sideDirection2,presentWalls):
            outerWallCount = wallChainFinder(maze,currentRoom,sideDirection2,pastWalls,futureWalls,[],outerWallCount)


    #if there is an outer wall to the second side of this room
    elif neighbours[sideDirection2] == -1: 

        outerWallCount += 1
        #get the room to the opposite side of the outer wall
        sideRoom1 = maze.structure[neighbours[sideDirection1] - 1] 

        futureWalls.extend(wallCoordinatesMaker(converseRoom,sideDirection1))
        futureWalls.extend(wallCoordinatesMaker(sideRoom1,direction))
        futureWalls.extend(wallCoordinatesMaker(currentRoom,sideDirection1))


        #if there is a wall to the first side of the converse room and room not already considered
        if converseRoom.routes[sideDirection1] == 0 and wallCoordinatesVerify(converseRoom,sideDirection1,presentWalls):             
            outerWallCount = wallChainFinder(maze,converseRoom,sideDirection1,pastWalls,futureWalls,[],outerWallCount)

        #if there is a wall inline with the current wall on the room to the first side and room not already considered
        if sideRoom1.routes[direction] == 0 and wallCoordinatesVerify(sideRoom1,direction,presentWalls):            
            outerWallCount = wallChainFinder(maze,sideRoom1,direction,pastWalls,futureWalls,[],outerWallCount)

        if routes[sideDirection1] == 0 and wallCoordinatesVerify(currentRoom,sideDirection1,presentWalls):         
            outerWallCount = wallChainFinder(maze,currentRoom,sideDirection1,pastWalls,futureWalls,[],outerWallCount)


    else:
        #get the rooms on either side of this room
        sideRoom2 = maze.structure[neighbours[sideDirection2] - 1] 
        sideRoom1 = maze.structure[neighbours[sideDirection1] - 1]

        #keeps note of all neighbouring walls of the current wall
        futureWalls.extend(wallCoordinatesMaker(converseRoom,sideDirection2))
        futureWalls.extend(wallCoordinatesMaker(sideRoom2,direction))
        futureWalls.extend(wallCoordinatesMaker(currentRoom,sideDirection2))
        futureWalls.extend(wallCoordinatesMaker(converseRoom,sideDirection1))
        futureWalls.extend(wallCoordinatesMaker(sideRoom1,direction))
        futureWalls.extend(wallCoordinatesMaker(currentRoom,sideDirection1))

        
        #if there is a wall to the second side of the converse room and room not already considered
        if converseRoom.routes[sideDirection2] == 0 and wallCoordinatesVerify(converseRoom,sideDirection2,presentWalls):       
            outerWallCount = wallChainFinder(maze,converseRoom,sideDirection2,pastWalls,futureWalls,[],outerWallCount)

        #if there is a wall inline with the current wall on the room to the second side and room not already considered        
        if sideRoom2.routes[direction] == 0 and wallCoordinatesVerify(sideRoom2,direction,presentWalls):    
            outerWallCount = wallChainFinder(maze,sideRoom2,direction,pastWalls,futureWalls,[],outerWallCount)

        if routes[sideDirection2] == 0 and wallCoordinatesVerify(currentRoom,sideDirection2,presentWalls):       
            outerWallCount = wallChainFinder(maze,currentRoom,sideDirection2,pastWalls,futureWalls,[],outerWallCount)

        #if there is a wall to the first side of the converse room and room not already considered
        if converseRoom.routes[sideDirection1] == 0 and wallCoordinatesVerify(converseRoom,sideDirection1,presentWalls):            
            outerWallCount = wallChainFinder(maze,converseRoom,sideDirection1,pastWalls,futureWalls,[],outerWallCount)

        #if there is a wall inline with the current wall on the room to the first side and room not already considered
        if sideRoom1.routes[direction] == 0 and wallCoordinatesVerify(sideRoom1,direction,presentWalls):            
            outerWallCount = wallChainFinder(maze,sideRoom1,direction,pastWalls,futureWalls,[],outerWallCount)

        if routes[sideDirection1] == 0 and wallCoordinatesVerify(currentRoom,sideDirection1,presentWalls):           
            outerWallCount = wallChainFinder(maze,currentRoom,sideDirection1,pastWalls,futureWalls,[],outerWallCount)


    return outerWallCount





#this function checks if a wall would obscure part of the maze by connecting two parts of the outer wall
def wallChainFinder(maze,currentRoom,direction,pastWalls,presentWalls,futureWalls,outerWallCount):

    if outerWallCount > 1:
        return outerWallCount


    currentWallPair = wallCoordinatesMaker(currentRoom,direction)


    #if current wall has already been checked previously, exit this algorithm
    if currentWallPair[0] in pastWalls:
        return 2
    #else add them to the list of checked walls
    pastWalls.extend(currentWallPair)


    outerWallCount = wallChainFinderBranch(maze,currentRoom,direction,pastWalls,presentWalls,futureWalls,outerWallCount)

    
    return outerWallCount





#this function checks if a wall is sandwhiched on both sides by other walls
def wallSandwhichFinder(maze,roomPosition,direction):

    targetRoom = maze.structure[roomPosition - 1]

    routes = targetRoom.routes
    neighbours = targetRoom.neighbours
    #get the room accross from where the current wall being checked is
    converseRoom = maze.structure[neighbours[direction] - 1] 

    sandwhichWallCount = 0

    sideDirection1 = directionCorrector(direction - 1)
    sideDirection2 = directionCorrector(direction + 1)


    #if there is an outer wall to the first side of this room
    if neighbours[sideDirection1] == -1: 

        sandwhichWallCount += 1
        #get the room to the opposite side of the outer wall
        sideRoom2 = maze.structure[neighbours[sideDirection2] - 1] 

        #if there is a wall beside the other end of the wall
        if converseRoom.routes[sideDirection2] == 0 or sideRoom2.routes[direction] == 0 or routes[sideDirection2] == 0: 
            sandwhichWallCount += 1


    #if there is an outer wall to the second side of this room
    elif neighbours[sideDirection2] == -1: 

        sandwhichWallCount += 1
        #get the room to the opposite side of the outer wall
        sideRoom1 = maze.structure[neighbours[sideDirection1] - 1] 

        #if there is a wall beside the other end of the wall
        if converseRoom.routes[sideDirection1] == 0 or sideRoom1.routes[direction] == 0 or routes[sideDirection1] == 0: 
            sandwhichWallCount += 1


    else:
        #get the rooms on either side of this room
        sideRoom2 = maze.structure[neighbours[sideDirection2] - 1] 
        sideRoom1 = maze.structure[neighbours[sideDirection1] - 1]

        #if there is a wall beside one end of the wall
        if converseRoom.routes[sideDirection2] == 0 or sideRoom2.routes[direction] == 0 or routes[sideDirection2] == 0: 
            sandwhichWallCount += 1

        #if there is a wall beside the other end of the wall
        if converseRoom.routes[sideDirection1] == 0 or sideRoom1.routes[direction] == 0 or routes[sideDirection1] == 0: 
            sandwhichWallCount += 1


    if sandwhichWallCount == 2:
        return True


    return False





#this function prodecurally generates a maze
def mazeRandomizer(): 

    randomMaze = Maze(8,8)

    #creates a selection pool of all the spaces in the maze where no walls are present
    possibleWallCoordinates = randomMaze.noWallRoutes() 
    addedWallCoordinates = []
    #finds the max walls you could place in the maze while still allowing room movement
    optimumWallCount = optimumWallCountFinder(8,8) 



    for index in range(optimumWallCount):

        #gets a wall from the selection pool
        randomWallCoordinate = random.choice(possibleWallCoordinates) 
        randomRoomPosition = randomWallCoordinate[0]
        randomDirection = randomWallCoordinate[1]
        targetRoom = randomMaze.structure[randomRoomPosition - 1]


        #if one of the conditions is not met
        while not mazeRandomizerConditions(randomMaze,targetRoom,randomDirection): 

            #removes the wall and converse wall from the selection pool
            possibleWallCoordinates.remove(randomWallCoordinate)
            possibleWallCoordinates.remove(wallCoordinatesMaker(targetRoom,randomDirection)[1])

            #gets a new wall from the selection pool
            randomWallCoordinate = random.choice(possibleWallCoordinates) 
            randomRoomPosition = randomWallCoordinate[0]
            randomDirection = randomWallCoordinate[1]
            targetRoom = randomMaze.structure[randomRoomPosition - 1]

        
        #adds wall to maze if conditions are met
        randomMaze.addWall(randomRoomPosition,randomDirection) 

        #creates a log of all the successfully added walls
        addedWallCoordinates.append(randomWallCoordinate) 
        
        #removes the wall and converse wall from the selection pool
        possibleWallCoordinates.remove(randomWallCoordinate)
        possibleWallCoordinates.remove(wallCoordinatesMaker(targetRoom,randomDirection)[1])



    if optimumWallCount >= 10:
        randomMaze = mazeRandomWallRemover(randomMaze,int(optimumWallCount / 10),addedWallCoordinates)


    return randomMaze





#this function is a set of conditions that an added wall must meet
def mazeRandomizerConditions(maze,targetRoom,direction): 

    #if 3 walls already exist in this room
    if not wallCountChecker(targetRoom): 
        return False

    
    #get the room that will be on the opposite side of the wall
    converseRoom = maze.structure[targetRoom.routes[direction] - 1] 
    if not wallCountChecker(converseRoom): #if 3 walls already exist in converse room
        return False


    #if the added wall will obscure parts of the maze
    outerWallCount = wallChainFinder(maze,targetRoom,direction,[],[],[],0) 
    if outerWallCount > 1:
        return False


    return True





#this function randomly removes walls from the maze to make it more random
def mazeRandomWallRemover(maze,removeCount,wallCoordinates): 

    for index in range(removeCount):
        
        #gets a wall from the selection pool
        randomWallCoordinate = random.choice(wallCoordinates)
        randomRoomPosition = randomWallCoordinate[0]
        randomDirection = randomWallCoordinate[1]


        #if one of the conditions is not met
        while not wallSandwhichFinder(maze,randomRoomPosition,randomDirection):
            
            #removes the wall from the selection pool
            wallCoordinates.remove(randomWallCoordinate) 

            #gets a new wall from the selection pool
            randomWallCoordinate = random.choice(wallCoordinates) 
            randomRoomPosition = randomWallCoordinate[0]
            randomDirection = randomWallCoordinate[1]


        #removes wall from maze if conditions are met
        maze.removeWall(randomRoomPosition,randomDirection) 

        #removes the wall from the selection pool
        wallCoordinates.remove(randomWallCoordinate) 


    return maze





#creates a list of all the routes you can take within the maze
def routesListMaker(maze): 

    routesList = []

    
    for index in range(maze.area):

        currentRoutes = maze.structure[index].routes

        
        for index in range(4):


            if currentRoutes[index] == -1:
                currentRoutes[index] = 0

        routesList.append(currentRoutes)


    return routesList