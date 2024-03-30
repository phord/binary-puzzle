# binary-puzzle
A quick binary-puzzle solver

The rules are these:
1. The finished grid is filled with 0s and 1s.
2. The grid is square.
3. Some initial values are given in the grid.
4. Each row and each column has as many 0s as 1s.
5. There is only one valid solution.
6. No two columns are the same.
7. No two rows are the same.
8. There are at most 2 adjacent cells with the same value.

From binarypuzzle.com:
> Each cell should contain a zero or a one. No more than two similar numbers below or next to each other are allowed. Each row and each column is unique and contains as many zeros as ones.

This is just a hack to experiment with a solver for this game. There are two solver methods implemented. 

The first is
an inference solver.  It attempts to find the value of cells by inference of the rules. This solver will not completely 
solve most puzzles. But it makes progress without considering the whole board.

The second is an exhaustive solver. This turns out to be easier than it might seem since there are not many valid
row patterns in a puzzle of any given size. For example, a 14x14 puzzle has only 259 different valid patterns.

The exhaustive solver can completely solve any puzzle by itself. The inference solver can help reduce the puzzle to
something smaller for the exhaustive solver to work on.

There's almost no documentation in the code.  It's just some quick and dirty experimental code I hacked on one evening.
I did not study any prior work or better optimizations for this.  It's very possible my solution is naive or even wrong.
