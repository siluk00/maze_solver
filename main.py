from window import *

def main():
    win = Window(800, 600)
    
    maze = Maze(50, 50, 10, 14, 50, 50, win, 50)
    maze.break_entrance_and_exit()
    maze.break_walls_r(0,0)
    print("FINISHED BUILDING")
    maze.reset_cells_visited()
    maze.solve()
    
    win.wait_for_close()
    

main()
