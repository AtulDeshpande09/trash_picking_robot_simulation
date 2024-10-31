import pygame as pg
from bfs import bfs

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

#grid = create_map()
grid = load_map("c_map1.txt")

# trash cordinates
trash_list = [(x, y) for y in range(len(grid)) for x in range(len(grid[0])) if grid[y][x] == 'T']

# how many trash are there
total_trash:int = len(trash_list)

# Define start and goal positions
start_position = (0, 0)
dump_position = (11,11)  # Coordinates of the trash or dump





if __name__ == '__main__':

    # this function will take bot to trash location
    # since we know there are "total_trash" numbers of trash we can iterate a loop
    current_position = start_position
    print("No of trash : ",total_trash)
    
    while total_trash > 0:

        print("No of trash in the : ",total_trash)

        #find nearest trash here
        nearest_trash = min(trash_list, key=lambda t: abs(bot_position[0] - t[0]) + abs(bot_position[1] - t[1]))

        # bfs function
        path = bfs(grid, current_position, nearest_trash)
        if path:
            for step in path:
                bot_position = step
                print(f"Bot moved to {step}")
                screen.fill(white)
                draw_grid(grid) 
                bot_rect = pg.Rect(bot_position[0]*grid_size,bot_position[1]*grid_size,grid_size,grid_size)
                pg.draw.rect(screen,black,bot_rect)
                pg.display.flip()
                pg.time.delay(300)

        # decrease one trash
        # remove picked up trash from trash_list :list
        total_trash -= 1
        trash_list.remove(nearest_trash)

        #mark trash as G - trash is picked
        grid[nearest_trash[1]][nearest_trash[0]] = 'G'
        
        # current position of bot
        current_position = bot_position


    # for dumping
    path = bfs(grid, current_position, dump_position)

    print("No of trash out of the loop : ",total_trash)

    if path:
        for step in path:
            bot_position = step
            print(f"Bot moved to {step}")
            screen.fill(white)
            draw_grid(grid) 
            bot_rect = pg.Rect(bot_position[0]*grid_size,bot_position[1]*grid_size,grid_size,grid_size)
            pg.draw.rect(screen,black,bot_rect)
            pg.display.flip()
            pg.time.delay(300)
    if input("enter q to quit :")=='q':
        pg.quit()



