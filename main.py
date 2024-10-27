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
green = (0,255,0)
red = (255,0,0)
grey = (100,100,100)


# map creation
def create_map():
    grid = [['.' for _ in range(cols)] for _ in range(rows)]

    for _ in range(5):
        x,y = random.randint(0,cols-1) , random.randint(0,rows-1)
        
        grid[y][x] = 'trash'

    grid[-1][-1] = 'dump'
    return grid


# draw grid
def draw_grid(grid):

    for y in range(rows):
        for x in range(cols):
            rect = pg.Rect(x*grid_size,y*grid_size,grid_size,grid_size)
           if grid[y][x] == 'trash':
                pg.draw.rect(screen,green , rect)
            elif grid[y][x] == 'dump':
                pg.draw.rect(screen , red, rect)
            else:
                pg.draw.rect(screen, grey, rect , 1)


# Loading custom map
def load_custom_map(filename):
    with open(filename,'r') as file:
        for line in file:
            row = line.strip().split()
            grid.append(row)
    return grid


# Moving the bot
def move_bot(direction,grid):
    global bot_position

    x,y = bot_position

    if direction == 'up' and y>0:
        bot_position = [x,y-1]
    elif direction == 'down' and y < rows-1:
        bot_position = [x,y+1]
    elif direction == 'left' and x>0:
        bot_position = [x-1,y]
    elif direction == 'right' and x<cols-1:
        bot_position = [x+1,y]
   
    if grid[y][x] == 'trash':
        print("Trashed picked up")
        grid[y][x] = ''
    elif grid[y][x] == 'dump':
        print("Trash dumped")

grid = create_map()

running = True

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
