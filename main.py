import numpy as np
from PIL import Image, ImageDraw

IMAGE_SIZE=1024;
POINT_SIZE=1;

def generate_points(dim, r, k=30, samples=6000):
    """
    Generate a set of points using the Fast Poisson Disk Sampling algorithm in arbitrary dimensions.

    :param dim: The dimension of the space in which to generate points.
    :param r: The minimum distance between points.
    :param k: The number of candidate points to generate for each existing point.
    :param samples: The number of samples to generate before terminating.
    :return: A NumPy array of generated points.
    """
    cell_size = r / np.sqrt(dim)
    grid_size = np.ceil(1 / cell_size).astype(int)
    grid = np.full((grid_size,) * dim,-1)
    
    active_list = []
    points = []
    initial_point = np.random.uniform(size=dim)
    grid_index = tuple(np.floor(initial_point / cell_size).astype(int))
    points.append(initial_point)
    grid[grid_index] = len(points)
    active_list.append(initial_point)



    while active_list:
        point_index = np.random.randint(len(active_list))
        point = active_list[point_index]

        for _ in range(k):
            #OLD
            #candidate_point = point + np.random.normal(size=dim) * r

            #boh
            u=np.random.normal(size=dim)
            candidate_point = point + (u/np.linalg.norm(u) * np.random.uniform(low=r, high=2*r,size=dim))


            if all(0 <= candidate_point[i] < 1 for i in range(dim)):
                candidate_grid_index = tuple(np.floor(candidate_point / cell_size).astype(int))
                conflicting_point_index = grid[candidate_grid_index] - 1

                if conflicting_point_index >= 0 and np.linalg.norm(candidate_point - points[conflicting_point_index]) < r:
                    continue
                grid[candidate_grid_index] = len(points) + 1
                points.append(candidate_point)
                active_list.append(candidate_point)

        if len(points) >= samples:
            break

        active_list.pop(point_index)

    return np.array(points)

# Generate points in 2D
points = generate_points(2, 0.03)

# Display the generated points on an image
img = Image.new('RGB', (IMAGE_SIZE, IMAGE_SIZE), (255, 255, 255))
draw = ImageDraw.Draw(img)
for point in points:
    x, y = point * IMAGE_SIZE
    draw.ellipse((x-POINT_SIZE, y-POINT_SIZE, x+POINT_SIZE, y+POINT_SIZE), fill=(0, 0, 0))
    #draw.point((x, y), fill=(0, 0, 0))
img.show()
