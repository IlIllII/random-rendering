print("Hello")

import pygame
import math

def rotation_matrix(axis, theta):
    a = math.cos(theta / 2)
    b, c, d = [-i * math.sin(theta / 2) for i in axis]
    return [
        [a * a + b * b - c * c - d * d, 2 * (b * c - a * d), 2 * (b * d + a * c)],
        [2 * (b * c + a * d), a * a + c * c - b * b - d * d, 2 * (c * d - a * b)],
        [2 * (b * d - a * c), 2 * (c * d + a * b), a * a + d * d - b * b - c * c],
    ]

def multiply_matrix_vector(matrix, vector):
    return [sum([matrix[i][j] * vector[j] for j in range(3)]) for i in range(3)]

def point_in_triangle(point, triangle):
    (x, y) = point
    (x1, y1), (x2, y2), (x3, y3) = triangle

    # Compute barycentric coordinates
    denominator = ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
    a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominator
    b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominator
    c = 1 - a - b

    # Check if the point is inside the triangle
    return 0 <= a <= 1 and 0 <= b <= 1 and 0 <= c <= 1



pygame.init()


tris = [
    [[-25, -25, -25], [-25, -25, 25], [-25, 25, -25]],
    [[-25, -25, 25], [-25, 25, -25], [-25, 25, 25]],
    [[-25, -25, -25], [-25, 25, -25], [25, -25, -25]],
    [[-25, -25, -25], [25, -25, -25], [25, -25, 25]],
    [[-25, -25, -25], [25, -25, 25], [-25, -25, 25]],
    [[-25, -25, 25], [25, -25, 25], [25, 25, 25]],
    [[-25, -25, 25], [25, 25, 25], [-25, 25, 25]],
    [[-25, 25, -25], [-25, 25, 25], [25, 25, -25]],
    [[-25, 25, -25], [25, 25, -25], [25, 25, 25]],
    [[25, -25, -25], [25, -25, 25], [25, 25, -25]],
    [[25, -25, 25], [25, 25, -25], [25, 25, 25]],
    [[-25, -25, -25], [-25, 25, -25], [25, -25, -25]],
    [[-25, -25, -25], [25, -25, -25], [25, 25, -25]],
]

size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")


done = False


clock = pygame.time.Clock()



def get_bounding_box(triangle):
    min_x = min(triangle[0][0], triangle[1][0], triangle[2][0])
    min_y = min(triangle[0][1], triangle[1][1], triangle[2][1])
    max_x = max(triangle[0][0], triangle[1][0], triangle[2][0])
    max_y = max(triangle[0][1], triangle[1][1], triangle[2][1])
    return (min_x, min_y, max_x, max_y)

count = 0

current_time = pygame.time.get_ticks()

def translated(triangle, x, y, z):
    for vertex in triangle:
        vertex[0] += x
        vertex[1] += y
        vertex[2] += z
    return triangle

def rotate_triangle(triangle, rotation_matrix):
    for vertex in triangle:
        vertex[0], vertex[1], vertex[2] = multiply_matrix_vector(rotation_matrix, vertex)
    return triangle

while not done:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    count += 1

    screen.fill((255, 255, 255))
    
    tri_count = 0
    translated_tris = []
    for tri in tris:
        tri_count += 1
        tri_copy = [vertex.copy() for vertex in tri]
        new_tri = rotate_triangle(tri_copy, rotation_matrix((0, 1, 0), current_time / 1000))
        new_tri = rotate_triangle(new_tri, rotation_matrix((1, 0, 0), current_time / 1000))
        new_tri = rotate_triangle(new_tri, rotation_matrix((0, 0, 1), current_time / 1000))
    
        
        translated_tri = translated(new_tri, 250, 150, 0)
        translated_tris.append(translated_tri)
        tri2D = [(translated_tri[0][0], translated_tri[0][1]), (translated_tri[1][0], translated_tri[1][1]), (translated_tri[2][0], translated_tri[2][1])]


    for i, translated_tri in enumerate(translated_tris):
        for x in range(math.floor(get_bounding_box(translated_tri)[0]), math.ceil(get_bounding_box(translated_tri)[2])):
            for y in range(math.floor(get_bounding_box(translated_tri)[1]), math.ceil(get_bounding_box(translated_tri)[3])):
                tri2D = [(translated_tri[0][0], translated_tri[0][1]), (translated_tri[1][0], translated_tri[1][1]), (translated_tri[2][0], translated_tri[2][1])]
                if point_in_triangle((x, y), tri2D):
                    screen.set_at((x, y), (i * 20, 255 - i * 10, i * 15))

        

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

