# ==========================================================================
# EFREI P2 INT 2025/2026 – Finite Automata and Regular Expressions
# Operations on Finite Automata
#
# WHAT IS A FINITE AUTOMATON (FA)?
# --------------------------------
# A Finite Automaton is a mathematical model of computation. Think of it
# as a machine that reads a word (a sequence of symbols like "abba") one
# symbol at a time. At each step, it moves from one "state" to another
# based on the symbol it just read. After reading the entire word, if
# the machine is in an "accepting" (final) state, the word is ACCEPTED;
# otherwise it is REJECTED.
#
# Formally, a FA is defined by 5 components (called a 5-tuple):
#   - Q      : a finite set of STATES (e.g., {0, 1, 2, 3})
#   - Sigma  : a finite ALPHABET of symbols (e.g., {a, b})
#   - delta  : a TRANSITION FUNCTION that tells us, for a given state
#              and symbol, which state(s) to go to next
#   - q0     : one or more INITIAL states (where the machine starts)
#   - F      : a set of FINAL (accepting/terminal) states
#
# This program implements all 7 project stages:
#   1. Reading a FA from a text file and displaying it
#   2. Checking properties: deterministic / complete / standard
#   3. Standardization on demand
#   4. Determinization and completion
#   5. Minimization (partition refinement / Moore's algorithm)
#   6. Word recognition
#   7. Complementary language automaton
# ==========================================================================

# --- Python Standard Library Imports ---
# 'os' provides functions to interact with the operating system,
# e.g., listing files in a directory.
import os
# 'copy' provides functions to duplicate objects in memory.
# (imported for potential deep-copy needs; not strictly used here)
import copy


# ──────────────────────────────────────────────────────────────────────
#  DATA STRUCTURE
# ──────────────────────────────────────────────────────────────────────

class FiniteAutomaton:
    """
    This class is our DATA STRUCTURE to represent a Finite Automaton in memory.

    WHY A CLASS?
    A class groups related data together. Instead of having 5 separate
    variables floating around, we bundle them into one object. This makes
    our code cleaner and easier to pass around between functions.

    ATTRIBUTES (the 5 components of a FA):
      - alphabet    : list of characters, e.g., ['a', 'b']
                      These are the symbols the automaton can read.
      - states      : set of integers, e.g., {0, 1, 2, 3, 4}
                      Each integer is a label for a state.
      - initial     : set of integers — the INITIAL (start) state(s).
                      The machine begins processing a word from these states.
      - final       : set of integers — the FINAL (accepting/terminal) states.
                      If we end up in one of these after reading a word,
                      the word is ACCEPTED.
      - transitions : dictionary mapping (state, symbol) -> set of states.
                      This is the TRANSITION FUNCTION (delta).
                      Example: {(0,'a'): {0,1}} means "from state 0, reading
                      symbol 'a', we can go to state 0 OR state 1".
                      If the set has more than one element, the FA is
                      non-deterministic (NFA).

    WHY USE A SET FOR TARGETS?
    Because a non-deterministic FA can have MULTIPLE target states for one
    (state, symbol) pair. Using a set lets us handle both DFA (exactly 1
    target) and NFA (0 or more targets) with the same data structure.
    """

    def __init__(self):
        """Constructor: called when we create a new FiniteAutomaton().
        Initializes all attributes to empty collections."""
        self.alphabet = []        # e.g. ['a', 'b']
        self.states = set()       # e.g. {0, 1, 2, 3, 4}
        self.initial = set()      # e.g. {0}
        self.final = set()        # e.g. {4}
        self.transitions = {}     # e.g. {(0,'a'): {0,1}, (0,'b'): {0}, ...}

    def add_transition(self, src, symbol, dst):
        """
        Add a single transition: from state 'src', reading 'symbol', go to 'dst'.

        HOW IT WORKS:
        - We use the tuple (src, symbol) as a dictionary key.
        - The value is a SET of destination states.
        - If the key doesn't exist yet, we create a new empty set first.
        - Then we add 'dst' to that set.

        EXAMPLE:
          add_transition(0, 'a', 1)  -> transitions[(0,'a')] = {1}
          add_transition(0, 'a', 2)  -> transitions[(0,'a')] = {1, 2}
          (Now state 0 with 'a' leads to BOTH 1 and 2 -> non-deterministic!)
        """
        key = (src, symbol)  # Create the dictionary key as a tuple
        if key not in self.transitions:
            # First time we see this (state, symbol) pair -> create empty set
            self.transitions[key] = set()
        # Add the destination state to the set of targets
        self.transitions[key].add(dst)

    def get_targets(self, state, symbol):
        """
        Return the set of states reachable from 'state' by reading 'symbol'.

        Uses dict.get(key, default): if the key exists, return its value;
        otherwise return the default (an empty set), meaning "no transition".

        EXAMPLE:
          If transitions = {(0,'a'): {1,2}, (0,'b'): {0}}
          get_targets(0, 'a') -> {1, 2}
          get_targets(0, 'b') -> {0}
          get_targets(0, 'c') -> set()   (no transition defined)
        """
        return self.transitions.get((state, symbol), set())


# ──────────────────────────────────────────────────────────────────────
#  1. READING A FA FROM A TEXT FILE
# ──────────────────────────────────────────────────────────────────────

def read_automaton_from_file(filename):
    """
    Read a Finite Automaton definition from a text (.txt) file and build
    a FiniteAutomaton object in memory.

    FILE FORMAT (as specified in the project):
      Line 1 : number of symbols in the alphabet (integer)
      Line 2 : number of states (integer)
      Line 3 : number of initial states, followed by their numeric labels
      Line 4 : number of final states, followed by their numeric labels
      Line 5 : number of transitions (integer)
      Lines 6+: one transition per line in the form <source><symbol><target>
                e.g. "0a1" means: from state 0, reading symbol 'a', go to state 1

    EXAMPLE FILE for the automaton in the project spec:
        2          <- 2 symbols: a, b
        5          <- 5 states: 0, 1, 2, 3, 4
        1 0        <- 1 initial state: {0}
        1 4        <- 1 final state: {4}
        6          <- 6 transitions follow
        0a0        <- state 0 --a--> state 0
        0b0        <- state 0 --b--> state 0
        0a1        <- state 0 --a--> state 1
        1b2        <- state 1 --b--> state 2
        2a3        <- state 2 --a--> state 3
        3a4        <- state 3 --a--> state 4

    Returns:
        A FiniteAutomaton object with all data loaded.
    """
    # Create a new empty automaton object
    fa = FiniteAutomaton()

    # --- Read the file ---
    # 'with open(...)' opens the file and automatically closes it when done.
    # We read ALL lines at once, strip whitespace from each line,
    # and ignore blank lines.
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() != '']

    # 'idx' is our line pointer — it tracks which line we're currently reading.
    idx = 0

    # --- Line 1: Number of symbols in the alphabet ---
    # If num_symbols = 2, the alphabet is ['a', 'b'].
    # If num_symbols = 3, the alphabet is ['a', 'b', 'c'].
    # chr(ord('a') + i) converts a number to its corresponding letter:
    #   ord('a') = 97, so chr(97+0)='a', chr(97+1)='b', chr(97+2)='c', etc.
    num_symbols = int(lines[idx]); idx += 1
    fa.alphabet = [chr(ord('a') + i) for i in range(num_symbols)]

    # --- Line 2: Number of states ---
    # States are numbered from 0 to num_states-1.
    # set(range(5)) creates {0, 1, 2, 3, 4}.
    num_states = int(lines[idx]); idx += 1
    fa.states = set(range(num_states))

    # --- Line 3: Initial states ---
    # Format: "<count> <state1> <state2> ..."
    # Example: "1 0" means 1 initial state, which is state 0.
    # Example: "2 0 1" means 2 initial states: state 0 and state 1.
    # .split() breaks the string by whitespace into a list of substrings.
    parts = lines[idx].split(); idx += 1
    num_initial = int(parts[0])          # How many initial states
    for i in range(1, num_initial + 1):  # Read each initial state label
        fa.initial.add(int(parts[i]))

    # --- Line 4: Final (terminal/accepting) states ---
    # Same format as line 3.
    parts = lines[idx].split(); idx += 1
    num_final = int(parts[0])
    for i in range(1, num_final + 1):
        fa.final.add(int(parts[i]))

    # --- Line 5: Number of transitions ---
    num_transitions = int(lines[idx]); idx += 1

    # --- Lines 6+: Read each transition ---
    # Each transition is a string like "0a1" (state 0, symbol 'a', state 1).
    # We need to PARSE this string to extract the three parts.
    # The tricky part: state numbers can have multiple digits (e.g., "12a3").
    # Strategy: scan from the left, collecting digits for the source state,
    # then the first letter is the symbol, then the remaining digits are the target.
    for i in range(num_transitions):
        t = lines[idx]; idx += 1

        # Find where the source state ends and the symbol begins.
        # We scan character by character: as long as we see digits, it's
        # part of the source state number.
        j = 0
        while j < len(t) and t[j].isdigit():
            j += 1
        # Now: t[:j] is the source state, t[j] is the symbol, t[j+1:] is the target
        src = int(t[:j])       # e.g., "12" -> 12
        symbol = t[j]          # e.g., 'a'
        dst = int(t[j+1:])     # e.g., "3" -> 3

        # Add this transition to our automaton
        fa.add_transition(src, symbol, dst)

    return fa


# ──────────────────────────────────────────────────────────────────────
#  2. DISPLAYING A FA ON SCREEN
# ──────────────────────────────────────────────────────────────────────

def format_state_label(state, initial_states, final_states):
    """
    Create a prefix marker string for a state in the transition table.

    MARKERS:
      'E' = Entry (initial state)   — where the automaton starts
      'S' = Sortie (final state)    — accepting/terminal state
      'ES' = both initial AND final — the start state also accepts
      ''  = neither                 — a regular intermediate state

    These markers appear in the leftmost column of the transition table
    so the reader can immediately see which states are special.
    """
    markers = ""                     # Start with an empty string
    if state in initial_states:      # Is this state an initial state?
        markers += "E"               # Mark with 'E' for Entry
    if state in final_states:        # Is this state a final state?
        markers += "S"               # Mark with 'S' for Sortie (exit)
    return markers                   # Return e.g. "", "E", "S", or "ES"


def display_automaton(fa, title="Finite Automaton"):
    """
    Display the automaton on screen in a human-readable format.

    OUTPUT INCLUDES:
      - A title header
      - The list of initial state(s)
      - The list of final state(s)
      - The alphabet
      - A TRANSITION TABLE with properly aligned columns

    THE TRANSITION TABLE looks like this:
        +------+-------+-----+
        |      |   a   |  b  |
        +------+-------+-----+
        | E 0  | {0,1} | {0} |     <- 'E' marks state 0 as initial (Entry)
        |   1  |  --   | {2} |     <- '--' means no transition for that symbol
        | S 4  |  --   |  -- |     <- 'S' marks state 4 as final (Sortie)
        +------+-------+-----+

    HOW ALIGNMENT WORKS:
    We compute the maximum width needed for each column, then center
    every cell within that width. This ensures the table looks good
    regardless of how many digits the state numbers have.
    """
    # Sort states numerically so the table rows appear in order 0, 1, 2, ...
    sorted_states = sorted(fa.states)
    sorted_alpha = list(fa.alphabet)

    # --- Print the header information ---
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)

    # f-string with join: converts each state number to a string and joins with ', '
    print(f"  Initial state(s) : {{{', '.join(str(s) for s in sorted(fa.initial))}}}")
    print(f"  Final state(s)   : {{{', '.join(str(s) for s in sorted(fa.final))}}}")
    print(f"  Alphabet         : {{{', '.join(fa.alphabet)}}}")
    print(f"  Number of states : {len(fa.states)}")
    print()

    # --- Build the transition table as a 2D grid of strings ---
    # Header row: first cell is empty (for the state column), then one cell per symbol
    header = [""] + sorted_alpha

    # Build one row per state
    rows = []
    for s in sorted_states:
        # Get the marker ("E", "S", "ES", or "") for this state
        marker = format_state_label(s, fa.initial, fa.final)
        if marker:
            label = f"{marker} {s}"   # e.g. "E 0" or "S 4" or "ES 0"
        else:
            label = f"  {s}"          # e.g. "  1" (leading spaces for alignment)

        row = [label]  # Start the row with the state label
        for a in sorted_alpha:
            targets = fa.get_targets(s, a)  # Get set of target states
            if targets:
                # Format as "{0,1}" — curly braces with comma-separated state numbers
                row.append("{" + ",".join(str(t) for t in sorted(targets)) + "}")
            else:
                # No transition exists for this (state, symbol) pair
                row.append("--")
        rows.append(row)

    # --- Compute column widths for proper alignment ---
    # Each column should be as wide as its longest cell content
    col_widths = [0] * len(header)
    # Check header widths
    for c in range(len(header)):
        col_widths[c] = max(col_widths[c], len(header[c]))
    # Check each row's cell widths
    for row in rows:
        for c in range(len(row)):
            col_widths[c] = max(col_widths[c], len(row[c]))

    # Add 2 characters of padding (1 space on each side of the content)
    for c in range(len(col_widths)):
        col_widths[c] += 2

    # --- Print the formatted table ---
    # Separator line: "+-----+-----+-----+"
    sep = "+" + "+".join("-" * w for w in col_widths) + "+"

    # Print header row
    print(sep)
    hdr_line = "|"
    for c, h in enumerate(header):
        # .center(width) centers the string within 'width' characters
        hdr_line += h.center(col_widths[c]) + "|"
    print(hdr_line)
    print(sep)

    # Print data rows (one per state)
    for row in rows:
        r_line = "|"
        for c, cell in enumerate(row):
            r_line += cell.center(col_widths[c]) + "|"
        print(r_line)
    print(sep)
    print()


# ──────────────────────────────────────────────────────────────────────
#  3. PROPERTY CHECKS: deterministic, complete, standard
# ──────────────────────────────────────────────────────────────────────

def is_deterministic(fa, verbose=True):
    """
    Check whether the automaton is DETERMINISTIC (DFA).

    DEFINITION:
    A Finite Automaton is deterministic if and only if:
      1. It has EXACTLY ONE initial state (not zero, not multiple).
      2. For every (state, symbol) pair, there is AT MOST ONE target state.
         (i.e., from any state reading any symbol, there is only one
          possible next state — no ambiguity, no "choice").

    If either condition is violated, the FA is NON-DETERMINISTIC (NFA).

    WHY DOES THIS MATTER?
    - A DFA processes each word in exactly one way — one path through states.
    - An NFA can have multiple possible paths (branching), which makes it
      harder to simulate but sometimes easier to design.
    - We need a DFA for word recognition (step 6), so if we have an NFA,
      we must determinize it first (step 4).

    Parameters:
        fa      : the FiniteAutomaton to check
        verbose : if True, print the reasons when the FA is not deterministic

    Returns:
        True if deterministic, False otherwise.
    """
    reasons = []  # Collect all reasons why the FA might not be deterministic

    # CHECK 1: Does it have more than one initial state?
    if len(fa.initial) > 1:
        reasons.append(f"  - It has {len(fa.initial)} initial states: "
                       f"{{{', '.join(str(s) for s in sorted(fa.initial))}}} "
                       f"(must have exactly 1).")

    # CHECK 2: For every (state, symbol), is there at most 1 target?
    for s in sorted(fa.states):
        for a in fa.alphabet:
            targets = fa.get_targets(s, a)
            if len(targets) > 1:
                # Found a (state, symbol) with multiple possible next states
                # -> this is the defining property of non-determinism
                reasons.append(
                    f"  - State {s} with symbol '{a}' leads to multiple states: "
                    f"{{{', '.join(str(t) for t in sorted(targets))}}}.")

    # Report the result
    if reasons:
        if verbose:
            print("  The automaton is NOT deterministic because:")
            for r in reasons:
                print(r)
        return False
    else:
        if verbose:
            print("  The automaton IS deterministic.")
        return True


def is_complete(fa, verbose=True):
    """
    Check whether a DETERMINISTIC automaton is COMPLETE.

    DEFINITION:
    A deterministic FA is complete if, for EVERY state and EVERY symbol
    in the alphabet, there exists EXACTLY ONE transition.
    In other words, no matter what state we are in and what symbol we
    read, there is always a defined next state — there is no "dead end".

    EXAMPLE OF INCOMPLETE:
    If state 2 has no transition for symbol 'b', the automaton doesn't
    know what to do when reading 'b' in state 2 — it's incomplete.

    WHY THIS MATTERS:
    An incomplete DFA can't process words that reach a "missing" transition.
    To fix this, we add a SINK STATE (also called "trash" or "bin" state)
    that absorbs all missing transitions — see the complete() function.

    NOTE: This function should only be called on a deterministic FA.
    """
    reasons = []  # Collect all missing transitions

    # Check every (state, symbol) pair
    for s in sorted(fa.states):
        for a in fa.alphabet:
            targets = fa.get_targets(s, a)
            if len(targets) == 0:
                # Found a state with no transition for this symbol -> incomplete
                reasons.append(
                    f"  - State {s} has no transition for symbol '{a}'.")

    if reasons:
        if verbose:
            print("  The automaton is NOT complete because:")
            for r in reasons:
                print(r)
        return False
    else:
        if verbose:
            print("  The automaton IS complete.")
        return True


def is_standard(fa, verbose=True):
    """
    Check whether the automaton is STANDARD.

    DEFINITION:
    A FA is standard if and only if:
      1. It has EXACTLY ONE initial state.
      2. NO transition in the entire automaton leads TO the initial state.
         (i.e., the initial state has no incoming arrows)

    WHY IS STANDARDNESS USEFUL?
    A standard automaton is easier to combine with other automata
    (e.g., for union or concatenation operations on languages).
    The key property is that the initial state is "clean" — it's never
    revisited once you leave it.

    EXAMPLE:
    If state 0 is initial and there's a transition (1, 'a') -> 0, then
    the automaton is NOT standard because we can go BACK to the initial state.
    """
    reasons = []

    # CHECK 1: Exactly one initial state?
    if len(fa.initial) != 1:
        reasons.append(f"  - It has {len(fa.initial)} initial states "
                       f"(must have exactly 1).")
    else:
        # CHECK 2: Does any transition lead TO the initial state?
        i0 = next(iter(fa.initial))  # Get the single initial state
        # next(iter(...)) extracts the one element from a single-element set
        for s in fa.states:
            for a in fa.alphabet:
                targets = fa.get_targets(s, a)
                if i0 in targets:
                    # Found a transition that goes back to the initial state!
                    reasons.append(
                        f"  - Transition ({s}, '{a}') -> {i0} leads back "
                        f"to the initial state.")

    if reasons:
        if verbose:
            print("  The automaton is NOT standard because:")
            for r in reasons:
                print(r)
        return False
    else:
        if verbose:
            print("  The automaton IS standard.")
        return True


# ──────────────────────────────────────────────────────────────────────
#  4. STANDARDIZATION
# ──────────────────────────────────────────────────────────────────────

def standardize(fa):
    """
    Build a STANDARD automaton equivalent to the given FA.

    ALGORITHM (from the course):
    1. Create a NEW initial state 'i' (with a fresh label not used yet).
    2. For every symbol in the alphabet, the new state 'i' gets the UNION
       of all outgoing transitions from ALL old initial states.
       (i.e., 'i' can go everywhere the old initial states could go)
    3. The new state 'i' is marked as FINAL if at least one of the old
       initial states was final (to preserve acceptance of the empty word).
    4. No transition leads to 'i' (since it's brand new), so the result
       is standard by construction.

    WHY THIS WORKS:
    The new automaton recognizes exactly the same language because 'i'
    mimics all old initial states, but since nothing points to 'i', it
    satisfies the standard property.

    Returns a new FiniteAutomaton (does NOT modify the original).
    """
    sfa = FiniteAutomaton()            # Create a new empty automaton
    sfa.alphabet = list(fa.alphabet)   # Copy the alphabet

    # Choose a label for the new initial state that doesn't conflict
    # with existing state labels. Since states are 0..n-1, we use n.
    new_i = max(fa.states) + 1

    # The new automaton has all old states PLUS the new initial state
    # The '|' operator on sets means UNION: {0,1,2} | {3} = {0,1,2,3}
    sfa.states = fa.states | {new_i}
    sfa.initial = {new_i}  # Only the new state is initial

    # Copy the final states from the original
    sfa.final = set(fa.final)
    # If any old initial state was also final, the new initial must be final too.
    # This preserves recognition of the empty word (epsilon).
    # 'fa.initial & fa.final' computes the INTERSECTION of the two sets:
    # if it's non-empty, at least one initial state is also final.
    if fa.initial & fa.final:
        sfa.final.add(new_i)

    # Copy ALL original transitions unchanged
    for (s, a), targets in fa.transitions.items():
        for t in targets:
            sfa.add_transition(s, a, t)

    # Add transitions FROM new_i: for each symbol, new_i goes wherever
    # ANY of the old initial states could go.
    for old_i in fa.initial:
        for a in fa.alphabet:
            for t in fa.get_targets(old_i, a):
                sfa.add_transition(new_i, a, t)

    return sfa


# ──────────────────────────────────────────────────────────────────────
#  5. DETERMINIZATION AND COMPLETION
# ──────────────────────────────────────────────────────────────────────

def _frozenset_label(fs, separator="."):
    """
    Create a human-readable label from a frozenset of states.
    Example: frozenset({1, 2, 3}) -> "1.2.3"
    The separator ensures we can distinguish {1,2,3} from {12,3}.
    """
    return separator.join(str(s) for s in sorted(fs))


def determinize_and_complete(fa):
    """
    Convert a Non-Deterministic FA (NFA) into a Complete Deterministic FA (CDFA)
    using the SUBSET CONSTRUCTION algorithm (also called "powerset construction").

    THE IDEA (from lectures):
    In an NFA, reading a symbol from a state can lead to MULTIPLE states.
    The key insight is: instead of tracking ONE current state, we track
    the SET of all states the NFA could currently be in.

    Each "macro-state" in the new DFA represents a SET of original NFA states.
    For example, if the NFA could be in states {0, 1, 3} after reading "ab",
    then {0,1,3} becomes a single state in the DFA.

    ALGORITHM STEPS:
    1. Start with the macro-state = set of all initial states of the NFA.
    2. For each unprocessed macro-state and each symbol:
       - Compute the UNION of all targets from every state in the macro-state.
       - This union becomes the new macro-state for that transition.
    3. Repeat until no new macro-states are discovered (BFS exploration).
    4. A macro-state is FINAL if it contains at least one original final state.
    5. After determinization, COMPLETE the automaton by adding a sink state
       for any missing transitions.

    WHAT IS A FROZENSET?
    A frozenset is Python's immutable (unchangeable) version of a set.
    We need it because we want to use sets as dictionary keys, and Python
    requires dictionary keys to be immutable (hashable).

    Returns:
        (cdfa, state_map) where:
        - cdfa is the resulting Complete Deterministic FiniteAutomaton
        - state_map is a dict {new_int_label: frozenset of original states}
          showing what each new state corresponds to in the original NFA.
    """
    cdfa = FiniteAutomaton()
    cdfa.alphabet = list(fa.alphabet)

    # --- Step 1: The initial macro-state ---
    # It's the frozenset of ALL initial states from the original NFA.
    # Example: if initial = {0}, then start = frozenset({0})
    # Example: if initial = {0, 1}, then start = frozenset({0, 1})
    start = frozenset(fa.initial)

    # --- Step 2-3: BFS exploration (work-list algorithm) ---
    # 'unmarked' = list of macro-states we still need to process
    # 'all_macro' = set of all macro-states we've discovered so far
    # 'macro_transitions' = the transition function for the new DFA
    unmarked = [start]          # Start by processing the initial macro-state
    all_macro = {start}         # We've discovered the initial macro-state
    macro_transitions = {}      # Will map (frozenset, symbol) -> frozenset

    while unmarked:
        # Take the next unprocessed macro-state
        current = unmarked.pop(0)  # pop(0) = remove and return the first element (FIFO/BFS)

        for a in fa.alphabet:
            # Compute the union of all targets for every state in 'current'
            # Example: current = {0, 1}, symbol = 'a'
            #   targets of state 0 with 'a' = {0, 1}
            #   targets of state 1 with 'a' = {2}
            #   union = {0, 1, 2}  -> this becomes the new macro-state
            target = set()
            for s in current:
                # |= is the set union-assignment operator: target = target | ...
                target |= fa.get_targets(s, a)
            target = frozenset(target)  # Make it immutable so we can use it as a key

            # Record this transition
            macro_transitions[(current, a)] = target

            # If this macro-state is new, add it to our exploration list
            if target not in all_macro:
                all_macro.add(target)
                unmarked.append(target)

    # --- Step 4: Assign integer labels to each macro-state ---
    # Sort for reproducible output (same input always gives same numbering)
    macro_list = sorted(all_macro, key=lambda fs: (len(fs), sorted(fs)))
    state_map = {}  # new integer -> frozenset of original states
    for idx, ms in enumerate(macro_list):
        state_map[idx] = ms

    # Create reverse mapping: frozenset -> new integer
    inv_map = {ms: idx for idx, ms in state_map.items()}

    # --- Build the CDFA using integer state labels ---
    cdfa.states = set(range(len(macro_list)))
    cdfa.initial = {inv_map[start]}  # Map the start macro-state to its integer label

    # A macro-state is final if it contains at least one original final state
    # 'ms & fa.final' is the set intersection; non-empty means overlap exists
    for idx, ms in state_map.items():
        if ms & fa.final:
            cdfa.final.add(idx)

    # Copy transitions using the new integer labels
    for (ms, a), target_ms in macro_transitions.items():
        cdfa.add_transition(inv_map[ms], a, inv_map[target_ms])

    # --- Step 5: COMPLETION ---
    # Check if any (state, symbol) pair is missing a transition.
    # If so, we need a SINK STATE (a "trash" state that goes to itself
    # for all symbols and is NOT final). This ensures the DFA is complete.
    needs_sink = False
    for s in list(cdfa.states):
        for a in cdfa.alphabet:
            if not cdfa.get_targets(s, a):
                needs_sink = True
                break
        if needs_sink:
            break

    if needs_sink:
        # Create the sink state with a fresh label
        sink = max(cdfa.states) + 1
        cdfa.states.add(sink)
        state_map[sink] = frozenset()  # Sink corresponds to the EMPTY set of original states
        # All missing transitions go to the sink; sink goes to itself for all symbols
        for s in cdfa.states:
            for a in cdfa.alphabet:
                if not cdfa.get_targets(s, a):
                    cdfa.add_transition(s, a, sink)

    return cdfa, state_map


def complete(fa):
    """
    Complete a DETERMINISTIC (but incomplete) FA by adding a SINK STATE.

    WHAT IS A SINK STATE?
    A sink state (also called "trash" or "bin" state, noted 'P' for 'poubelle'
    in French) is a non-final state that, for every symbol, transitions
    only to itself. It's like a "black hole": once you enter it, you can
    never leave, and since it's not final, any word that reaches it is rejected.

    ALGORITHM:
    1. Make a copy of the original FA.
    2. Scan all (state, symbol) pairs for missing transitions.
    3. If any are missing, create a new sink state.
    4. Point all missing transitions to the sink state.

    Returns:
        (cdfa, sink) where:
        - cdfa is the completed automaton
        - sink is the label of the added sink state, or None if no sink was needed
    """
    # Create a copy of the original FA
    cdfa = FiniteAutomaton()
    cdfa.alphabet = list(fa.alphabet)
    cdfa.states = set(fa.states)      # Copy the set of states
    cdfa.initial = set(fa.initial)    # Copy initial states
    cdfa.final = set(fa.final)        # Copy final states

    # Copy all transitions
    for (s, a), targets in fa.transitions.items():
        for t in targets:
            cdfa.add_transition(s, a, t)

    # Check if any (state, symbol) pair is missing a transition
    needs_sink = False
    for s in cdfa.states:
        for a in cdfa.alphabet:
            if not cdfa.get_targets(s, a):  # Empty set = missing transition
                needs_sink = True
                break
        if needs_sink:
            break

    # If we need a sink, create it and fill in all missing transitions
    sink = None
    if needs_sink:
        sink = max(cdfa.states) + 1   # Fresh label (e.g., if states are 0-4, sink = 5)
        cdfa.states.add(sink)         # Add the sink to the set of states
        # For every state (including the sink itself) and every symbol,
        # if no transition exists, add one pointing to the sink.
        # This also makes the sink point to itself for all symbols.
        for s in cdfa.states:
            for a in cdfa.alphabet:
                if not cdfa.get_targets(s, a):
                    cdfa.add_transition(s, a, sink)

    return cdfa, sink


# ──────────────────────────────────────────────────────────────────────
#  6. MINIMIZATION (partition refinement / Moore's algorithm)
# ──────────────────────────────────────────────────────────────────────

def minimize(cdfa):
    """
    Minimize a Complete Deterministic FA using PARTITION REFINEMENT
    (also called Moore's algorithm).

    WHAT IS MINIMIZATION?
    Two states are "equivalent" if, no matter what word you read from them,
    they both lead to the same accept/reject decision. Minimization merges
    all equivalent states into one, producing the smallest possible DFA
    that recognizes the same language.

    ALGORITHM (from lectures):
    1. INITIAL PARTITION: split all states into two groups:
       - Group of FINAL states (accepting)
       - Group of NON-FINAL states (rejecting)
       These are definitely NOT equivalent to each other (one accepts
       the empty word continuation, the other doesn't).

    2. REFINEMENT LOOP: for each group, check if all states in the group
       behave the same way. Two states s1 and s2 are in the same group
       only if, for EVERY symbol, they both go to states in the SAME group.
       If they don't, SPLIT the group.

    3. Repeat step 2 until the partition stops changing (is "stable").

    4. Build the minimal automaton: each group becomes one state.

    WHAT IS A "SIGNATURE"?
    For a state s, its signature is a tuple of group numbers where s goes
    for each symbol. Example: if s goes to group 0 for 'a' and group 1
    for 'b', its signature is (0, 1). States with different signatures
    must be in different groups.

    Returns:
        (mcdfa, partition_map) where:
        - mcdfa is the Minimal Complete Deterministic FiniteAutomaton
        - partition_map is {new_state: frozenset of original CDFA states}
    """
    sorted_states = sorted(cdfa.states)

    # --- Step 1: INITIAL PARTITION ---
    # Separate final states from non-final states.
    # These two groups are our starting point.
    finals = frozenset(s for s in sorted_states if s in cdfa.final)
    non_finals = frozenset(s for s in sorted_states if s not in cdfa.final)

    partition = []  # List of groups (each group is a frozenset of states)
    if non_finals:
        partition.append(non_finals)
    if finals:
        partition.append(finals)

    # Display the initial partition
    step = 0
    print(f"\n  --- Minimization: step {step} (initial partition) ---")
    print(f"  Partition: {_format_partition(partition)}")

    # HELPER FUNCTION: given a state, find which group number it belongs to.
    # This is needed to compute signatures.
    def group_of(state):
        for i, grp in enumerate(partition):
            if state in grp:
                return i
        return -1  # Should never happen if the partition covers all states

    # --- Step 2-3: REFINEMENT LOOP ---
    while True:
        new_partition = []

        for grp in partition:
            # For each group, compute the SIGNATURE of every state in the group.
            # Signature = tuple of (group number of target) for each symbol.
            # States with the same signature stay together;
            # states with different signatures are split into different sub-groups.
            sig_map = {}  # signature (tuple) -> set of states with that signature
            for s in grp:
                # Build the signature: for each symbol, where does state s go?
                # next(iter(...)) gets the single target (DFA = exactly 1 target)
                sig = tuple(group_of(next(iter(cdfa.get_targets(s, a))))
                            for a in cdfa.alphabet)
                if sig not in sig_map:
                    sig_map[sig] = set()
                sig_map[sig].add(s)

            # Each unique signature creates a new sub-group
            for sub in sig_map.values():
                new_partition.append(frozenset(sub))

        step += 1
        # Sort groups by their smallest state for consistent display
        new_partition.sort(key=lambda fs: min(fs))

        # Display the new partition
        print(f"\n  --- Minimization: step {step} ---")
        print(f"  Partition: {_format_partition(new_partition)}")

        # Display transitions in terms of groups (for readability)
        print("  Transitions by group:")
        for gi, grp in enumerate(new_partition):
            rep = min(grp)  # Use the smallest state as a representative
            targets = []
            for a in cdfa.alphabet:
                t = next(iter(cdfa.get_targets(rep, a)))  # Target state
                # Find which group the target belongs to
                for gj, grp2 in enumerate(new_partition):
                    if t in grp2:
                        targets.append(f"G{gj}")
                        break
            print(f"    G{gi}{_format_partition_group(grp)} "
                  f"--({', '.join(cdfa.alphabet)})--> "
                  f"({', '.join(targets)})")

        # CHECK: has the partition stopped changing?
        if len(new_partition) == len(partition):
            if set(new_partition) == set(partition):
                print("\n  Partition is stable. Minimization complete.")
                break
        # Update partition for the next iteration
        partition = new_partition

    # --- Check if the automaton was already minimal ---
    # If the number of groups equals the number of original states,
    # no states were merged -> already minimal.
    if len(partition) == len(cdfa.states):
        print("  The automaton was already minimal.")

    # --- Step 4: BUILD THE MINIMAL AUTOMATON ---
    mcdfa = FiniteAutomaton()
    mcdfa.alphabet = list(cdfa.alphabet)

    # Create the mapping: new state number -> set of original states in that group
    partition_map = {}  # new state ID -> frozenset of original CDFA states
    for i, grp in enumerate(partition):
        partition_map[i] = grp

    # The minimal automaton has one state per group
    mcdfa.states = set(range(len(partition)))

    # The initial state of the MCDFA is whichever group contains
    # the original initial state
    old_initial = next(iter(cdfa.initial))
    for i, grp in enumerate(partition):
        if old_initial in grp:
            mcdfa.initial = {i}
            break

    # A group is final if it contains at least one original final state
    for i, grp in enumerate(partition):
        if grp & cdfa.final:  # Set intersection: non-empty = overlap
            mcdfa.final.add(i)

    # Build transitions: use any representative from each group
    # (they all behave the same, that's why they're in the same group!)
    for i, grp in enumerate(partition):
        rep = min(grp)  # Pick the smallest state as representative
        for a in cdfa.alphabet:
            t = next(iter(cdfa.get_targets(rep, a)))  # Where does rep go?
            # Find which group the target belongs to
            for j, grp2 in enumerate(partition):
                if t in grp2:
                    mcdfa.add_transition(i, a, j)
                    break

    return mcdfa, partition_map


def _format_partition(partition):
    """Format a partition for display, e.g. '{0,2,3}  {1,4}'.
    Each group is shown as a set in curly braces."""
    parts = []
    for grp in partition:
        parts.append("{" + ",".join(str(s) for s in sorted(grp)) + "}")
    return "  ".join(parts)


def _format_partition_group(grp):
    """Format a single group, e.g. '{0,2,3}'."""
    return "{" + ",".join(str(s) for s in sorted(grp)) + "}"


# ──────────────────────────────────────────────────────────────────────
#  7. WORD RECOGNITION
# ──────────────────────────────────────────────────────────────────────

def recognize_word(word, fa):
    """
    Test whether the (deterministic, complete) automaton FA ACCEPTS a word.

    HOW WORD RECOGNITION WORKS:
    1. Start at the initial state.
    2. Read the word symbol by symbol (left to right).
    3. For each symbol, follow the transition to the next state.
    4. After reading the entire word, check if the current state is FINAL.
       - If YES -> the word is ACCEPTED (it belongs to the language).
       - If NO  -> the word is REJECTED.

    IMPORTANT (from the project spec):
    The word must be fully read as a string BEFORE it is tested.
    There should be absolutely no letter-by-letter reading and testing.

    Parameters:
        word : string to test (e.g., "abba")
        fa   : a deterministic, complete FiniteAutomaton

    Returns:
        True if the word is accepted, False otherwise.
    """
    # --- Special case: empty word ---
    # The empty word (epsilon) is accepted iff the initial state is also final.
    if not word:
        current = next(iter(fa.initial))  # Get the single initial state
        accepted = current in fa.final
        print(f"    Empty word : start at state {current} -> "
              f"{'ACCEPTED' if accepted else 'REJECTED'}")
        return accepted

    # --- Validate: are all characters in the alphabet? ---
    for ch in word:
        if ch not in fa.alphabet:
            print(f"    Symbol '{ch}' is not in the alphabet "
                  f"{{{', '.join(fa.alphabet)}}}. Word REJECTED.")
            return False

    # --- Process the word symbol by symbol ---
    current = next(iter(fa.initial))  # Start at the initial state
    trace = [str(current)]           # Record the sequence of states visited

    for ch in word:
        targets = fa.get_targets(current, ch)
        if not targets:
            # This should not happen in a complete DFA, but just in case:
            print(f"    No transition from state {current} with '{ch}'. "
                  f"Word REJECTED.")
            return False
        # In a DFA, there's exactly one target state
        current = next(iter(targets))
        trace.append(str(current))  # Add the new state to the trace

    # --- Check if we ended in a final state ---
    accepted = current in fa.final
    print(f"    Trace: {' -> '.join(trace)}")
    print(f"    Final state {current} "
          f"{'is' if accepted else 'is NOT'} a terminal state.")
    print(f"    Result: {'ACCEPTED' if accepted else 'REJECTED'}")
    return accepted


# ──────────────────────────────────────────────────────────────────────
#  8. COMPLEMENTARY LANGUAGE
# ──────────────────────────────────────────────────────────────────────

def complementary_automaton(fa):
    """
    Build a FA that recognizes the COMPLEMENTARY LANGUAGE.

    WHAT IS THE COMPLEMENTARY LANGUAGE?
    If L is the language recognized by automaton A (the set of all words A accepts),
    then the complementary language L' is the set of ALL words over the alphabet
    that A REJECTS. In other words: L' = Sigma* - L.

    HOW TO COMPUTE IT:
    For a Complete Deterministic FA, simply SWAP final and non-final states!
    - Every state that WAS final becomes NON-final.
    - Every state that WAS non-final becomes FINAL.
    This works because in a CDFA, every word leads to exactly one state.
    A word accepted by the original is rejected by the complement, and vice versa.

    WARNING: This only works correctly on a COMPLETE DETERMINISTIC FA.
    If the FA is not complete, some words have no path, and swapping
    states wouldn't correctly handle those words.

    Parameters:
        fa : a Complete Deterministic FiniteAutomaton (CDFA or MCDFA)

    Returns:
        A new FiniteAutomaton recognizing the complementary language.
    """
    comp = FiniteAutomaton()
    comp.alphabet = list(fa.alphabet)   # Same alphabet
    comp.states = set(fa.states)        # Same states
    comp.initial = set(fa.initial)      # Same initial state

    # THE KEY OPERATION: swap final and non-final states
    # fa.states - fa.final = all states that are NOT in fa.final
    comp.final = fa.states - fa.final

    # Copy all transitions unchanged
    for (s, a), targets in fa.transitions.items():
        for t in targets:
            comp.add_transition(s, a, t)

    return comp


# ──────────────────────────────────────────────────────────────────────
#  DISPLAY HELPERS FOR DETERMINIZATION STATE MAPPING
# ──────────────────────────────────────────────────────────────────────

def display_state_composition(state_map, title="State Composition"):
    """
    Display a table showing the CORRESPONDENCE between new state labels
    and the original states they represent.

    WHY IS THIS NEEDED?
    After determinization, each new state is a SET of original states.
    After minimization, each new state is a GROUP of CDFA states.
    This table makes it clear which original states are "inside" each new state.

    Example output:
        New State    Original States
        ------------ ------------------------------
        0            {0, 1}
        1            {2}
        2            {3}
        3            {} (sink / trash state)
    """
    print(f"\n  {title}:")
    print(f"  {'New State':<12} {'Original States'}")
    print(f"  {'-'*12} {'-'*30}")
    for new_s in sorted(state_map.keys()):
        orig = state_map[new_s]
        if orig:
            # Format the set of original states
            orig_str = "{" + ", ".join(str(s) for s in sorted(orig)) + "}"
        else:
            # Empty set means this is the sink/trash state
            orig_str = "{} (sink / trash state)"
        print(f"  {new_s:<12} {orig_str}")
    print()


# ──────────────────────────────────────────────────────────────────────
#  MAIN MENU LOOP
# ──────────────────────────────────────────────────────────────────────

def list_automaton_files():
    """
    List all .txt files in the current working directory.
    These are the automaton description files the user can choose from.
    os.listdir('.') returns all files/folders in the current directory.
    We filter to keep only files ending with '.txt'.
    """
    files = [f for f in os.listdir('.') if f.endswith('.txt')]
    files.sort()  # Sort alphabetically for consistent ordering
    return files


def select_automaton():
    """
    Let the user interactively choose which automaton file to load.

    The user can:
      - Type a NUMBER (e.g., "1") to select from the numbered list
      - Type a FILENAME directly (e.g., "INT2-1_1.txt")
      - Type a PARTIAL NAME and we'll try to match it

    Returns:
        (fa, filename) where fa is the loaded FiniteAutomaton and filename
        is the name of the file, or (None, None) if selection failed.
    """
    files = list_automaton_files()
    if not files:
        print("  No .txt automaton files found in the current directory.")
        return None, None

    # Display the available files with numbers
    print("\n  Available automaton files:")
    for i, fname in enumerate(files):
        print(f"    {i + 1}. {fname}")

    choice = input("\n  Enter the number of the automaton to load (or filename): ").strip()

    try:
        # Try to interpret the input as a number
        idx = int(choice) - 1  # Convert to 0-indexed
        if 0 <= idx < len(files):
            filename = files[idx]
        else:
            print("  Invalid choice.")
            return None, None
    except ValueError:
        # Not a number -> treat it as a filename or partial match
        if choice in files:
            filename = choice
        else:
            # Try to find a file whose name contains the user's input
            matches = [f for f in files if choice in f]
            if len(matches) == 1:
                filename = matches[0]
            else:
                print("  File not found.")
                return None, None

    # Load the automaton from the selected file
    fa = read_automaton_from_file(filename)
    return fa, filename


def main():
    """
    Main program loop.

    This implements the "multiple automata loop" required by the project:
    the user can study several automata without restarting the program.

    OVERALL FLOW (following the project pseudocode):
    1. Select and load an automaton from a .txt file
    2. Display it
    3. Check properties (deterministic? complete? standard?)
    4. Standardize on demand
    5. Determinize and complete if needed
    6. Minimize
    7. Test word recognition
    8. Build and test the complementary automaton
    9. Ask if the user wants to study another automaton
    """
    print("=" * 60)
    print("  EFREI P2 INT 2025/2026")
    print("  Operations on Finite Automata")
    print("=" * 60)

    # === OUTER LOOP: allows studying multiple automata ===
    while True:

        # ── STEP 1: Select and display the automaton ──
        fa, filename = select_automaton()
        if fa is None:
            again = input("\n  Try again? (y/n): ").strip().lower()
            if again != 'y':
                break
            continue

        print(f"\n  Automaton loaded from: {filename}")
        display_automaton(fa, title=f"Original Automaton ({filename})")

        # ── STEP 2: Property checks ──
        # We check if the FA is deterministic, standard, and (if deterministic) complete.
        # These checks determine which operations we need to perform next.
        print("-" * 60)
        print("  PROPERTY CHECKS")
        print("-" * 60)

        det = is_deterministic(fa)  # Is it a DFA?
        print()
        std = is_standard(fa)       # Is it standard?
        print()

        # Completeness only makes sense for a deterministic FA
        if det:
            comp = is_complete(fa)
        else:
            comp = False
            print("  (Completeness check skipped: automaton is not deterministic.)")
        print()

        # ── STEP 3: Standardization on demand ──
        # As per the project spec: IF not standard, ASK the user if they want
        # to standardize. The standardized FA is used for subsequent operations.
        sfa = fa  # Default: continue with the original FA
        if not std:
            print("-" * 60)
            print("  STANDARDIZATION")
            print("-" * 60)
            want = input("  The automaton is not standard. "
                         "Do you want to standardize it? (y/n): ").strip().lower()
            if want == 'y':
                sfa = standardize(fa)
                display_automaton(sfa, title="Standardized Automaton")
            else:
                print("  Standardization skipped.")
        else:
            print("  The automaton is already standard. "
                  "No standardization needed.")

        # ── STEP 4: Determinization and Completion ──
        # Following the project pseudocode:
        #   - If already DFA and complete -> do nothing
        #   - If DFA but not complete -> just complete it
        #   - If NFA -> determinize AND complete
        # WARNING: We must NOT determinize a DFA (the spec says this is an error).
        print("\n" + "-" * 60)
        print("  DETERMINIZATION AND COMPLETION")
        print("-" * 60)

        work_fa = sfa  # Work on the (possibly standardized) automaton

        # Re-check properties on the working automaton (standardization may change things)
        det_w = is_deterministic(work_fa, verbose=False)
        comp_w = is_complete(work_fa, verbose=False) if det_w else False

        if det_w and comp_w:
            # CASE 1: Already a complete DFA -> nothing to do
            print("  The automaton is already deterministic and complete.")
            cdfa = work_fa
            cdfa_state_map = None
        elif det_w and not comp_w:
            # CASE 2: Deterministic but incomplete -> add a sink state
            print("  The automaton is deterministic but NOT complete.")
            print("  Completing the automaton...")
            cdfa, sink = complete(work_fa)
            if sink is not None:
                print(f"  Added sink (trash) state: {sink}")
            display_automaton(cdfa, title="Complete Deterministic Automaton (CDFA)")
            cdfa_state_map = None
        else:
            # CASE 3: Non-deterministic -> must determinize and complete
            print("  The automaton is NOT deterministic.")
            print("  Determinizing and completing the automaton...")
            cdfa, cdfa_state_map = determinize_and_complete(work_fa)
            display_automaton(cdfa,
                              title="Complete Deterministic Automaton (CDFA)")
            display_state_composition(cdfa_state_map,
                                      title="CDFA State Composition "
                                            "(new state -> original states)")

        # ── STEP 5: Minimization ──
        # Always minimize the CDFA. The minimize() function will detect
        # if the automaton was already minimal and inform the user.
        print("-" * 60)
        print("  MINIMIZATION")
        print("-" * 60)

        mcdfa, min_partition_map = minimize(cdfa)
        display_automaton(mcdfa,
                          title="Minimal Complete Deterministic Automaton (MCDFA)")
        display_state_composition(min_partition_map,
                                  title="MCDFA State Composition "
                                        "(new state -> CDFA states)")

        # ── STEP 6: Word recognition ──
        # The user types words to test. Each word is fully read as a string,
        # then tested against the MCDFA. Type 'end' to stop.
        print("-" * 60)
        print("  WORD RECOGNITION (on MCDFA)")
        print("-" * 60)
        print("  Type words to test recognition.")
        print("  Type 'end' to stop testing.\n")

        while True:
            word = input("  Enter a word (or 'end'): ").strip()
            if word.lower() == 'end':
                break
            recognize_word(word, mcdfa)
            print()

        # ── STEP 7: Complementary language ──
        # Build the complement of the MCDFA (swap final/non-final states)
        # and let the user test words on it.
        print("-" * 60)
        print("  COMPLEMENTARY LANGUAGE")
        print("-" * 60)
        print("  Building the complementary automaton from the MCDFA...")

        comp_fa = complementary_automaton(mcdfa)
        display_automaton(comp_fa, title="Complementary Automaton")

        print("  Word recognition on the complementary automaton:")
        print("  Type words to test. Type 'end' to stop.\n")
        while True:
            word = input("  Enter a word (or 'end'): ").strip()
            if word.lower() == 'end':
                break
            recognize_word(word, comp_fa)
            print()

        # ── Ask if the user wants to study another automaton ──
        print("\n" + "=" * 60)
        again = input("  Do you want to study another automaton? (y/n): ").strip().lower()
        if again != 'y':
            break

    print("\n  Goodbye!")


# ──────────────────────────────────────────────────────────────────────
#  PROGRAM ENTRY POINT
# ──────────────────────────────────────────────────────────────────────
# The 'if __name__ == "__main__"' idiom means:
# "Only run main() if this file is executed directly (not imported)."
# When you run 'python automaton.py', Python sets __name__ to "__main__".
# If another file does 'from automaton import ...', __name__ would be
# "automaton" instead, so main() would NOT run automatically.

if __name__ == "__main__":
    main()
