import numpy as np
import threading
from processing_py import App


class Sudoku():
    """
    This will be a class of helper functions for the manipulation of a grid with
    Sudoku like properties
    """

    def get_row(grid, i):
        return grid[i-1, :].copy()

    def get_col(grid, j):
        return grid[:, j-1].copy()

    def get_box_from_box_coord(grid, coord):
        row_range = [(coord[0]-1)*3, (coord[0])*3]
        col_range = [(coord[1]-1)*3, (coord[1])*3]
        box = grid[row_range[0]: row_range[1],
                   col_range[0]: col_range[1]]
        return box.flatten().copy()

    def get_box(grid, coord):
        box_coord = ((coord[0]+2)//3, (coord[1]+2)//3)
        return Sudoku.get_box_from_box_coord(grid, box_coord)

    def check_valid_grid(grid):
        for n in range(1, 10):
            # check if each number in [1,2,3,4,5,6,7,8,9] appears at most once
            # in each row,
            if np.max(np.count_nonzero(grid == n, axis=1)) > 1:
                return False
            # each column
            if np.max(np.count_nonzero(grid == n, axis=0)) > 1:
                return False
            # and each box
            for i in [1, 2, 3]:
                for j in [1, 2, 3]:
                    box = Sudoku.get_box_from_box_coord(grid, (i, j))
                    if np.count_nonzero(box == n) > 1:
                        return False
        return True

    def get_grid_options(grid, coord):
        options = set(range(1, 10))
        options.difference_update(Sudoku.get_row(grid, coord[0]))
        options.difference_update(Sudoku.get_col(grid, coord[1]))
        if len(options) == 0:
            # Possible early return to skip box check
            return options
        options.difference_update(Sudoku.get_box(grid, coord))
        return options

    def get_empty_squares(grid):
        return np.argwhere(grid == 0) + 1

    def print(grid):
        print(Sudoku.string(grid))

    def string(grid):
        lines = []
        for i in range(9):
            if i in [3, 6]:
                lines.append("-------+-------+-------")
            # print row
            lines.append((" {} {} {} | {} {} "
                          "{} | {} {} {} ").format(*list(grid[i, :])))
        return "\n".join(lines).replace("0", "*")


class SudokuSolver:
    def __init__(self, grid, step_by_step=False, draw=False):
        self.grid = grid
        if step_by_step:
            self.draw = draw
            if draw:
                self._lock = threading.Lock()
                # setup draw thread
                thread = threading.Thread(target=self.draw_step)
                # thread.daemon = False
                thread.start()
            self.queue = []
            self.queue.append([self.grid, None])
            self.solution, _ = self.step_solve_sudoku(self.grid)
            self.queue.append([self.solution, None])
        else:
            self.solution, _ = self.solve_sudoku(self.grid)

    def solve_sudoku(self, grid, depth=0):
        # find all empty empty squares
        empty_squares = Sudoku.get_empty_squares(grid)
        # If there are no empty squares, then the Sudoku is solved
        # return (Sudoku, True)
        if empty_squares.shape[0] == 0:
            return (grid, True)
        # Else, find the empty square with the smallest +ve number of
        # possible values
        else:
            min_len_pos_vals = None
            min_pos_vals = None
            min_coord = [None, None]
            for coord in empty_squares:
                coord = list(coord)
                pos_vals = Sudoku.get_grid_options(grid, coord)
                len_pos_vals = len(pos_vals)
                if len_pos_vals == 0:
                    # If there exits a square with no possibilities return
                    # (None, False)
                    return (None, False)
                elif len_pos_vals > 0 and ((min_len_pos_vals is None) or
                                           (len_pos_vals < min_len_pos_vals)):
                    min_len_pos_vals = len_pos_vals
                    min_pos_vals = pos_vals
                    min_coord = coord
                    # break
                if len_pos_vals == 1:
                    # Can end search early if a square with
                    # 1 possible value is found
                    break
        # If all squares have no possible values, then return (None, False)
        # if min_len_pos_vals is None:
        #     return (None, False)
        # for each of the possible values, put the possible value in the square
        for value in min_pos_vals:
            new_grid = grid.copy()
            new_grid[min_coord[0]-1, min_coord[1]-1] = value
            # solve the sudoku for new grid
            result, done = self.solve_sudoku(new_grid, depth=depth+1)
            # If the returned value is (Sudoku, True), return (Sudoku, True)
            if done:
                return (result, True)
        # If out of the loop and find no solution, return (None, False)
        return (None, False)

    def step_solve_sudoku(self, grid, depth=0):
        # find all empty empty squares
        empty_squares = Sudoku.get_empty_squares(grid)
        # If there are no empty squares, then the Sudoku is solved
        # return (Sudoku, True)
        if empty_squares.shape[0] == 0:
            return (grid, True)
        # Else, find the empty square with the smallest +ve number of
        # possible values
        else:
            min_len_pos_vals = None
            min_pos_vals = None
            min_coord = [None, None]
            for coord in empty_squares:
                coord = list(coord)
                pos_vals = Sudoku.get_grid_options(grid, coord)
                len_pos_vals = len(pos_vals)
                if len_pos_vals == 0:
                    # If there exits a square with no possibilities return
                    # (None, False)
                    return (None, False)
                elif len_pos_vals > 0 and ((min_len_pos_vals is None) or
                                           (len_pos_vals < min_len_pos_vals)):
                    min_len_pos_vals = len_pos_vals
                    min_pos_vals = pos_vals
                    min_coord = coord
                    # break
                if len_pos_vals == 1:
                    # Can end search early if a square with
                    # 1 possible value is found
                    break
        # If all squares have no possible values, then return (None, False)
        # if min_len_pos_vals is None:
        #     return (None, False)
        # for each of the possible values, put the possible value in the square
        for value in min_pos_vals:
            new_grid = grid.copy()
            new_grid[min_coord[0]-1, min_coord[1]-1] = value
            # Append new grid to queue, as well as value inputted
            if self.draw:
                with self._lock:
                    self.queue.append([new_grid, min_coord])
            else:
                self.queue.append([new_grid, min_coord])
            # solve the sudoku for new grid
            result, done = self.step_solve_sudoku(new_grid, depth=depth+1)
            # If the returned value is (Sudoku, True), return (Sudoku, True)
            if done:
                return (result, True)
        # If out of the loop and find no solution, return (None, False)
        return (None, False)

    def draw_step(self):
        # last_time = time.time()
        app = App(600, 600)
        lb = 50
        ub = 550
        # tstep = 0.00
        itv = (ub-lb)/9
        while True:
            try:
                with self._lock:
                    q = self.queue
                if (len(q) > 0):
                    # last_time = time.time()

                    # print(len(q))
                    result = q.pop(0)
                    grid = result[0]
                    iteration = result[1]

                    # Draw background
                    app.background(255, 255, 255)

                    # Highlight the current iteration square
                    if iteration is not None:
                        x = lb + (iteration[1]-1) * itv
                        y = lb + (iteration[0]-1) * itv
                        app.fill(255, 128, 0)
                        app.strokeWeight(0)
                        app.rect(x, y, itv, itv)

                    # Draw the Grid
                    app.fill(0, 0, 0)
                    for i in range(9 + 1):
                        m = lb + itv * i
                        if i % 3 == 0:
                            # draw bold lines
                            app.strokeWeight(3)
                        else:
                            # draw thin lines
                            app.strokeWeight(1)
                        app.line(lb, m, ub, m)
                        app.line(m, lb, m, ub)

                    # Draw the numbers
                    app.fill(0, 0, 0)
                    app.textAlign("CENTER,CENTER")
                    app.textSize(24)
                    for i in range(9):
                        for j in range(9):
                            if grid[i, j] == 0:
                                continue
                            else:
                                if iteration is None:
                                    app.fill(0, 0, 0)
                                elif self.grid[i, j] != 0:
                                    app.fill(0, 0, 0)
                                else:
                                    app.fill(255, 0, 0)
                                n = str(grid[i, j])
                                x = lb + j * itv
                                y = lb + i * itv
                                app.sendLine((f"text('{n}', {x}, {y},"
                                              f" {itv}, {itv})"))

                    # Draw it all to surface
                    app.redraw()
            except KeyboardInterrupt:
                break


def main1(difficulty, n, random=True):
    with open(f"{difficulty}.txt", "r") as file:
        puzzles = file.readlines()
    if random:
        try:  # random puzzles
            puzzles = np.random.choice(puzzles, n, replace=False)
        except ValueError:
            print("n greater than the number of puzzles so all puzzles used")
    else:
        try:  # deterministic puzzles
            puzzles = [puzzles[i] for i in range(n)]
        except IndexError:
            print("n greater than the number of puzzles so all puzzles used")
    for num, puzzle in enumerate(puzzles):
        grid = [int(char) for char in puzzle.strip()]
        grid = np.array(grid).reshape((9, 9))
        print(f"Puzzle {num + 1}")
        Sudoku.print(grid)
        result = SudokuSolver(grid, step_by_step=True).solution
        print(len(SudokuSolver(grid, step_by_step=True).queue))
        print()
        Sudoku.print(result)


def main2(grid):
    x = SudokuSolver(grid, step_by_step=True, draw=True)
    # x = SudokuSolver(grid)
    Sudoku.print(x.solution)


if __name__ == '__main__':
    grid = np.array([[0, 9, 0, 1, 6, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 4, 0, 5, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 7, 0, 2, 8, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 3, 4, 0],
                     [0, 0, 0, 0, 7, 0, 0, 0, 5],
                     [0, 0, 0, 9, 0, 0, 1, 0, 0],
                     [5, 0, 4, 0, 0, 0, 0, 0, 0],
                     [8, 0, 0, 0, 0, 0, 0, 0, 0]])  # 17 Clue Sudoku
    # grid = np.array([[0, 2, 0, 0, 0, 0, 0, 0, 0],
    #                  [0, 0, 0, 6, 0, 0, 0, 0, 3],
    #                  [0, 7, 4, 0, 8, 0, 0, 0, 0],
    #                  [0, 0, 0, 0, 0, 3, 0, 0, 2],
    #                  [0, 8, 0, 0, 4, 0, 0, 1, 0],
    #                  [6, 0, 0, 5, 0, 0, 0, 0, 0],
    #                  [0, 0, 0, 0, 1, 0, 7, 8, 0],
    #                  [5, 0, 0, 0, 0, 9, 0, 0, 0],
    #                  [0, 0, 0, 0, 0, 0, 0, 4, 0]])  # 19 Clue Sudoku
    # grid = np.array([[8, 0, 0, 0, 0, 0, 0, 0, 0],
    #                  [0, 0, 3, 6, 0, 0, 0, 0, 0],
    #                  [0, 7, 0, 0, 9, 0, 2, 0, 0],
    #                  [0, 5, 0, 0, 0, 7, 0, 0, 0],
    #                  [0, 0, 0, 0, 4, 5, 7, 0, 0],
    #                  [0, 0, 0, 1, 0, 0, 0, 3, 0],
    #                  [0, 0, 1, 0, 0, 0, 0, 6, 8],
    #                  [0, 0, 8, 5, 0, 0, 0, 1, 0],
    #                  [0, 9, 0, 0, 0, 0, 4, 0, 0]])  # Hardest Sudoku
    # grid = np.array([[5, 3, 0, 0, 7, 0, 0, 0, 0],
    #                  [6, 0, 0, 1, 9, 5, 0, 0, 0],
    #                  [0, 9, 8, 0, 0, 0, 0, 6, 0],
    #                  [8, 0, 0, 0, 6, 0, 0, 0, 3],
    #                  [4, 0, 0, 8, 0, 3, 0, 0, 1],
    #                  [7, 0, 0, 0, 2, 0, 0, 0, 6],
    #                  [0, 6, 0, 0, 0, 0, 2, 8, 0],
    #                  [0, 0, 0, 4, 1, 9, 0, 0, 5],
    #                  [0, 0, 0, 0, 8, 0, 0, 7, 9]])  # Easy Sudoku
    import cProfile
    import pstats
    import io
    from pstats import SortKey

    difficulty = "easiest"
    n = 1000

    pr = cProfile.Profile()
    pr.enable()
    # result, _ = solve_sudoku(grid)
    # main1(difficulty, n, random=False)
    main2(grid)
    pr.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats("sudoku.py")
    print(s.getvalue())
