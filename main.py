import pygame
import pprint
import random


def mazeMatrix(height, width):
    matrix = []
    for i in range(height):
        row = []
        for j in range(width):
            if (i + j) % 2 == 0:
                row.append(0)
                continue
            row.append(2)

        matrix.append(row)

    return matrix


def primsAlgorithm(matrix, startPosition):
    current_cordinate = startPosition
    matrix[current_cordinate[0]][current_cordinate[1]] = 1
    walkable_paths = [current_cordinate]
    frontiers = []

    # frontiers
    frontiers += getPossibleDirections(current_cordinate, matrix)
    while len(frontiers) != 0:
        current_cordinate = random.choice(frontiers)
        matrix[current_cordinate[0]][current_cordinate[1]] = 1
        frontiers += getPossibleDirections(current_cordinate, matrix)
        frontiers.remove(current_cordinate)



def primsAlgorithmStreamer(matrix, frontiers: list):
    random_cell = random.choice(frontiers)
    #ADD UNSELECTED CELLS TO WALLS
    matrix[random_cell[0]][random_cell[1]] = 1
    #GET NEIGHBOURS OF SELECTED CELL
    temp_frontiers_of_random_cell, nearest_walked_cell = getPossibleDirections(random_cell, matrix=matrix)
    neighbours =  temp_frontiers_of_random_cell
    frontiers += neighbours
    frontiers.remove(random_cell)
    #REMOVE THE WALL
    wall_index = [(random_cell[0]+nearest_walked_cell[0])//2, (random_cell[1]+nearest_walked_cell[1]) // 2]
    matrix[wall_index[0]][wall_index[1]] =  1
    
    
 


def getPossibleDirections(current_cordinate, matrix):
    # directions
    left = [current_cordinate[0]-2, current_cordinate[1]]
    right = [current_cordinate[0]+2, current_cordinate[1]]
    top = [current_cordinate[0], current_cordinate[1]+2]
    down = [current_cordinate[0], current_cordinate[1]-2]
    possible_directions = [left, right, top, down]
    frontiers_ = []
    nearest_walked_cell = None
    for direction in possible_directions:
        try:
            x = matrix[direction[0]][direction[1]]
            # avoid wrapping back  at matrix
            # avoid adding cell already walkable to frontiers
            if -2 in direction or x==2 :
                continue
            if x == 1:
                nearest_walked_cell = direction
                continue
            frontiers_.append(direction)

        except IndexError:
            continue
    return frontiers_, nearest_walked_cell


def pygameGrid(matrix, startPosition=[0, 0], screen_height=255, screen_width=255):
    WINDOW_SIZE = [screen_height, screen_width]
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    # COLORS
    
    FRONTIER_COLOR = (0,0,255)
    CELL_COLOR = (255, 255, 255)
    CELL_COLOR_AFTER_WALK = (0, 255, 0)
    WORLD_COLOR = (0, 0 , 0)
    WALL_COLLOR = (100, 100, 100)
    draw = True
    cell_dimension = 20
    MARGIN =0
    
    # INITIALIZE START POSITION OF MATRIX
    matrix[startPosition[0]][startPosition[1]] = 1
    # walkable_paths = [current_cordinate]
    frontiers = []
    temp_frontiers ,  _ = getPossibleDirections(startPosition, matrix)
    frontiers += temp_frontiers
    finished_creating_maze = False

    while draw:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                draw = False

        screen.fill(WORLD_COLOR)
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                cell = matrix[row][col]

                temp_color = CELL_COLOR
                # cordinates to start drawing
                if cell == 1:
                    temp_color = CELL_COLOR_AFTER_WALK
                if cell == 2:
                    temp_color = WALL_COLLOR

                if [row, col] in frontiers:
                    temp_color = FRONTIER_COLOR
                
                if finished_creating_maze and cell==0:
                    temp_color = WALL_COLLOR
                left = MARGIN + col * (cell_dimension + MARGIN)
                right = MARGIN + row * (cell_dimension + MARGIN)
                # draw the cell at the coordinates  with dimenstons
                pygame.draw.rect(screen, temp_color, [
                                 (left, right), (cell_dimension, cell_dimension)])

        if len(frontiers) > 0:
           primsAlgorithmStreamer(matrix, frontiers)
        else:
            if not finished_creating_maze:
                finished_creating_maze = True

        
        clock.tick(60)
        pygame.display.flip()
        #pygame.time.wait(10)
    

matrix = mazeMatrix(20, 25)
# matrix[0][1] = 1
# primsAlgorithm(matrix = matrix, startPosition=[0,0])
screen_width = 600
screen_height = 600
pygameGrid(matrix=matrix, startPosition=[10, 10], screen_height=screen_height, screen_width=screen_width)
