print("Hello")

import pygame
import math


def cross_product(a, b):
    return a[0] * b[1] - a[1] * b[0]

def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1]

def subtract(a, b):
    return (a[0] - b[0], a[1] - b[1])

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def same_side(a, b, c, d):
    cp1 = cross_product(subtract(d, c), subtract(a, c))
    cp2 = cross_product(subtract(d, c), subtract(b, c))
    if cp1 * cp2 >= 0:
        return True
    return False

def contains(triangle, point):
    a = triangle[0]
    b = triangle[1]
    c = triangle[2]
    if same_side(point, a, b, c) and same_side(point, b, a, c) and same_side(point, c, a, b):
        return True
    return False

def matrix_mult(matrix, vector):
    result = []
    for row in matrix:
        result.append(dot_product(row, vector))
    return result

def project(point, screen_width, screen_height, fov=500):
    x, y, z = point
    factor = fov / (z + fov)
    x = x * factor + screen_width // 2
    y = y * factor + screen_height // 2
    return (x, y)


def rotate_in_place(triangle, angle, origin, rotation_matrix):
    result = []
    for point in triangle:
        result.append(add_vec3(matrix_mult(rotation_matrix, subtract_vec3(point, origin)), origin))
    return result

def add_vec3(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])

def subtract_vec3(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])

def rotated(triangle, rotation_matrix):
    result = []
    for point in triangle:
        result.append(matrix_mult(rotation_matrix, point))
        print(result[-1])
    return result

def rotate_x(triangle, angle):
    rotation_matrix = ((1, 0, 0), (0, math.cos(angle), -math.sin(angle)), (0, math.sin(angle), math.cos(angle)))
    return rotated(triangle, rotation_matrix)

def rotate_y(triangle, angle):
    rotation_matrix = ((math.cos(angle), 0, math.sin(angle)), (0, 1, 0), (-math.sin(angle), 0, math.cos(angle)))
    return rotated(triangle, rotation_matrix)

def rotate_z(triangle, angle):
    rotation_matrix = ((math.cos(angle), -math.sin(angle), 0), (math.sin(angle), math.cos(angle), 0), (0, 0, 1))
    return rotated(triangle, rotation_matrix)

def translated(triangle, x, y, z):
    result = []
    for point in triangle:
        result.append((point[0] + x, point[1] + y, point[2] + z))
    return result


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

def general_rotation_matrix(angle_a, angle_b, angle_c):
    rotation_matrix = [
        (math.cos(angle_a) * math.cos(angle_b),
         math.cos(angle_a) * math.sin(angle_b) * math.sin(angle_c) - math.sin(angle_a) * math.cos(angle_c),
         math.cos(angle_a) * math.sin(angle_b) * math.cos(angle_c) + math.sin(angle_a) * math.sin(angle_c)),
        (math.sin(angle_a) * math.cos(angle_b),
            math.sin(angle_a) * math.sin(angle_b) * math.sin(angle_c) + math.cos(angle_a) * math.cos(angle_c),
            math.sin(angle_a) * math.sin(angle_b) * math.cos(angle_c) - math.cos(angle_a) * math.sin(angle_c)),
        (-math.sin(angle_b), math.cos(angle_b) * math.sin(angle_c), math.cos(angle_b) * math.cos(angle_c))
    ]
    return rotation_matrix

def get_bounding_box(triangle):
    min_x = min(triangle[0][0], triangle[1][0], triangle[2][0])
    min_y = min(triangle[0][1], triangle[1][1], triangle[2][1])
    max_x = max(triangle[0][0], triangle[1][0], triangle[2][0])
    max_y = max(triangle[0][1], triangle[1][1], triangle[2][1])
    return (min_x, min_y, max_x, max_y)

count = 0

current_time = pygame.time.get_ticks()

def rotate_triangle(triangle, angle):
    angle = math.radians(angle)
    sin = math.sin(angle)
    cos = math.cos(angle)
    return [
        [x * cos - y * sin, x * sin + y * cos, z]
        for x, y, z in triangle
    ]

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

        # new_tri = rotate_triangle(tri, current_time / 3)
        # new_tri = rotate_x(tri, current_time / 10000 + tri_count)
        # new_tri = rotate_y(new_tri, current_time / 10000 * tri_count)
        # new_tri = rotate_z(new_tri, current_time / 10000 * tri_count)
        
        new_tri = rotated(tri, general_rotation_matrix(current_time / 1000,
                                                       current_time / 1000,
                                                       current_time / 1000))
        translated_tri = translated(new_tri, 250, 150, 0)
        translated_tris.append(translated_tri)


    # for i, translated_tri in enumerate(translated_tris):
        
    #     for x in range(math.floor(get_bounding_box(translated_tri)[0]), math.ceil(get_bounding_box(translated_tri)[2])):
    #         for y in range(math.floor(get_bounding_box(translated_tri)[1]), math.ceil(get_bounding_box(translated_tri)[3])):
    #             if contains(translated_tri, (x, y)):
    #                 screen.set_at((x, y), (i * 20, 255 - i * 10, i * 15))

    for i, translated_tri in enumerate(translated_tris):
        projected_tri = [project(point, size[0], size[1]) for point in translated_tri]

        for x in range(math.floor(get_bounding_box(projected_tri)[0]), math.ceil(get_bounding_box(projected_tri)[2])):
            for y in range(math.floor(get_bounding_box(projected_tri)[1]), math.ceil(get_bounding_box(projected_tri)[3])):
                if contains(projected_tri, (x, y)):
                    screen.set_at((x, y), (i * 20, 255 - i * 10, i * 15))

        

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

