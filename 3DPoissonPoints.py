import numpy as np
import matplotlib.pyplot as plt
import math

# size of the space where the points are allowed.
# they must be some type of integer, no float allowed.
WIDTH = 2
HEIGHT = 2
DEPTH = 2

# for display purpouse
POINT_SIZE = 6

# adjust the radius automatically-
r = 0.20*(max(HEIGHT, WIDTH, DEPTH))
k = 45


"""
generate k random points around "point" in an anulus of r-2r.
"""


def random_point(point, r):

    # Source:  https://math.stackexchange.com/questions/87230/picking-random-points-in-the-volume-of-sphere-with-uniform-probability
    # generate the angles from the point
    theta = np.random.uniform(0, 2*math.pi)
    v = np.random.uniform(0, 1)
    gamma = np.arccos(2*v-1)
    distance = r*(math.pow(np.random.uniform(0, 1), 1/3))+r
    # add the point generated to the list of random points
    point = ((point[0]+distance*np.cos(theta)*np.sin(gamma), point[1] +
              distance*np.sin(theta)*np.cos(gamma), point[2]+distance*np.cos(gamma)))
    return point


"""
Add "point" in "grid" and in "active_list" given a cellsize.
"""


def add_point(grid, active_list, cellsize, point):
    active_list.append(point)
    i, j, k = int(point[0]/cellsize), int(point[1] /
                                          cellsize), int(point[2]/cellsize)
    grid[i, j, k] = point


"""
Given a "point", check the absence in "grid" of another point in a r radius.
"""


def check_distances(grid, rows, cols, depth, cellsize, r, point):
    i, j, k = int(point[0]/cellsize), int(point[1] /
                                          cellsize), int(point[2]/cellsize)
    if grid[i, j, k][0] > -1:
        return False

    row, col, deep = i, j, k
    iMin = max(0, row-2)
    jMin = max(0, col-2)
    kMin = max(0, deep-2)
    iMax = min(row+2, rows)
    jMax = min(col+2, cols)
    kMax = min(deep+2, depth)
    for i2 in range(iMin, iMax):
        for j2 in range(jMin, jMax):
            for k2 in range(kMin, kMax):
                if i2 != row or j2 != col or k2 != deep:
                    if grid[i2, j2, k2][0] > -1:
                        if math.sqrt(math.pow(point[0]-grid[i2, j2, k2][0], 2)+math.pow(point[1]-grid[i2, j2, k2][1], 2)+math.pow(point[2]-grid[i2, j2, k2][2], 2)) < r:
                            return False

    return True


"""
generate poisson points in a radius r, trying k times for every point.
"""


def generate_poisson_points(r=0.038, k=30):

    cellsize = r/np.sqrt(3)
    rows = int(np.ceil(WIDTH/cellsize))
    cols = int(np.ceil(HEIGHT/cellsize))
    z = int(np.ceil(DEPTH/cellsize))

    grid = np.full((rows, cols, z, 3), -1.0)

    active_list = []
    add_point(grid, active_list, cellsize, (np.random.uniform(WIDTH),
              np.random.uniform(HEIGHT), np.random.uniform(DEPTH)))
    while len(active_list):
        index = np.random.randint(len(active_list))
        point = active_list.pop(index)

        found = False
        for _ in range(k):
            newPoint = random_point(point, r)
            if 0 <= newPoint[0] and newPoint[0] < WIDTH and 0 <= newPoint[1] and newPoint[1] < HEIGHT and 0 <= newPoint[2] and newPoint[2] < DEPTH and check_distances(grid, rows, cols, z, cellsize, r, newPoint):
                add_point(grid, active_list, cellsize, newPoint)
                found = True
                break
        if found:
            active_list.append(point)

    poisson_points = []
    for i in range(rows):
        for j in range(cols):
            for k in range(z):
                point = grid[i, j, k]
                if (point[0] != -1):
                    poisson_points.append(point)

    return poisson_points


points = generate_poisson_points(r, k)
X = []
Y = []
Z = []
for (x, y, z) in points:
    X.append(x)
    Y.append(y)
    Z.append(z)

# source: https://matplotlib.org/stable/gallery/mplot3d/scatter3d.html
ax = plt.figure().add_subplot(projection='3d')
plt.title("Fast Poisson Disk Sampling in 3 Dimensions\n r="+str(r)+"  k="+str(k))
# change color based on the height
ax.scatter(X, Y, Z, s=POINT_SIZE, c=np.divide(X, HEIGHT))
ax.set_xlabel("X")
ax.set_xlim(0, WIDTH)
ax.set_ylabel("Y")
ax.set_ylim(0, HEIGHT)
ax.set_zlabel("Z")
ax.set_zlim(0, DEPTH)


plt.show()
