import storage
import solver
import drawer

#######################################################
# Main function starts from here:
#######################################################
storage.readMissionFile()

solver.solveProblem()

drawer.drawSoltuionIn3D()

#######################################################
# Test Code
#######################################################
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