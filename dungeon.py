from random import randint
from math import exp
import sys

class block(object):
    """docstring for block"""
    types = ['open', 'closed', 'damage']

    def __init__(self):
        super(block, self).__init__()
        self.blocktype = 'closed'

    def printblock(self):
        if self.blocktype == 'open':
            print(' ', end="")
        if self.blocktype == 'closed':
            print('X', end="")
        if self.blocktype == 'door':
            print('D', end="")

    def pixelprintblock(self):
        if self.blocktype == 'open':
            return ' '
        if self.blocktype == 'closed':
            return 'X'
        if self.blocktype == 'door':
            return 'D'

    def setposition(self, x, y):
        self.x = x
        self.y = y

    def settype(self, newtype):
        self.blocktype = newtype


class room(object):
    """docstring for room"""
    def __init__(self, x, y):
        super(room, self).__init__()
        self.x = x
        self.y = y
        self.length = 19
        self.width = 31
        self.size = self.width * self.length
        self.blockarray = []  # 2d array 16:9
        self.mapped = False
        for i in range(self.width * self.length):
            b = block()
            self.blockarray.append(b)
            self.blockarray[i].setposition(i % self.width, int(i / self.width))

    def printroom(self):
        for i in range(self.length):
            for j in range(self.width):
                self.blockarray[self.width * i + j].printblock()
            print()
    
    def printrow(self, row):
        for j in range(self.width):
                self.blockarray[self.width * row + j].printblock()
    def pixelprintrow(self,row):
        templist = []
        for j in range(self.width):
                templist += self.blockarray[self.width * row + j].pixelprintblock()
        return templist

    def roomcreator(self, roomDict):
        for i in range(self.size):
            if (i>self.width-1 and i < self.size-self.width and i%self.width != 0 and i%self.width != self.width-1):
                self.blockarray[i].settype('open')
            if (i == int(self.width/2) and roomDict.keys().__contains__(Point(self.x,self.y-1))):
                self.blockarray[i].settype('door')
            if (i == (self.size-int(self.width/2)-1) and roomDict.keys().__contains__(Point(self.x,self.y+1)) ):
                self.blockarray[i].settype('door')
            if (i == int(self.size/2) - int(self.width/2) and roomDict.keys().__contains__(Point(self.x-1,self.y))):
                self.blockarray[i].settype('door')
            if (i == int(self.size/2) + int(self.width/2) and roomDict.keys().__contains__(Point(self.x+1,self.y))):
                self.blockarray[i].settype('door')

    def setpos(self,x,y):
        self.x =x
        self.y=y

    def convertxy(self, x, y):
        return self.width * y + x

class Point(object):
    """docstring for Point"""
    def __init__(self, x, y):
        super(Point, self).__init__()
        self.x = x
        self.y = y
    def __eq__(self,other):
        return isinstance(other, self.__class__) and self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))  
    def __str__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

class Floor(object):
    """docstring for Floor"""
    roomconst = randint(15,35) #defines how many rooms wanted per floor approx
    def __init__(self):
        super(Floor, self).__init__()
        roomHead = room(0,0)
        self.width = roomHead.width
        self.length = roomHead.length
        self.rrange = roomHead.length
        roomList = []
        self.roomDict = {} #Point:Room
        temproomDict = {}
        roomList.append(roomHead)
        count =-1
        minx = 999
        miny = 999
        maxx = -999
        maxy = -999
        while (len(roomList) >0):
            tempRoom = roomList.pop()
            tempPoint = Point(tempRoom.x, tempRoom.y)
            if not temproomDict.keys().__contains__(tempPoint):
                count+=1
            temproomDict[tempPoint] = tempRoom
            tempcount = count-1
            for d in range(4):
                tempcount+=1
                deltax=0
                deltay=0

                if d ==0:
                    deltay= 1
                if d ==1:
                    deltax= 1
                if d==2:
                    deltay = -1
                if d==3:
                    deltax= -1
                if (randint(0, 100) <= 100 * exp(-2.71* tempcount / self.roomconst)):
                    ##make a new room
                    newx = tempRoom.x+deltax
                    newy = tempRoom.y+deltay
                    if newx > maxx:
                        maxx=newx
                    if newx < minx:
                        minx=newx
                    if newy > maxy:
                        maxy=newy
                    if newy < miny:
                        miny=newy
                    roomList.append(room(newx,newy))                  
        #shift to origin
        for k in temproomDict.keys():
            temproomDict[k].setpos(temproomDict[k].x - minx, temproomDict[k].y - miny)
            self.roomDict[Point(k.x - minx,k.y -miny)] = temproomDict[k]
        self.shiftedmaxx = maxx - minx
        self.shiftedmaxy = maxy - miny
        
        #generate rooms
        for v in self.roomDict.values():
            v.roomcreator(self.roomDict)

    def printMap(self):
        for k in self.roomDict.keys():
            #print(k)
            pass
        for y in range(-1, self.shiftedmaxy+2):
            for x in range(-1, self.shiftedmaxx+2):
                p = Point(x,y)
                
                if (y == -1 or y == self.shiftedmaxy+1) or (x == -1 or x == self.shiftedmaxx+1):
                    sys.stdout.write("*")
                elif self.roomDict.keys().__contains__(p):
                   sys.stdout.write("R")
                else:
                    sys.stdout.write(" ")
            print("")

    def pixelMap(self):
        returnstring = []
        for k in self.roomDict.keys():
            #print(k)
            pass
        for y in range(-1,self.shiftedmaxy+2):
            for x in range(-1, self.shiftedmaxx+2):
                p = Point(x,y)
                
                if (y == -1 or y == self.shiftedmaxy+1) or (x == -1 or x == self.shiftedmaxx+1):
                   returnstring += '*'
                elif self.roomDict.keys().__contains__(p):
                   returnstring += 'R'
                else:
                    returnstring += ' '
            returnstring += 'n'
        return returnstring


    def printFloor(self):
        wall = room(-1,-1)
        rrange = self.rrange
        for y in range(self.shiftedmaxy+1):
            for r in range(rrange):
                for x in range(self.shiftedmaxx+1):
                    p = Point(x,y)

                    if self.roomDict.keys().__contains__(p):
                       self.roomDict[p].printrow(r)
                    else:
                        wall.printrow(r)    
                    print(" ", end = "")
                print("")
            print("")    

    def pixelFloor(self):
        returnstring = []
        wall = room(-1,-1)
        rrange = self.rrange
        for y in range(self.shiftedmaxy+1):
            for r in range(rrange):
                for x in range(self.shiftedmaxx+1):
                    p = Point(x,y)

                    if self.roomDict.keys().__contains__(p):
                       returnstring += self.roomDict[p].pixelprintrow(r)
                    else:
                        returnstring += wall.pixelprintrow(r)    
                    #returnstring += ' '
                returnstring += 'n'
            #returnstring += 'n' 
        return returnstring  


def main():
    f = Floor()
    f.printFloor()

