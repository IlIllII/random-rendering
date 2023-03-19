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
    a = triangle[0][:-1]
    b = triangle[1][:-1]
    c = triangle[2][:-1]
    if same_side(point, a, b, c) and same_side(point, b, a, c) and same_side(point, c, a, b):
        return True
    return False

def matrix_mult(matrix, vector):
    result = []
    for row in matrix:
        result.append(dot_product(row, vector))
    return result



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



tri3D_3_model = ((-50, -50, 0), (50, -50, 0), (50, 50, 0))
tri3D_3_model2 = ((50, 50, 0), (-50, 50, 0), (-50, -50, 0))

pygame.init()


size = (700, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")


done = False


clock = pygame.time.Clock()

tri1 = [(100, 100), (200, 100), (150, 200)]
tri2 = [(300, 100), (400, 100), (350, 200)]

tri1_3d = [(100, 100, 0), (200, 100, 0), (150, 200, 0)]
tri2_3d = [(300, 100, 0), (400, 100, 0), (350, 200, 0)]

def get_bounding_box(triangle):
    min_x = min(triangle[0][0], triangle[1][0], triangle[2][0])
    min_y = min(triangle[0][1], triangle[1][1], triangle[2][1])
    max_x = max(triangle[0][0], triangle[1][0], triangle[2][0])
    max_y = max(triangle[0][1], triangle[1][1], triangle[2][1])
    return (min_x, min_y, max_x, max_y)

count = 0

current_time = pygame.time.get_ticks()

while not done:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    count += 1

    tri3D_3_model2

    tri3D_3 = rotate_x(tri3D_3_model, current_time / 1000)
    tri3D_3 = rotate_z(tri3D_3, current_time / 2000)
    tri3D_3 = rotate_y(tri3D_3, current_time / 3000)
    translated_tri = translated(tri3D_3, 20, 20, 0)
    translated_tri = rotate_z(translated_tri, current_time / 2000)
    translated_tri = translated(translated_tri, 250, 150, 0)

    tri3D_32 = rotate_x(tri3D_3_model2, current_time / 1000)
    tri3D_32 = rotate_z(tri3D_32, current_time / 2000)
    tri3D_32 = rotate_y(tri3D_32, current_time / 3000)
    translated_tri2 = translated(tri3D_32, 20, 20, 0)
    translated_tri2 = rotate_z(translated_tri2, current_time / 2000)
    translated_tri2 = translated(translated_tri2, 250, 150, 0)

    screen.fill((255, 255, 255))

    for x in range(math.floor(get_bounding_box(translated_tri)[0]), math.ceil(get_bounding_box(translated_tri)[2])):
        for y in range(math.floor(get_bounding_box(translated_tri)[1]), math.ceil(get_bounding_box(translated_tri)[3])):
            if contains(translated_tri, (x, y)):
                screen.set_at((x, y), (0, 0, 0))
    for x in range(int(get_bounding_box(translated_tri2)[0]), int(get_bounding_box(translated_tri2)[2])):
        for y in range(int(get_bounding_box(translated_tri2)[1]), int(get_bounding_box(translated_tri2)[3])):
            if contains(translated_tri2, (x, y)):
                screen.set_at((x, y), (0, 150, 100))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

