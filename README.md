# DPLL
The DPLL algorithm optimizes the process of solving Boolean Satisfiability (SAT) problems by using:

- Backtracking search: The algorithm recursively tries different truth assignments and backtracks if a conflict is found.

- Unit Clause Heuristic: If a clause has only one literal, that literal must be true.

- Pure Literal Heuristic: If a literal appears only in one polarity (positive or negative), it can be assigned a truth value that satisfies all clauses where it appears.

# How to Run the Program 

Running the Program Directly: To run the program manually (outside of the autochecker), you can use the sat executable:

    //Basic Usage:
        ./sat < input-file.txt

   //Disable Unit Clause Heuristic:
        ./sat --nounit < input-file.txt

    //Disable Pure Literal Heuristic:
        ./sat --nopure < input-file.txt

    //Enable Debugging:
        ./sat --debug < input-file.txt

    //Combining Options (e.g., disabling both heuristics and enabling debugging):
        ./sat --nounit --nopure --debug < input-file.txt


Running with the Autochecker: The provided checker.py script will run the program on a set of test cases. You can run it in two modes:

   // With Heuristics Enabled (faster):
        ./checker.py hw3

    // With Heuristics Disabled (may take longer):
        ./checker.py hw3 none

# Command-Line Options 
--nounit: Disables the unit clause heuristic, which means unit clauses will not be automatically assigned truth values.<br>
--nopure: Disables the pure literal heuristic, so pure literals won’t be assigned truth values based on polarity.<br>
--debug: Enables debug mode, which prints detailed information about the solving process (e.g., current assignments, clause simplifications).

# Expected Outputs 
    sat-problem1.txt - Expected output: satisfiable
    sat-problem2.txt - Expected output: unsatisfiable
    sat-problem3.txt - Expected output: satisfiable
    sat-problem4.txt - Expected output: satisfiable
    sat-problem5.txt - Expected output: unsatisfiable
    sat-problem6.txt - Expected output: unsatisfiable
    sat-problem7.txt - Expected output: satisfiable

# References 

DPLL Algorithm: 
The Davis-Putnam-Logemann-Loveland (DPLL) algorithm was first introduced in a 1960 paper on decision procedures for logical formulas in propositional logic. It's an extension of the original Davis-Putnam algorithm.

Python Typing and Libraries: 
The typing module from Python’s standard library is used to provide type hints for better readability and maintainability.

Command-line Option Parsing: 
The program uses basic command-line option parsing to enable or disable heuristics and enable debugging.


