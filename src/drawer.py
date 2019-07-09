
from tkinter import *
import storage

#######################################################
# Drawing code (still test code)
#######################################################

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



##################################################
# Draw Solutioin in 3D
##################################################
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def drawSoltuionIn3D():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    # Plot the obstacle
    ##################################################
    for currentObsacle in storage.obstacleList:
        # Cylinder
        x = np.linspace(-currentObsacle.radius, currentObsacle.radius, 100)
        z = np.linspace(0, currentObsacle.height, 100)
        Xc, Zc = np.meshgrid(x, z)
        Yc = np.sqrt(currentObsacle.radius**2 - Xc**2)

        # Draw parameters
        rstride = 20
        cstride = 10
        ax.plot_surface(Xc + currentObsacle.center.x , Yc + currentObsacle.center.y, Zc, alpha=0.2, rstride=rstride, cstride=cstride)
        ax.plot_surface(Xc + currentObsacle.center.x, -Yc + currentObsacle.center.y, Zc, alpha=0.2, rstride=rstride, cstride=cstride)


    #Plot the waypoint and lines in between
    ##################################################

    #Load the first waypoint
    x = [storage.waypointSeq[0].x, 0]
    y = [storage.waypointSeq[0].y, 0]
    z = [storage.waypointSeq[0].z, 0]

    #draw each line segment
    for i in range(len(storage.waypointSeq)):

        #load the next waypoint
        x[1] = storage.waypointSeq[i].x
        y[1] = storage.waypointSeq[i].y
        z[1] = storage.waypointSeq[i].z

        #draw a line
        ax.plot(x, y, z, label='Flight Path')

        #move the current waypoint to become the last waypint
        x[0] = storage.waypointSeq[i].x
        y[0] = storage.waypointSeq[i].y
        z[0] = storage.waypointSeq[i].z
        

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    #Set axis limit here
    ax.set_xlim3d(0, 1500)
    ax.set_ylim3d(0, 1500)
    ax.set_zlim3d(0, 750)

    plt.show()