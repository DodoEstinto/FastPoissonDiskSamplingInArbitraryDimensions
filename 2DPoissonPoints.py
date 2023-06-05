import numpy as np
import matplotlib.pyplot as plt
import math
from PIL import Image, ImageDraw

# they must be some type of integer, no float allowed.
WIDTH = 2
HEIGHT = 2

# for display purpouse
POINTS_SIZE = 6

# adjust the radius automatically
r = 0.038*(max(HEIGHT, WIDTH))
k = 30

# used only for PIL display
IMAGE_SIZE = 1024

"""
Generate a random point around "point" in an anulus of r-2r.
"""


def random_point(point, r):

    # generate the angle from the point
    theta = np.random.uniform(0, 2*math.pi)
    # generate the distance from the point, between r and 2r
    distance = np.random.uniform(r, 2*r)
    # add the point generated to the list of random points
    point = ((point[0]+distance*np.sin(theta),
              point[1]+distance*np.cos(theta)))
    return point


"""
Add "point" in "grid" and in "active_list" given a cellsize.
"""


def add_point(grid, active_list, cellsize, point):
    active_list.append(point)
    i, j = int(point[0]/cellsize), int(point[1]/cellsize)
    grid[i, j] = point


"""
Given a "point", check the absence in "grid"  of another point in a r radius.
"""


def check_distances(grid, rows, cols, cellsize, r, point):
    i, j = int(point[0]/cellsize), int(point[1]/cellsize)
    # check if the cell is occupied
    if grid[i, j][0] > -1:
        return False
    row, col = i, j
    iMin = max(0, row-2)
    jMin = max(0, col-2)
    iMax = min(row+2, rows)
    jMax = min(col+2, cols)
    # check all the conflict zones
    for i in range(iMin, iMax):
        for j in range(jMin, jMax):
            if i != row or j != col:
                if grid[i, j][0] > -1:
                    # for every cell occupied, check the distance
                    if math.sqrt(math.pow(point[0]-grid[i, j][0], 2)+math.pow(point[1]-grid[i, j][1], 2)) < r:
                        return False

    # no conflict found, the point is ok
    return True


"""
Generate poisson points in a radius r, trying k times for every point.
"""


def generate_poisson_points(r=0.038, k=30):

    cellsize = r/np.sqrt(2)
    rows = int(np.ceil(WIDTH/cellsize))
    cols = int(np.ceil(HEIGHT/cellsize))

    grid = np.full((rows, cols, 2), -1.0)

    active_list = []
    # add a random point
    add_point(grid, active_list, cellsize,
              (np.random.uniform(WIDTH), np.random.uniform(HEIGHT)))
    while len(active_list):
        index = np.random.randint(len(active_list))
        point = active_list.pop(index)
        found = False
        for _ in range(k):
            newPoint = random_point(point, r)
            if 0 <= newPoint[0] and newPoint[0] < WIDTH and 0 <= newPoint[1] and newPoint[1] < HEIGHT and check_distances(grid, rows, cols, cellsize, r, newPoint):
                add_point(grid, active_list, cellsize, newPoint)
                found = True
                break
        if found:
            active_list.append(point)

    poisson_points = []
    for i in range(rows):
        for j in range(cols):
            point = grid[i, j]
            if (point[0] != -1):
                poisson_points.append(point)

    return poisson_points


points = generate_poisson_points(r, k)

# Display the generated points on a plot
plt.figure()
plt.subplot(1, 1, 1, aspect=1)

X = []
Y = []
for (x, y) in points:
    X.append(x)
    Y.append(y)

plt.title("Fast Poisson Disk Sampling in 2 Dimensions\n r="+str(r)+"  k="+str(k))
plt.scatter(X, Y, s=POINTS_SIZE)
plt.xlabel("X")
plt.xlim(0, WIDTH)
plt.ylabel("Y")
plt.ylim(0, HEIGHT)
plt.show()

"""
# Display the generated points on an image
img = Image.new('RGB', (1024, 1024), (255, 255, 255))
draw = ImageDraw.Draw(img)
points = generate_poisson_points(r,30)
for point in points:
    x, y = point [0]/HEIGHT*IMAGE_SIZE, point[1]/WIDTH*IMAGE_SIZE
    draw.ellipse((x-POINT_SIZE, y-POINT_SIZE, x+POINT_SIZE, y+POINT_SIZE), fill=(0, 0, 0))
    #draw.point((x, y), fill=(0, 0, 0))
img.show()
"""
