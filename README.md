# Sudoku-Solver

## How to install

1. Download the repository
2. Install Python version 3.8 available [here](https://www.python.org/downloads/release/python-385/)
3. Go to the directory where `sudoku.py` is located
4. Unzip all of the `.zip` files
5. Run `pip install -r requirements.txt`

You can now use `sudoku.py` within your project.

## How to use`sudoku.py`

First note that grids in `sudoku.py` are treated as numpy arrays of shape (9, 9), e.g.
```
grid = np.array([[0, 9, 0, 1, 6, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 4, 0, 5, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 7, 0, 2, 8, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 3, 4, 0],
                 [0, 0, 0, 0, 7, 0, 0, 0, 5],
                 [0, 0, 0, 9, 0, 0, 1, 0, 0],
                 [5, 0, 4, 0, 0, 0, 0, 0, 0],
                 [8, 0, 0, 0, 0, 0, 0, 0, 0]])
```
where a `0` represents an empty cell.

To simply get the solution you can do the following
```
from sudoku import SudokuSolver
data = SudokuSolver(grid)
solu = data.solution
```
`sudoku.py` also provides the option to see step-by-step how the algorithm goes about solving the problem, to see this you can alter the above to be
```
from sudoku import SudokuSolver
data = SudokuSolver(grid, step_by_step=True, draw=True)
```
(Note that if you don't care to see it drawn step-by-step, you can leave out the argument `draw=True`, and simply see all the steps taken in `data.queue`)
