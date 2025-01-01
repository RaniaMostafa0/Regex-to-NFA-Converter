Overview:
This Python program converts a given regular expression into a Non-Deterministic Finite Automaton (NFA). The process involves parsing the regular expression, converting it to postfix notation (using the Shunting Yard algorithm), and constructing the corresponding NFA. The resulting automaton is visualized as a graph using Graphviz and displayed with Matplotlib.
Features:
- Converts regular expressions to NFAs.
-Supports basic regex operations like concatenation, union (|), Kleene star (*), and one-or-more (+).
- Visualizes the generated NFA as a graph.
Output:
- Console output includes details of the NFA: states, transitions, start, and final states.
- A visual graph of the NFA saved as nfa.png and displayed using Matplotlib.
