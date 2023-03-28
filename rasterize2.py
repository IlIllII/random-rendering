import sys
import pygame
import math
from pygame.locals import QUIT

# Set up display
pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Cube vertices
vertices = [
    (-1, -1, -1),
    (-1, -1, 1),
    (-1, 1, -1),
    (-1, 1, 1),
    (1, -1, -1),
    (1, -1, 1),
    (1, 1, -1),
    (1, 1, 1),
]

# Cube faces as triangles
faces = [
    (0, 1, 2),
    (1, 2, 3),
    (0, 1, 4),
    (1, 4, 5),
    (0, 2, 4),
    (2, 4, 6),
    (2, 3, 6),
    (3, 6, 7),
    (1, 3, 5),
    (3, 5, 7),
    (4, 5, 6),
    (5, 6, 7),
]

for j, face in enumerate(faces):
    tri = []
    for i in range(3):
        tri.append(list(vertices[face[i]]))
    for i, p in enumerate(tri):
        for j in range(3):
            tri[i][j] *= 25
    print(tri)

# Rotation matrix
def rotation_matrix(axis, theta):
    a = math.cos(theta / 2)
    b, c, d = [-i * math.sin(theta / 2) for i in axis]
    return [
        [a * a + b * b - c * c - d * d, 2 * (b * c - a * d), 2 * (b * d + a * c)],
        [2 * (b * c + a * d), a * a + c * c - b * b - d * d, 2 * (c * d - a * b)],
        [2 * (b * d - a * c), 2 * (c * d + a * b), a * a + d * d - b * b - c * c],
    ]

def get_bounding_box(triangle):
    min_x = min(triangle[0][0], triangle[1][0], triangle[2][0])
    min_y = min(triangle[0][1], triangle[1][1], triangle[2][1])
    max_x = max(triangle[0][0], triangle[1][0], triangle[2][0])
    max_y = max(triangle[0][1], triangle[1][1], triangle[2][1])
    return (min_x, min_y, max_x, max_y)



def point_in_triangle(point, triangle):
    (x, y) = point
    (x1, y1), (x2, y2), (x3, y3) = triangle

    # Compute barycentric coordinates
    denominator = ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
    if denominator == 0:
        return False
    a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
    b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
    c = 1 - a - b

    # Check if the point is inside the triangle
    return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1



# Matrix multiplication
def multiply_matrix_vector(matrix, vector):
    return [sum([matrix[i][j] * vector[j] for j in range(3)]) for i in range(3)]

# Rendering function
def render(vertices, angle_x, angle_y, angle_z):
    screen.fill((0, 0, 0))

    rotated_vertices = []
    for vertex in vertices:
        rotated = multiply_matrix_vector(rotation_matrix((1, 0, 0), angle_x), vertex)
        rotated = multiply_matrix_vector(rotation_matrix((0, 1, 0), angle_y), rotated)
        rotated = multiply_matrix_vector(rotation_matrix((0, 0, 1), angle_z), rotated)
        rotated_vertices.append(rotated)

    scaling_factor = 50
    projected_vertices = [(WIDTH // 2 + int(v[0] * scaling_factor), HEIGHT // 2 + int(v[1] * scaling_factor)) for v in rotated_vertices]

    for j, face in enumerate(faces):
        tri = []
        for i in range(3):
            tri.append(projected_vertices[face[i]])
            x1, y1 = projected_vertices[face[i]]
            x2, y2 = projected_vertices[face[(i + 1) % 3]]
            # pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2))
        for x in range(math.floor(get_bounding_box(tri)[0]), math.ceil(get_bounding_box(tri)[2])):
            for y in range(math.floor(get_bounding_box(tri)[1]), math.ceil(get_bounding_box(tri)[3])):
                if point_in_triangle((x, y), tri):
                    screen.set_at((x, y), (j * 20, 255 - j * 20, i * i))

    pygame.display.flip()

# Main loop
angle = 0
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    angle += 0.01
    render(vertices, angle, angle, angle)
    clock.tick(60)
