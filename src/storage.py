class Point:
    def __init__(self, xval=0.0, yval=0.0, zval=0.0):
        self.x = xval
        self.y = yval
        self.z = zval
    def PrintMe(self):
        print("x=" + str(self.x) + " y=" + str(self.y) + "z=" + str(self.z))

class Waypoint(Point):
    def __init__(self, aname, xval=0.0, yval=0.0, zval=0.0):
        self.name = aname
        self.x = xval
        self.y = yval
        self.z = zval
    def PrintMe(self):
        print(self.name + "x=" + str(self.x) + " y=" + str(self.y) + "z=" + str(self.z))

class Circle:
    def __init__(self, pt:Point, rad): #pt:Point
        self.center = pt
        self.radius = rad
    def PrintMe(self):
        print("x=" + str(self.center.x) + " y=" + str(self.center.y) + " r=" + str(self.radius))
      
class Obstacle(Circle):
    def __init__(self, aname, pt:Point, rad): #pt:Point(pt.z is the height)
        self.name = aname
        self.center = pt
        self.radius = rad
        self.height = pt.z
    def PrintMe(self):
        print(self.name + " x=" + str(self.center.x) + " y=" + str(self.center.y) + " r=" + str(self.radius) + "z(Height)=" + str(self.height))

class Line:
    def __init__(self, m, yint):
        self.slope = m
        self.yInt = yint
    def PrintMe(self):
        print("m=" + str(self.slope) + " b=" + str(self.yInt))

waypointSeq = []
obstacleList = []

def readMissionFile():
    # Need to change to read a mission.json file in the future.
    
    global waypointSeq
    global obstacleList
  
    waypointSeq = [Waypoint('w1', 10, 10, 50),
                   Waypoint('w2', 25, 550, 75), 
                   Waypoint('w3', 500, 750, 100),
                   Waypoint('w4', 510, 50, 125),
                   Waypoint('w5', 550, 60, 150),
                   Waypoint('w6', 560, 700, 150),
                   Waypoint('w7', 1200, 500, 150)]

    obstacleList = [Obstacle('o1', Point(200,700,500), 75),
                    Obstacle('o2', Point(500,500,500), 75),
                    Obstacle('o3', Point(1000,500,750), 100),
                    Obstacle('o4', Point(750,600,200), 50)]

