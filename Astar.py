import pygame 
import math 
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* PATH FINDING ALGORITHM")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0 , 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width      # (optional but correct)
        self.y = row * width      # (optional but correct)
        self.color = WHITE
        self.neighbors = []       # <-- use this name everywhere
        self.width = width
        self.total_rows = total_rows

    def get_pos(self): 
        return self.row, self.col 
    
    def is_closed(self):
        return self.color == RED 
    
    def is_open(self): 
        return self.color == GREEN 
    
    def is_barrier(self): 
        return self.color == BLACK 
    
    def is_start(self): 
        return self.color == ORANGE 
    
    def is_end(self): 
        return self.color == TURQUOISE  
    
    def reset(self): 
        self.color = WHITE 
    
    def make_start(self): 
        self.color = ORANGE
    
    def make_closed(self): 
        self.color = RED 
        
    def make_open(self): 
        self.color = GREEN 
        
    def make_barrier(self): 
        self.color = BLACK 
        
    def make_end(self): 
        self.color = TURQUOISE 
        
    def make_path(self): 
        self.color = PURPLE
        
    def draw(self, win): 
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
    def update_neighbor(self, grid):
        self.neighbors = []

        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
    
    def __lt__(self, other): 
        return False  
    
def h(p1, p2): 
    #manhattan distance (L distance)
    x1, y1 = p1 
    x2, y2 = p2 
    return abs(x1 - x2) + abs( y1 - y2)

def reconstruct_path(came_from, current, draw): 
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
        
def algorithm(draw, grid, start, end): 
    count = 0 
    open_set = PriorityQueue()#get min element 
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}#start at infinity     
    g_score[start] = 0 
    
    f_score = {spot: float("inf") for row in grid for spot in row}#start at infinity     
    f_score[start] = h(start.get_pos(), end.get_pos())
    
    open_set_hash = {start} 
    
    while not open_set.empty(): #run until openset is empty (no more nodes to explore)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
        
        current = open_set.get()[2] #we only want to access node 
        open_set_hash.remove(current) 
        
        if current == end: 
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True 
        
        for neighbor in current.neighbors: 
            temp_g_score = g_score[current] + 1 #distance to current node + node (one more node over)
           #temp g score represents what it would cost to reach neighbor if I go from the current node i am at 
            if temp_g_score < g_score[neighbor]: 
                #g_score[ neighbor] what is the best cost ive found so far to reach neighbor 
                #was there a better route I found? if not update neighbor node 
                #if temp g score is not as good as neighbors current cost, no need to update 
                came_from[neighbor] = current 
                #if neighbor not already in dict, add neighbor with previous node ? 
                g_score[neighbor] = temp_g_score 
                #update neighbor node 
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos()) 
                #update f_score                
                if neighbor not in open_set_hash: 
                    count += 1 
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open() 
        
        draw()
    
        if current != start: 
            current.make_closed()
    
    return False 

def make_grid(rows, width): 
    grid = []
    gap = width // rows #int division (whats the width of each cube)
    for i in range(rows): 
        grid.append([])
        for j in range(rows): 
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
            
    return grid 

def draw_grid(win, rows, width):
    gap = width // rows 
    for i in range(rows): 
        #draw horizontal line at row i
        pygame.draw.line(win, GREY, (0, i * gap), (width, i*gap))
        for j in range(rows): 
            #draw vertical line at column i 
            pygame.draw.line(win, GREY, (i*gap, 0), (i*gap, width))
        
def draw(win, grid, rows, width): 
    win.fill(WHITE)
    
    for row in grid: 
        for spot in row: 
            spot.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width): 
    gap = width // rows 
    x, y = pos 
    row = y // gap 
    col = x // gap 
    
    return row, col 

def main(win, width): 
    ROWS = 50 
    grid = make_grid(ROWS, width)
    
    start = None 
    end = None 
    
    run = True 
    started = False 
    
    while run: 
        draw(win, grid, ROWS, width)
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                run = False 
            if started: #if algorithm is started, user shouldnt be able to press or change obstacle 
                continue 
            
            if pygame.mouse.get_pressed()[0]: #LEFT click 
                pos = pygame.mouse.get_pos() 
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end: 
                    start = spot 
                    start.make_start()
                elif not end and spot != start: 
                    end = spot 
                    end.make_end()
                elif spot != end and spot != start: 
                    spot.make_barrier()
            
            elif pygame.mouse.get_pressed()[2]: #right click 
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col] 
                spot.reset()
                if spot == start: 
                    start = None 
                if spot == end: 
                    end = None 
                    
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SPACE and not started: 
                    for row in grid: 
                        for spot in row:
                            spot.update_neighbor(grid) 
                    
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    #lambda is an anon function, we can pass a function as an argument 
    pygame.quit()

main(WIN, WIDTH)
