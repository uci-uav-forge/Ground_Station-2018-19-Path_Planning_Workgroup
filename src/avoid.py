from math import *
import json

waypoint_file = open('FlyMission.json','r+')
plan = json.load(waypoint_file)
print(plan)
waypoint_list = plan[0]['mission_waypoints']
obstacle_file = open('Obstacles.json','r')
obstacle_list = json.load(obstacle_file)['stationary_obstacles']
obstacle_file.close()
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
    def __init__(self, aname, pt:Point, rad): #pt:Point
        self.name = aname
        self.center = pt
        self.radius = rad
        self.height = pt.z
    def PrintMe(self):
        print(self.name + " x=" + str(self.center.x) + " y=" + str(self.center.y) + " r=" + str(self.radius) + "z=" + str(self.height))
        

class Line:
    def __init__(self, m, yint):
        self.slope = m
        self.yInt = yint
    def PrintMe(self):
        print("m=" + str(self.slope) + " b=" + str(self.yInt))




def GetLinePts(pt1, pt2):
    m = (pt2.y - pt1.y) / (pt2.x - pt1.x)
    b = pt1.y - (m * pt1.x)
    return(Line(m, b))

def GetLineSlope(pt, m):
    b = pt.y - (m * pt.x)
    return(Line(m, b))

# Solve Quadratic returns a list of solutions to the quadratic formula
def SolveQuadratic(a, b, c):
    d = b**2-4*a*c # discriminant
    if d < 0:
        return ([])
    elif d == 0:
        s1 = (-b)/(2*a)
        return ([s1])
    else:
        s1 = (-b+sqrt(d))/(2*a)
        s2 = (-b-sqrt(d))/(2*a)
        return([s1, s2])

def GetIntersectLineCirc(aline, circ, height):
    # Need to solve quadratic formula
    # First, define some shorthand
    m = aline.slope
    bi = aline.yInt
    x = circ.center.x
    y = circ.center.y
    r = circ.radius

#    print("m=" + str(m) + " bi=" + str(bi) + " x=" + str(x) + " y=" + str(y) + " r=" + str(r)) # debug
    
    # Next, compute a, b, and c
    a = m**2 + 1
    b = 2 * (bi * m - y * m - x)
    c = x**2 + y**2 + bi**2 - r**2 - 2 * bi * y

#    print("a=" + str(a) + " b=" + str(b) + " c=" + str(c)) # debug
    
    # Now, apply the quadratic formula to get the 2 solutions
    solns = SolveQuadratic(a, b, c)
    
    # Now generate the points and return them
    if len(solns) == 0:
        return([])
    elif len(solns) == 1:
        return([Point(solns[0], m * solns[0] + bi, height)])
    elif len(solns) == 2:
        return([Point(solns[0], m * solns[0] + bi, height), Point(solns[1], m * solns[1] + bi, height)])
    else:
        return (-1) # This should never happen

def Midpoint(pt1, pt2):
    return(Point((pt1.x + pt2.x) / 2, (pt1.y + pt2.y) / 2, (pt1.z + pt2.z) / 2))

def GetAvoidPoints(w1, w2, o1):
    # Step 1: Find intersecting points between waypoint line and buffer circle
    wline = GetLinePts(w1, w2)

#    print("Waypoint line") # debug
#    wline.PrintMe() # debug

    SafetyMargin = o1.radius * 0.2
    bcirc = Circle(o1.center, o1.radius + SafetyMargin)

#    print("Buffer circle") # debug
#    bcirc.PrintMe() # debug
	
    aver_z = (w1.z + w2.z) / 2  #average height of w1 and w2
    
    iPts = GetIntersectLineCirc(wline, bcirc, aver_z)
    # Important! Check that intersecting points not between the two waypoints.
    minx = min(w1.x, w2.x)
    maxx = max(w1.x, w2.x)
    miny = min(w1.y, w2.y)
    maxy = max(w1.y, w2.y)
    for pt in iPts:
        if pt.x > maxx or pt.x < minx or pt.y > maxy or pt.y < miny:
            return([])

#    print("Intersecting points") # debug
#    PrintPointList(iPts) # debug

    # Step 2: Check how many intersections there are
    if len(iPts) > 2 or len(iPts) < 0:
        print("Error")
        return(-1)
    if len(iPts) == 0:
        return([])
    if len(iPts) > 0:
        # Step 3: Compute the midpoint of the secant line
        if len(iPts) == 1:
            midPt = iPts[0]
        else: # Two intersection points are found
            midPt = Midpoint(iPts[0], iPts[1])
        # Step 4: Get slope of perpendicular line
        if wline.slope != 0:
            pSlope = -1/wline.slope
        else:
            pSlope = 1000.0
        # Step 5: Generate perpendicular line and double safety circle
        pline = GetLineSlope(midPt, pSlope)
        SafetyMargin = o1.radius * 0.2
        bcirc2 = Circle(o1.center, o1.radius + 2 * SafetyMargin)
        # Step 6: Find the intersection points and return them
        return (GetIntersectLineCirc(pline, bcirc2, aver_z))
    

def checkSafe(pt, o):
    # check if the points in the range of the obstacle
    margin = o.radius * 0.2
    return not (o.center.x - o.radius - margin < pt.x and pt.x < o.center.x + o.radius + margin and \
        o.center.y - o.radius - margin < pt.y and pt.y < o.center.y + o.radius + margin and pt.z < o.height)
    
    
def getSafePts(pts, w2, o1):
    safePts = []
    for pt in pts:
        #check new line between new waypoint and next waypoint
        w1 = Waypoint("new", pt.x, pt.y, pt.z)
        points = GetAvoidPoints(w1, w2, o1)
        if points != []:
            continue        
        #check new waypoint with other obstacle
        if all(checkSafe(pt, o) for o in ObstacleList):
            safePts.append(pt)

#             safePts.add(pt)
    if len(safePts) == 0:
        #reduce the margin but for now just return pts
        return pts
    
    return safePts
    

def FixSingleSegment():
    global WaypointSeq
    prevPt = WaypointSeq[0]
    for i in range(1, len(WaypointSeq)):
        for ob in ObstacleList:
			# height checking
            min_h = min(prevPt.z, WaypointSeq[i].z)
            if min_h > ob.center.z + 20:
                continue
            averg_h = (prevPt.z + WaypointSeq[i].z) / 2
            aPts = GetAvoidPoints(prevPt, WaypointSeq[i], ob)
            if len(aPts) > 0: # Crossing
                #check aPts position
                safePts = getSafePts(aPts, WaypointSeq[i], ob)
                WaypointSeq.insert(i, safePts[0])
                return(False)
        prevPt = WaypointSeq[i]
    return(True)

def SolveProblem():
    done = False
    print('waypt\n',WaypointSeq)
    while not(done):
        DrawSolution(WaypointSeq, ObstacleList)
        done = FixSingleSegment()

#######################################################
# Test Code
#######################################################

WaypointSeq = []
ObstacleList = []

# TestInitProblem just creates a set of waypoints and obstacles for testing
def create_waypoints(waypt_list):

    return [Waypoint('w'+str(waypt['order']),waypt['latitude'],waypt['longitude'],waypt['altitude_msl']) for waypt in sorted(waypt_list,key = lambda x:x['order'])]

def create_obstacles(obs_list):
    return [Obstacle('o'+str(i),Point(obs['latitude'],obs['longitude'],obs['cylinder_height']),obs['cylinder_radius']) for i,obs in enumerate(obs_list)]
def TestInitProblem():
    global WaypointSeq
    global ObstacleList


    WaypointSeq = [Waypoint('w1', 10, 500, 50), Waypoint('w2', 600, 550, 100), Waypoint('w3', 1200, 500, 200)]

    ObstacleList = [Obstacle('o1', Point(500,500,50), 50), Obstacle('o2', Point(1000,500,75), 50)]

    WaypointSeq = [Waypoint('w1', 10, 500, 50), Waypoint('w2', 1000, 550, 100), Waypoint('w3', 1400, 500, 200)]

    ObstacleList = [Obstacle('o1', Point(500,500,75), 50), Obstacle('o2', Point(1200,500,75), 50)] # 
    WaypointSeq = create_waypoints(waypoint_list)
    ObstacleList =create_obstacles(obstacle_list)

def PrintWaypointSeq(wseq):
    print("Waypoint Sequence")
    for w in wseq:
        w.PrintMe()

def jObstacleList(oseq):
    print("Obstacle List")
    for o1 in oseq:
        o1.PrintMe()

def PrintPointList(pseq):
    for p in pseq:
        p.PrintMe()

#######################################################
# Drawing code (still test code)
#######################################################

from tkinter import *

def InitGui():

    master = Tk()

    w = Canvas(master, width=2000, height=1000)
    w.pack()
    return(w)

def StartGui():
    mainloop()

def DrawWaypoint(myCanvas, pt):
    PR = 3
    x = pt.x
    y = pt.y
    z = pt.z
    item = myCanvas.create_oval(pt.x-PR, pt.y-PR, pt.x+PR, pt.y+PR, fill="blue", outline="black")
    ###test zone
    myCanvas.create_text(x+2*PR,y+2*PR,text="height: {}".format(z),fill="green")

    
def DrawObstacle(myCanvas, o1):
    x = o1.center.x
    y = o1.center.y
    r = o1.radius
    h = o1.center.z
    myCanvas.create_oval(x-r, y-r, x+r, y+r, fill="red", outline="black")
    myCanvas.create_text(x-r-5,y-r-5,text="height: {}".format(h))

def DrawLineSeg(myCanvas, pt1, pt2):
    myCanvas.create_line(pt1.x, pt1.y, pt2.x, pt2.y, fill="blue")

def DrawWaypointSeq(myCanvas, wseq):
    DrawWaypoint(myCanvas, wseq[0])
    prevPt = wseq[0]
    for i in range(1, len(wseq)):
        DrawWaypoint(myCanvas, wseq[i])
        DrawLineSeg(myCanvas, prevPt, wseq[i])
        prevPt = wseq[i]
        
def DrawSolution(wseq, olist):
    w = InitGui()
    DrawWaypointSeq(w, wseq)
    for ob in olist:
        DrawObstacle(w, ob)
    StartGui()

### Some test code
TestInitProblem()
#x = GetAvoidPoints(WaypointSeq[0], WaypointSeq[1], ObstacleList[0])
#PrintWaypointSeq(WaypointSeq)
#PrintObstacleList(ObstacleList)
#main()
#DrawSolution(WaypointSeq, ObstacleList)
SolveProblem()
plan[0]['mission_waypoints'] = [{'altitude_msl':w.z,'latitude':w.x,'longitude':w.y,'order':i+1} for i,w in enumerate(WaypointSeq)]
waypoint_file.seek(0)
json.dump(plan,waypoint_file)
waypoint_file.truncate()
waypoint_file.close()
#DrawSolution(WaypointSeq, ObstacleList)

