import pandas as pd
from sympy import symbols, Eq, solve
import logging
import sys


def geometric_progression(L1, L2, gap_length):
    #to do: describe input parameters
    #n - the number of elements to fill the gap
    #r - constant ratio by which the element lengths increase by
    r = symbols('r', real=True)
    n = symbols('n', integer=True)

    # defining equations
    # formula for the sum of element lengths using geometric progression
    # a1 is the first element to fill the gap
    # gap_length = a1 * (1 - r**n) / (1 - r)
    # constraint for the first element length
    # a1 = L1 * r
    eq1 = Eq(L1 * r * (1 - r**n) / (1 - r), gap_length)

    #constraint for the n+1 element length which must equal L2
    # a1 * r**n = L2
    eq2 =   Eq(L1 * r**(n+1), L2)

    solutions = solve([eq1,eq2], [r,n])

    #check for solutions where n is an integer
    valid_solutions = []
    for i in range(0,len(solutions)):
        n_solution = float(solutions[i][1]) #convert to float from sympy.core.numbers.Float
        if n_solution.is_integer():
            r_solution = float(solutions[i][0])
            n_solution = int(n_solution)
            valid_solutions.append([r_solution, n_solution])

    return valid_solutions


def arithmetic_progression(L1, L2, gap_length):
    #to do: describe input parameters
    # n - the number of elements to fill the gap
    # d - common difference by which the element lengths increase by

    # formula for the sum of element lengths using arithmetic progression
    # a1 is the first element to fill the gap; an is the last element
    # gap_length = n/2 * (a1 + an)
    # constraints for the first and last element lengths
    # a1 = L1 + d
    # an = L2 - d
    n = int(2 * gap_length / (L1 + L2)) #grab only the integer part
    # constraint for the n+1 element length
    # a1 + n * d = L2
    d = float(round((L2 - L1) / (n + 1),2))

    return [d, n]


def fill_gap(S1_length, S2_length, gap_length):

    # L1 is the shorter length of the two element lengths, L2 is longer
    error_message = ""
    L1 = 0.0
    L2 = 0.0
    if S1_length == S2_length or S1_length <= 0 or S2_length <= 0:
        error_message = ("S1 and S2 must not be equal and must be greater than 0." +
                         " Input parameters: S1=" + str(S1_length) + " S2=" + str(S2_length) + " L=" + str(gap_length))
        logging.info(error_message)
    elif S1_length < S2_length:
        L1 = S1_length
        L2 = S2_length
    elif S1_length > S2_length:
        L1 = S2_length
        L2 = S1_length

    #minimum gap length
    if not error_message:
        if gap_length <= L1 + L2:
            error_message = ("Gap length must be greater than the sum of S1 and S2." +
                       " Input parameters: S1=" + str(S1_length) + " S2=" + str(S2_length) + " L=" + str(gap_length))
            logging.info(error_message)

    #defining output parameters
    solution_type = ""
    solution = []
    gap_elements = []

    if not error_message:
        #using geometric progression first
        solutions = geometric_progression(L1,L2,gap_length)

        #if no valid solutions were found using geometric progression, use arithmetic progression
        if len(solutions) > 0:
            solution_type = "geometric progression"
            # grab one valid solution
            solution = solutions[0]
        else:
            solution_type = "arithmetic progression"
            solution = arithmetic_progression(L1,L2,gap_length)

        if solution_type == "geometric progression":
            n = solution[1]
            r = solution[0]
            for i in range(0,n):
                elem_len = float(round(L1 * r**(i+1),2))
                gap_elements.append(elem_len)
        else:
            n = solution[1]
            d = solution[0]
            for i in range(0,n):
                elem_len = float(round(L1 + (i+1) * d,2))
                gap_elements.append(elem_len)

        if S1_length > S2_length and gap_elements:
            #reverse the order of elements
            gap_elements.reverse()

    return solution_type, solution, gap_elements, error_message


def main():

    #grab lengths from a csv file and store solutions in another file
    test_file = "test_fill_gap.csv"
    logging.info(f"Trying to access file {test_file}")
    test_df = []
    try:
        test_df = pd.read_csv(test_file)
    except OSError as err:
        logging.error(f"OS Error: {err}")
        sys.exit(1)
    logging.info(f"Accessed file {test_file}")

    output_df = pd.DataFrame(columns=["S1", "S2", "L", "test_case", "solution_type", "solution", "element_lengths", "message"])
    output_file = "output.csv"

    for i in range(0,len(test_df)):
        S1_length = test_df["S1"].values[i]
        S2_length = test_df["S2"].values[i]
        gap_length = test_df["L"].values[i]
        test_case = test_df["Test_case"].values[i]
        solution_type, solution, gap_elements,message = fill_gap(S1_length, S2_length, gap_length)

        # storing the results in a csv file one row at a time in case of any unforeseen errors
        output_df.loc[0] = [S1_length, S2_length, gap_length, test_case, solution_type, str(solution), str(gap_elements), message]

        if i == 0:
            output_df.to_csv(output_file, mode='w', index=False, header=True)
        else:
            output_df.to_csv(output_file, mode='a', index=False, header=False)



if __name__ == "__main__":
    main()
