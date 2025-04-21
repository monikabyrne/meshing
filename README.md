# meshing/fill_gap.py description

This script calculates a sequence of element lengths to fill a gap of total length L, transitioning smoothly from an initial size > S₁ to a final size < S₂. It prioritizes geometric progression for exponential scaling and falls back to arithmetic progression for linear scaling if no valid geometric progression solution exists.

## Input
The script takes test_fill_gap.csv as input. The file contains 3 columns: S1, S2, L, Test_case

## Output
The results are written to a output.csv in the following format:  S1, S2, L, Test_case, solution_type (either geometric or arithmetic progression), solution ([r,n] for geometric progression; [d,n] for arithmetic progression), element_lengths (list of element lengths to fill gap L), message (in case of invalid input data)
