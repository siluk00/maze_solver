import random
from tkinter import Tk, BOTH, Canvas
from time import sleep

class Window:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.canvas = Canvas(height = height, width = width, bg="white")
        self.canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
    
        
    
    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, color):
        line.draw(self.canvas, color)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def draw(self, canvas, color):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill = color, width = 2)

class Cell:
    def __init__(self, has_left_wall, has_right_wall, has_top_wall, has_bottom_wall, x1, y1, x2, y2, win):
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall 
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self.x1 = x1 
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.win = win
        self.visited = False

    def draw(self, color):
        left_line = Line(self.x1, self.y1, self.x1, self.y2)
        right_line = Line(self.x2, self.y1, self.x2, self.y2)
        top_line = Line(self.x1, self.y1, self.x2, self.y1)
        bottom_line = Line(self.x1, self.y2, self.x2, self.y2)
        
        if self.has_left_wall:
            left_line.draw(self.win.canvas, color)
        else:
            left_line.draw(self.win.canvas, "white")
        if self.has_right_wall:
            right_line.draw(self.win.canvas, color)
        else:
            right_line.draw(self.win.canvas, "white")
        if self.has_top_wall:
            top_line.draw(self. win.canvas, color)
        else:
            top_line.draw(self. win.canvas, "white")
        if self.has_bottom_wall:
            bottom_line.draw(self.win.canvas, color)    
        else:
            bottom_line.draw(self.win.canvas, "white")    

    def draw_move(self, cell, undo = False):
        color = "green"
        if undo:
            color = "red"

        line = Line((self.x1+self.x2)/2, (self.y1+self.y2)/2, (cell.x1 + cell.x2)/2, (cell.y1 + cell.y2)/2)
        line.draw(self.win.canvas, color)

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win, seed = None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self.cells = []
        self.create_cells()
        self.seed = random.seed(seed)

    def create_cells(self):
        for row in range(self.num_rows):
            cell = []
            x = self.x1
            y = self.y1 + row * self.cell_size_y
            y2 = y + self.cell_size_y

            for col in range(self.num_cols):
                x2 = x + self.cell_size_x
                cell.append(Cell(True, True, True, True, x, y, x2, y2, self.win))
                x += self.cell_size_x
            
            self.cells.append(cell)
       
        self.draw_cells()
        

    def draw_cells(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                self.cells[i][j].draw("black")
        self.animate()

    def animate(self):
        self.win.redraw()
        sleep(0.05)

    def break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.cells[len(self.cells)-1][len(self.cells[0])-1].has_bottom_wall= False
        self.draw_cells()

    def solve(self):
        return self.solve_r(0, 0)

    def break_walls_r(self, i, j):
        self.cells[i][j].visited = True

        while True:
            to_visit = []
            if i != 0:
                to_visit.append((self.cells[i-1][j], 't'))
            if j != 0:
                to_visit.append((self.cells[i][j-1], 'l'))
            if i != len(self.cells)-1:
                to_visit.append((self.cells[i+1][j], 'b'))
            if j != len(self.cells[0])-1:
                to_visit.append((self.cells[i][j+1], 'r'))
            
            to_visit = list(filter(lambda x: not x[0].visited, to_visit))

            if len(to_visit) == 0:
                self.draw_cells()
                return
            else:
                n = random.randrange(len(to_visit))
                if to_visit[n][1] == 'r':
                    self.cells[i][j].has_right_wall = False
                    to_visit[n][0].has_left_wall = False
                    self.break_walls_r(i, j+1)
                elif to_visit[n][1] == 'l':
                    self.cells[i][j].has_left_wall = False
                    to_visit[n][0].has_right_wall = False
                    self.break_walls_r(i, j-1)
                elif to_visit[n][1] == 'b':
                    self.cells[i][j].has_bottom_wall = False
                    to_visit[n][0].has_top_wall = False
                    self.break_walls_r(i+1, j)
                elif to_visit[n][1] == 't':
                    self.cells[i][j].has_top_wall = False
                    to_visit[n][0].has_bottom_wall = False
                    self.break_walls_r(i-1,j)

    def reset_cells_visited(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[0])):
                self.cells[i][j].visited = False

    def solve_r(self, i , j):
        self.animate()
        self.cells[i][j].visited = True
        if i == self.num_rows - 1 and j == self.num_cols -1 :
            return True
        to_visit = []
        if i != 0 and not self.cells[i][j].has_top_wall:
            to_visit.append((self.cells[i-1][j], 't'))
        if j != 0 and not self.cells[i][j].has_left_wall:
            to_visit.append((self.cells[i][j-1], 'l'))
        if i != len(self.cells)-1 and not self.cells[i][j].has_bottom_wall:
            to_visit.append((self.cells[i+1][j], 'b'))
        if j != len(self.cells[0])-1 and not self.cells[i][j].has_right_wall:
            to_visit.append((self.cells[i][j+1], 'r'))
        
        if to_visit:
            to_visit = list(filter(lambda x: not x[0].visited, to_visit))

            for cell in to_visit:
                cell[0].draw_move(self.cells[i][j])
                if cell[1]=='r':
                    if self.solve_r(i, j+1):
                        return True
                    else:
                        self.cells[i][j].draw_move(cell[0], undo= True)
                if cell[1]=='l':
                    if self.solve_r(i, j-1):
                        return True
                    else:
                        self.cells[i][j].draw_move(cell[0], undo= True)
                if cell[1]=='t':
                    if self.solve_r(i-1, j):
                        return True
                    else:
                        self.cells[i][j].draw_move(cell[0], undo= True)
                if cell[1]=='b':
                    if self.solve_r(i+1, j):
                        return True
                    else:
                        self.cells[i][j].draw_move(cell[0], undo= True)
        else:
            return False

                
                
            

            

        
