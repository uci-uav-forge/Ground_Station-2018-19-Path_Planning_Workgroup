import storage
import drawer

from math import *


#only work for 2D
def GetLinePts(pt1, pt2):
    m = (pt2.y - pt1.y) / (pt2.x - pt1.x)
    b = pt1.y - (m * pt1.x)
    return(storage.Line(m, b))

def GetLineSlope(pt, m):
    b = pt.y - (m * pt.x)
    return(storage.Line(m, b))

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
        return([storage.Point(solns[0], m * solns[0] + bi, height)])
    elif len(solns) == 2:
        return([storage.Point(solns[0], m * solns[0] + bi, height), storage.Point(solns[1], m * solns[1] + bi, height)])
    else:
        return (-1) # This should never happen

def Midpoint(pt1, pt2):
    return(storage.Point((pt1.x + pt2.x) / 2, (pt1.y + pt2.y) / 2, (pt1.z + pt2.z) / 2))

def GetAvoidPoints(w1, w2, o1):
    # Step 1: Find intersecting points between waypoint line and buffer circle
    wline = GetLinePts(w1, w2)

#    print("Waypoint line") # debug
#    wline.PrintMe() # debug

    SafetyMargin = o1.radius * 0.2
    bcirc = storage.Circle(o1.center, o1.radius + SafetyMargin)

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
        bcirc2 = storage.Circle(o1.center, o1.radius + 2 * SafetyMargin)
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
        w1 = storage.Waypoint("new", pt.x, pt.y, pt.z)
        points = GetAvoidPoints(w1, w2, o1)
        if points != []:
            continue        
        #check new waypoint with other obstacle
        if all(checkSafe(pt, o) for o in storage.obstacleList):
            safePts.append(pt)

#             safePts.add(pt)
    if len(safePts) == 0:
        #reduce the margin but for now just return pts
        return pts
    
    return safePts
    
def FixSingleSegment():
    prevPt = storage.waypointSeq[0]
    for i in range(1, len(storage.waypointSeq)):
        for ob in storage.obstacleList:
			# height checking
            min_h = min(prevPt.z, storage.waypointSeq[i].z)
            if min_h > ob.center.z + 20:
                continue
            averg_h = (prevPt.z + storage.waypointSeq[i].z) / 2
            aPts = GetAvoidPoints(prevPt, storage.waypointSeq[i], ob)
            if len(aPts) > 0: # Crossing
                #check aPts position
                safePts = getSafePts(aPts, storage.waypointSeq[i], ob)
                storage.waypointSeq.insert(i, safePts[0])
                return(False)
        prevPt = storage.waypointSeq[i]
    return(True)

def solveProblem():
    done = False
    while not(done):
        drawer.DrawSolution(storage.waypointSeq, storage.obstacleList)
        done = FixSingleSegment()