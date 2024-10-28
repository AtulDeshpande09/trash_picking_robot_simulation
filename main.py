import pygame as pg
import random

width , height = 600,600

screen = pg.display.set_mode((width,height))
pg.display.set_caption("Simulation")

# Grid

grid_size  = 50
cols , rows = width//grid_size, height//grid_size

bot_position = [0,0]

white = (255,255,255)
black = (0,0,0)
green = (0,255,0) # when trash is picked up
red = (255,0,0) # when trash is not picked
grey = (100,100,100)
brown = (140,70,20) # for dumping zone
blue = (0,0,255)
# map creation
def create_map():
    grid = [['.' for _ in range(cols)] for _ in range(rows)]

    for _ in range(5):
        x,y = random.randint(0,cols-1) , random.randint(0,rows-1)
        
        grid[y][x] = 'T'

    grid[-1][-1] = 'D'
    return grid


# draw grid
def draw_grid(grid):

    for y in range(rows):
        for x in range(cols):
            rect = pg.Rect(x*grid_size,y*grid_size,grid_size,grid_size)
            if grid[y][x] == 'T':
                pg.draw.rect(screen,red , rect)
            elif grid[y][x] == 'D':
                pg.draw.rect(screen , brown, rect)
            elif grid[y][x]=='.':
                pg.draw.rect(screen, grey, rect , 1)
            elif grid[y][x] == 'G':
                pg.draw.rect(screen,green,rect)
            elif grid[y][x] =='n':
                pg.draw.rect(screen,blue,rect)

# Loading custom map
def load_map(filename, expected_rows=12, expected_cols=12):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            # Trim or pad each row to expected_cols length
            row = line.strip().split()
            row = row[:expected_cols] + ['.'] * (expected_cols - len(row))  # Ensure each row is exactly 12 columns
            grid.append(row)
    
    # Trim or pad the number of rows to expected_rows
    while len(grid) < expected_rows:
        grid.append(['.'] * expected_cols)  # Add empty rows if less than expected_rows
    grid = grid[:expected_rows]  # Trim extra rows

    return grid

# Moving the bot
def move_bot(direction,grid):
    global bot_position

    x,y = bot_position

    restricted_area = ['n','H']

    if direction == 'up' and y>0 and (grid[y-1][x] not in restricted_area):
        bot_position = [x,y-1]
    elif direction == 'down' and y < rows-1 and (grid[y+1][x] not in restricted_area):
        bot_position = [x,y+1]
    elif direction == 'left' and x>0 and (grid[y][x-1] not in restricted_area):
        bot_position = [x-1,y]
    elif direction == 'right' and x<cols-1 and (grid[y][x+1] not in restricted_area):
        bot_position = [x+1,y]
   
    if grid[y][x] == 'T':
        print("Trashed picked up")
        grid[y][x] = 'G'
    elif grid[y][x] == 'D':
        print("Trash dumped")

grid = create_map()
grid2 = load_map("c_map1.txt")
running = True
"""
while running:
    screen.fill(white)
    draw_grid(grid)

    bot_rect = pg.Rect(bot_position[0]*grid_size,bot_position[1]*grid_size,grid_size,grid_size)
    pg.draw.rect(screen, black, bot_rect)

    pg.display.flip()


    for event in pg.event.get():
        if event.type == pg.QUIT:
            running =False
        elif event.type == pg.KEYDOWN:

            if event.key == pg.K_UP:
                move_bot('up',grid)
            elif event.key == pg.K_DOWN:
                move_bot('down',grid)
            elif event.key == pg.K_LEFT:
                move_bot('left',grid)
            elif event.key == pg.K_RIGHT:
                move_bot('right',grid)

pg.quit()
"""
if __name__ == '__main__':
    running = True

    while running:
        screen.fill(white)
        draw_grid(grid2)  # Use the custom map grid

        bot_rect = pg.Rect(bot_position[0]*grid_size, bot_position[1]*grid_size, grid_size, grid_size)
        pg.draw.rect(screen, black, bot_rect)

        pg.display.flip()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    move_bot('up', grid2)  # Pass grid2 as the map reference
                elif event.key == pg.K_DOWN:
                    move_bot('down', grid2)
                elif event.key == pg.K_LEFT:
                    move_bot('left', grid2)
                elif event.key == pg.K_RIGHT:
                    move_bot('right', grid2)

    pg.quit()
