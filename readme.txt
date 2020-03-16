solve.py: My solution
sudoku.py: Peter Norvig's solution
sudoku3.py: Peter Norvig' solution(python3)

Review other solution of sudoku(https://norvig.com/sudoku.html)
I saw solution by Peter Norvig and converted the soultion to python 3.
The solution is great!. But it assume that the problem is falutless.
If the problem has more than one answer, the solution program output only first answer(Sudoku problem must have only one answer).
For example, look at following example.
This problem is fault because it has two answer(X = 3, Y = 9 or X = 9, Y = 3).
========================================
239 146 587
617 852 934
584 XY7 126

726 YX8 415
345 671 892
198 425 673

461 283 759
953 714 268
872 569 341
========================================
The solution by Peter Norvig output only X = 3, Y = 9.

I decided that I would code the solution of sudoku that it can detect problem's fault.
My program find an answer and verify that the answer is unique.
Therefore it can detect whether the problem is faultless or not.

I like to solve puzzles and find a way to solve it more easily. To find an easy way, I had solved so many problems.
For sudoku, such a way does not exist. But I can demonstrate flowings.
1. Find number that must be correct in a cell - find an answer of a cell.
2. Find number that must be incorrect in a cell - remove a candidate of a cell.
Using these two way, you can solve all sudoku problems.

Sudoku 10000 by 1gravity LLC has many problems according to the difficulty.
The difficulty level is eight - very easy, easy, moderate, advanced, hard, very hard, fiendish, nightmare.
Sudoku 10000 provide hint functionalty and all the algorithms of hint is either way 1 or way 2 in a nutshell.
This hint include BUG and I can find out sudoku problem's fault.

The algorithm to solve sudoku problem is followings
★ Full House
★ Hidden Single
★ Hidden Subset (Pair, Triple + Quad)
★ Naked Single
★ Naked Subset (Pair, Triple + Quad)
★ Locked Candidates (Pointing + Claiming)
★ X-Wing (Regular, Finned + Sashimi)
★ Swordfish (Regular, Finned + Sashimi)
★ Jellyfish (Regular, Finned + Sashimi)
★ XY-, XYZ-, WXYZ-, VWXYZ-, UVWXYZ-, TUVWXYZ-, STUVWXYZ-, RSTUVWXYZ-Wing
★ W-Wing
★ Almost Locked Candidates (Pair, Triple + Quad)
★ Avoidable Rectangle (type 1 + 2)
★ Hidden Unique Rectangle
★ Uniqueness Test (type 1, 2, 3, 4 + 5)
★ BUG+1, BUG+2, BUG+3 and BUG+4
★ Aligned Pair + Triple Exclusion
★ Sue de Coq
★ ALS-XZ, ALS-XY-Wing
★ Remote Pairs
★ Bidirectional Cycles
★ Forcing X-Chains
★ Forcing XY-Chains
★ Nishio Forcing Chains
★ Double Forcing Chains
★ Contradiction Forcing Chains
★ Region Forcing Chains
★ Cell Forcing Chains
