import pygame, sys
from collections import deque

# initialize pygame
pygame.init()
width = 750
height = 700
screen = pygame.display.set_mode((width, height))
screen.fill((0,0,0))
clock = pygame.time.Clock()
pygame.display.set_caption('Search Algorithm Visualizer')
small_font = pygame.font.SysFont('Times New Roman', 15)

# takes care of each individual node
cols, rows = 50, 40
node_height = (height-100)//rows
node_width = width//cols

queue = deque()
stack = []
grid = []
final_path = []
start_coords = ()
end_coords = ()


class Node:
    def __init__(self, x, y):
        self.y_pos = y
        self.x_pos = x
        self.neighbors = []
        self.color = (255, 255, 255)
        self.visited = False
        self.is_wall = False
        self.is_end = False
        self.is_start = False
        self.previous = None

    def draw(self, screen):
        if self.is_wall == True:
            self.color = (0,0,0)
        elif self in final_path and self.is_start == False and self.is_end == False:
            #nodes in the final path are green
            self.color = (0, 255, 0)
        elif self.visited and self.is_start == False and self.is_end == False:
            # visited nodes are red
            self.color = (255, 0, 0)
        elif (self in queue or self in stack) and self.is_start == False and self.is_end == False:
            # queued nodes are yellow
            print("yes")
            self.color = (255, 255, 51)
        elif self.is_end:
            # final node is purple
            self.color = (127, 0, 255)
        elif self.is_start:
            # start node is blue
            self.color = (0, 128, 255)
        else:
            self.color = (255, 255, 255)
        pygame.draw.rect(screen, self.color, (self.x_pos*node_width, self.y_pos*node_height, node_height-1, node_width-1))

    def find_neighbors(self, grid):
        #adding right neighbor
        if (self.x_pos + 1) < cols:
            self.neighbors.append(grid[self.x_pos+1][self.y_pos])
        #adding left neighbor
        if (self.x_pos - 1) >= 0:
            self.neighbors.append(grid[self.x_pos-1][self.y_pos])
        #adding top neighbor
        if (self.y_pos + 1) < rows:
            self.neighbors.append(grid[self.x_pos][self.y_pos+1])
        #adding bottom neighbor
        if (self.y_pos - 1) >= 0:
            self.neighbors.append(grid[self.x_pos][self.y_pos-1])

def select_start(screen, grid, queue):
    
    start_selected = False
    while not start_selected:
        for event in pygame.event.get():
            pygame.draw.rect(screen, (255, 255, 255), (25, 625, 75, 50))
            screen.blit(small_font.render("Start Node", True, (0,0,0)), (30, 643))
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # clear queue and stack before
                queue.clear()
                stack.clear()
                pos = pygame.mouse.get_pos()
                if pos[1] < 600:
                    x = pos[0] // node_width
                    y = pos[1] // node_height
                    grid[x][y].is_start = True
                    grid[x][y].visited = True
                    # resets previous start node
                    for i in range(cols):
                        for j in range(rows):
                            if not i == x and not j == y:
                                grid[i][j].is_start = False
                                grid[i][j].visited = False
                    start_selected = True
                    queue.append(grid[x][y])
                    stack.append(grid[x][y])
                    print(queue)
                    return x,y
                else:
                    continue
                    
    return

def select_end(screen, grid):
    end_selected = False
    while not end_selected:
        for event in pygame.event.get():
            pygame.draw.rect(screen, (255, 255, 255), (125, 625, 75, 50))
            screen.blit(small_font.render("End Node", True, (0,0,0)), (132, 643))
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                if pos[1] < 600:
                    x = pos[0] // node_width
                    y = pos[1] // node_height
                    grid[x][y].is_end = True
                    # resets previous end node
                    for i in range(cols):
                        for j in range(rows):
                            if not i == x and not j == y:
                                grid[i][j].is_end = False
                    end_selected = True
                    return x,y
                else:
                    continue
                    
    return

def clear(screen, grid):
    for x in range(cols):
        for y in range(rows):
            grid[x][y].visited = False
            grid[x][y].is_wall = False
            grid[x][y].is_end = False
            grid[x][y].is_start = False
            grid[x][y].previous = None
    final_path.clear()
    queue.clear()
    stack.clear()
    return

def main():
    bfs_started = False
    dfs_started = False
    ended = False
    dfs_ended = False
    #initialize grid
    for i in range(cols):
        curr_col = []
        for j in range(rows):
            curr_col.append(Node(i,j))
        grid.append(curr_col)
    # find neighbors for each node
    for i in range(cols):
        for j in range(rows):
            grid[i][j].find_neighbors(grid)
    # pick a start and end node
    # add wall nodes
    # add start node to queue, mark as visited
    while True:
        for event in pygame.event.get():
            ###--------- BUTTONS -----------
            # create button for selecting start node
            start_button = small_font.render("Start Node", True, (0,0,0))
            mouse_pos = pygame.mouse.get_pos()
            if 25 <= mouse_pos[0] <= 100 and 625 <= mouse_pos[1] <= 675:
                #light color
                pygame.draw.rect(screen, (255, 255, 255), (25, 625, 75, 50))
            else:
                pygame.draw.rect(screen, (192, 192, 192), (25, 625, 75, 50))
            screen.blit(start_button, (30, 643))
            #pygame.display.update()
            
            # create button for selecting end node
            end_button = small_font.render("End Node", True, (0,0,0))
            mouse_pos = pygame.mouse.get_pos()
            if 125 <= mouse_pos[0] <= 200 and 625 <= mouse_pos[1] <= 675:
                #light color
                pygame.draw.rect(screen, (255, 255, 255), (125, 625, 75, 50))
            else:
                pygame.draw.rect(screen, (192, 192, 192), (125, 625, 75, 50))
            screen.blit(end_button, (132, 643))

            # create bfs button
            bfs_button = small_font.render("Breadth First Search", True, (0,0,0))
            mouse_pos = pygame.mouse.get_pos()
            if 225 <= mouse_pos[0] <= 400 and 625 <= mouse_pos[1] <= 675:
                #light color
                pygame.draw.rect(screen, (255, 255, 255), (225, 625, 175, 50))
            else:
                pygame.draw.rect(screen, (192, 192, 192), (225, 625, 175, 50))
            screen.blit(bfs_button, (250, 643))

            # create dfs button
            dfs_button = small_font.render("Depth First Search", True, (0,0,0))
            mouse_pos = pygame.mouse.get_pos()
            if 425 <= mouse_pos[0] <= 600 and 625 <= mouse_pos[1] <= 675:
                #light color
                pygame.draw.rect(screen, (255, 255, 255), (425, 625, 175, 50))
            else:
                pygame.draw.rect(screen, (192, 192, 192), (425, 625, 175, 50))
            screen.blit(dfs_button, (455, 643))

            # create clear button
            clear_button = small_font.render("Clear Board", True, (0,0,0))
            mouse_pos = pygame.mouse.get_pos()
            if 625 <= mouse_pos[0] <= 725 and 625 <= mouse_pos[1] <= 675:
                #light color
                pygame.draw.rect(screen, (255, 255, 255), (625, 625, 100, 50))
            else:
                pygame.draw.rect(screen, (192, 192, 192), (625, 625, 100, 50))
            screen.blit(clear_button, (638, 643))

            ###----------- ACTIONS --------------
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                # start node button clicked
                if 25 <= pos[0] <= 100 and 625 <= pos[1] <= 675:
                    start_coords = select_start(screen, grid, queue)
                    print("queue is " + str(len(queue)))
                # end node button clicked
                if 125 <= pos[0] <= 200 and 625 <= pos[1] <= 675:
                    end_coords = select_end(screen, grid)
                # clear board button clicked
                if 625 <= pos[0] <= 725 and 625 <= pos[1] <= 675:
                    ended = False
                    dfs_ended = False
                    clear(screen, grid)
                # bfs button clicked
                if 225 <= pos[0] <= 400 and 625 <= pos[1] <= 675:
                    if (end_coords == ()):
                        continue
                    else:
                        bfs_started = True
                # dfs button clicked
                if 425 <= pos[0] <= 600 and 625 <= pos[1] <= 675:
                    if (end_coords == ()):
                        continue
                    else:
                        dfs_started = True
            # puts wall nodes down
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    if pos[1] < 600:
                        x = pos[0] // node_width
                        y = pos[1] // node_height
                        if not grid[x][y].is_start and not grid[x][y].is_end:
                            grid[x][y].is_wall = True

            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        ##-----ALGORITHMS------
        if bfs_started:
            print(len(queue))
            if len(queue) > 0:
                curr = queue.popleft()
                print(curr)
                print(ended)
                # check if the current node is the end node
                if curr == grid[end_coords[0]][end_coords[1]]:
                    temp = curr
                    while temp.previous:
                        final_path.append(temp.previous)
                        temp = temp.previous
                        # how to end this ?
                    if not ended:
                        ended = True
                        print("Done")
                    elif ended:
                        continue
                if ended == False:
                    for neighbor in curr.neighbors:
                        if not neighbor.visited and not neighbor.is_wall:
                            neighbor.previous = curr
                            neighbor.visited = True
                            queue.append(neighbor)
            else:
                if ended:
                    bfs_started = False
                    continue
                else:
                    print("No solution")
                    bfs_started = False
                    
        if dfs_started:
            if len(stack) > 0:
                curr = stack.pop()
                # check if the current node is the end node
                if curr == grid[end_coords[0]][end_coords[1]]:
                    temp = curr
                    while temp.previous:
                        final_path.append(temp.previous)
                        temp = temp.previous
                        # how to end this ?
                    if not dfs_ended:
                        dfs_ended = True
                        print("Done")
                    elif dfs_ended:
                        continue
                if dfs_ended == False:
                    for neighbor in curr.neighbors:
                        if not neighbor.visited and not neighbor.is_wall:
                            neighbor.previous = curr
                            neighbor.visited = True
                            stack.append(neighbor)
            else:
                if dfs_ended:
                    dfs_started = False
                    continue
                else:
                    print("No solution")
                    dfs_started = False

        #----PRINTING-----
        for i in range(cols):
            for j in range(rows):
                curr_node = grid[i][j]
                if (curr_node in queue or curr_node in stack) and curr_node.is_start == False and curr_node.is_end == False:
                    curr_node.color = (255, 255, 51)
                    pygame.draw.rect(screen, curr_node.color, (curr_node.x_pos*node_width, curr_node.y_pos*node_height, node_height-1, node_width-1))
                else:
                    curr_node.draw(screen)
        
        pygame.display.flip()
        # clock.tick(30)
main()