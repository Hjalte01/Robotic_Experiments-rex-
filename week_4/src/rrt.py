
from grid import Grid, Cell

import numpy as np
import math
import matplotlib.pyplot as plt



class RRT(object):

    def __init__(self, grid = Grid(0.45), robot_size = 0.45):

        self.grid = grid
        self.robot_size = robot_size
        self.step_size = robot_size
        self.diag_step_size = math.sqrt(self.step_size**2 + self.step_size**2)
        self.init_cell = Cell(self.grid.grid_size/2, self.grid.grid_size/2, True)
        self.parent_cell = self.init_cell
        self.final_cell = Cell(self.grid.grid_size-2, self.grid.grid_size-2, True)
        self.rnd_cell = None
        self.random_cell()
        
        # Final route and parent list
        self.route = []
        self.parent_list = []
        self.route.append(self.init_cell)
        self.parent_list.append(0)


    def collision_check_point(self, cell):
        # check if a cell collides with grid
        return self.grid.grid[int(cell.x)][int(cell.y)].occupied
        

    def random_cell(self):
        # get a random cell
        x = np.random.randint(0, self.grid.grid_size)
        y = np.random.randint(0, self.grid.grid_size)
        self.rnd_cell = Cell(x, y)
    

    # def collision_rnd_cell(self):
    #     # check for colision from rnd_cell and a 
    #     for obstacle in self.grid.obstacles:
    #         length = np.linalg.norm(obstacle.x-self.rnd_cell.x, obstacle.y-self.rnd_cell.y)
    #         if length < self.robot_size:
    #             return False
    #     return True


    def distance_to_rnd(self, cell):
        # sort the list of cells in the following function with distance to rnd_cell
        return np.linalg.norm([cell.x - self.rnd_cell.x, cell.y - self.rnd_cell.y])
    

    def collision_check_line(self):
        # get a list of the best options to try for the new cell in path
        closest_cell = 0
        min = 2 * self.grid.grid_size ** 2
        for i in range(-1,2):
            for j in range(-1,2):
                if (i == 0 and j == 0): continue
                x_index = self.parent_cell.x + i
                y_index = self.parent_cell.y + j
                if x_index < 0 or x_index > self.grid.grid_size: continue
                if y_index < 0 or x_index > self.grid.grid_size: continue
                dist = self.distance_to_rnd(Cell(x_index, y_index))
                if (dist < min):
                    closest_cell_bool = self.collision_check_point(Cell(x_index, y_index))
                    closest_cell = Cell(x_index, y_index, closest_cell_bool)
                    min = dist
        collision_bool = self.collision_check_point(closest_cell)
        return collision_bool, closest_cell
    

    def nearest_cell(self):
        # Returns the nearest cell to the given random cell
        min_cell = 2 * self.grid.grid_size ** 2
        min_index = 0
        for index, cell in enumerate(self.route):
            length = np.linalg.norm([self.rnd_cell.x - cell.x, self.rnd_cell.y - cell.y])
            if length < min_cell:
                min_cell = length
                min_index = index
        self.parent_cell = self.route[min_index]


    def new_point_generate(self, closest_cell):
        closest_cell.parent = self.parent_cell
        closest_cell.occupied = True
        self.route.append(closest_cell)
            

    def connect_to_goal(self):
        dist = np.linalg.norm([self.parent_cell.x - self.final_cell.x, self.parent_cell.y - self.final_cell.y])
        if dist <= self.diag_step_size:
            return True
        return False

    def draw_graph(self):
        final_route = self.get_final_route()

        for i in range(self.grid.grid_size):
            for j in range(self.grid.grid_size):
                if self.grid.grid[i][j].occupied == True:
                    plt.plot(i, j, "sk", color = "red")
                else:
                    plt.plot(i, j, "ok", color = "blue")

        for i in range(int(len(final_route))-1):
            plt.plot([final_route[i][0], final_route[i+1][0]], [final_route[i][1], final_route[i+1][1]], "r")
        plt.show()

        

    def get_final_route(self):
        final_route = [[self.final_cell.x, self.final_cell.x]]
        while (self.parent_cell.parent != None):
            self.parent_cell = self.parent_cell.parent
            final_route.append([self.parent_cell.x, self.parent_cell.y])
        return final_route
    
  
    def print_route(self):
        route = self.route
        print("Route len:", len(route))
        route = list(set(route))
        print("Route len:", len(route))

    def RRT(self, iterations = 5000):
        #generate and plot circles

        for i in range(iterations):
            #check if the new vertex can connect with the final point
            #if yes, jump out of the loop
            if self.connect_to_goal() == True:
                break
            
            rrt.random_cell()
            #check for the start and end points
            while (rrt.collision_check_point(self.rnd_cell) == True):
                rrt.random_cell()
            
            self.nearest_cell()
      
            collision_bool, closest_cell = rrt.collision_check_line()

            # Check if the cloest cell is occipied
            if collision_bool == True:
                continue
            
            # Generate new vertex according to closest cell
            self.new_point_generate(closest_cell)

        print(i)
        
        
        # print(self.final_route())
        print("success!")
        print(len(self.route))
        print(self.print_route())
        print(self.draw_graph())





#--------------------------------------------------------
# run RRT example:
#--------------------------------------------------------
# set 
grid_size = 20
robot_size = 0.45

grid = Grid(robot_size, grid_size)
rrt = RRT(grid, robot_size)
rrt.RRT()




