#!/usr/bin/env python3
import sys
from typing import List, Tuple, Dict, Optional


def parse_input() -> Tuple[List[List[Tuple[str, str]]], List[str]]:
    """Parse the input clauses in CNF form and extract atoms."""
    clauses, atoms = [], set()
    for line in sys.stdin:
        line = line.strip()
        if line:
            clause = [(literal[0], literal[1:]) if literal.startswith('~') else ('', literal)
                      for literal in line.split(',')]
            clauses.append(clause)
            atoms.update(atom for _, atom in clause)
    return clauses, sorted(atoms)


def is_clause_satisfied(clause: List[Tuple[str, str]], assignment: Dict[str, bool]) -> bool:
    """Check if a clause is satisfied under a given assignment."""
    return any(not assignment[atom] if sign == '~' else assignment[atom] for sign, atom in clause)


def unit_clause_propagation(clauses: List[List[Tuple[str, str]]], assignment: Dict[str, bool], debug: bool = False) -> Optional[List[List[Tuple[str, str]]]]:
    """
    Apply the unit clause heuristic: if a clause has a single literal, 
    that literal must be true.
    """
    while True:
        unit_clauses = [clause for clause in clauses if len(clause) == 1]
        if not unit_clauses:
            break
        
        for clause in unit_clauses:
            sign, literal = clause[0]
            value = sign != '~'
            if literal in assignment and assignment[literal] != value:
                return None  # Conflict found
            assignment[literal] = value
            if debug:
                print(f"Unit clause found: {literal}={'T' if value else 'F'}")
            clauses = simplify_clauses(clauses, literal, value, debug)

    return clauses


def pure_literal_elimination(clauses: List[List[Tuple[str, str]]], assignment: Dict[str, bool], debug: bool = False) -> List[List[Tuple[str, str]]]:
    """Apply the pure literal heuristic: eliminate literals that appear with only one polarity."""
    literals = {literal for clause in clauses for sign, literal in clause}
    pure_literals = {literal for literal in literals if all(sign == '' for sign, l in sum(clauses, []) if l == literal)
                     or all(sign == '~' for sign, l in sum(clauses, []) if l == literal)}

    for literal in pure_literals:
        value = not any(sign == '~' for sign, l in sum(clauses, []) if l == literal)
        assignment[literal] = value
        clauses = simplify_clauses(clauses, literal, value, debug)
        if debug:
            print(f"Pure literal found: {literal}={'T' if value else 'F'}")

    return clauses


def simplify_clauses(clauses: List[List[Tuple[str, str]]], literal: str, value: bool, debug: bool = False) -> List[List[Tuple[str, str]]]:
    """Simplify clauses by removing satisfied clauses and false literals."""
    new_clauses = []
    for clause in clauses:
        # If the clause is satisfied by the current assignment, remove it.
        if any((sign == '' and value) or (sign == '~' and not value) for sign, atom in clause if atom == literal):
            if debug:
                print(f"Clause satisfied: {clause}")
            continue  # Clause is satisfied

        # Otherwise, remove the literal from the clause and keep the rest.
        new_clause = [(sign, atom) for sign, atom in clause if atom != literal]
        new_clauses.append(new_clause)

    return new_clauses


def dpll(clauses: List[List[Tuple[str, str]]], atoms: List[str], assignment: Dict[str, bool], use_unit: bool, use_pure: bool, debug: bool = False) -> Optional[Dict[str, bool]]:
    """DPLL recursive backtracking search with optional debugging."""
    if debug:
        print(f"Current assignment: {assignment}")
        print(f"Remaining clauses: {clauses}")
    
    clauses = unit_clause_propagation(clauses, assignment, debug) if use_unit else clauses
    if clauses is None:
        if debug:
            print("Conflict during unit clause propagation.")
        return None  # Conflict due to unit propagation
    clauses = pure_literal_elimination(clauses, assignment, debug) if use_pure else clauses
    
    if not clauses:
        return assignment  # All clauses are satisfied
    if any(len(clause) == 0 for clause in clauses):
        if debug:
            print("Conflict: Empty clause found.")
        return None  # Unsatisfiable (empty clause found)

    # Choose an unassigned atom and recurse
    unassigned = [atom for atom in atoms if atom not in assignment]
    if not unassigned:
        return assignment

    atom = unassigned[0]
    for value in [True, False]:
        new_assignment = assignment.copy()
        new_assignment[atom] = value
        if debug:
            print(f"Trying {atom} = {'T' if value else 'F'}")
        simplified_clauses = simplify_clauses(clauses, atom, value, debug)
        result = dpll(simplified_clauses, atoms, new_assignment, use_unit, use_pure, debug)
        if result is not None:
            return result

    return None


def format_output(assignment: Optional[Dict[str, bool]]) -> str:
    """Format the output as 'satisfiable' or 'unsatisfiable' with assignments."""
    if assignment is None:
        return 'unsatisfiable'
    return 'satisfiable ' + ' '.join(f'{atom}={"T" if assignment.get(atom, False) else "F"}' for atom in atoms)


def parse_command_line_options() -> Tuple[bool, bool, bool]:
    """Parse command-line arguments to determine whether to use heuristics and debugging."""
    use_unit, use_pure, debug = True, True, False
    if '--nounit' in sys.argv:
        use_unit = False
    if '--nopure' in sys.argv:
        use_pure = False
    if '--debug' in sys.argv:
        debug = True
    return use_unit, use_pure, debug


if __name__ == '__main__':
    clauses, atoms = parse_input()
    use_unit, use_pure, debug = parse_command_line_options()
    assignment = dpll(clauses, atoms, {}, use_unit, use_pure, debug)
    print(format_output(assignment))
