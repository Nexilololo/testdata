import os
import copy

class FiniteAutomaton:
    """Represents a finite automaton with its states, alphabet, transitions, and initial/final states."""

    def __init__(self):
        """Initializes an empty automaton structure."""
        self.alphabet = []
        self.states = set()
        self.initial = set()
        self.final = set()
        self.transitions = {}

    def add_transition(self, src, symbol, dst):
        """Registers a transition from the 'src' state to the 'dst' state reading 'symbol'."""
        key = (src, symbol)
        if key not in self.transitions:
            self.transitions[key] = set()
        self.transitions[key].add(dst)

    def get_targets(self, state, symbol):
        """Returns the set of reachable states from 'state' given 'symbol'."""
        return self.transitions.get((state, symbol), set())

def read_automaton_from_file(filename):
    """Parses a text file to extract an automaton definition and returns a FiniteAutomaton instance."""
    fa = FiniteAutomaton()
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() != '']
    idx = 0
    num_symbols = int(lines[idx])
    idx += 1
    fa.alphabet = [chr(ord('a') + i) for i in range(num_symbols)]
    num_states = int(lines[idx])
    idx += 1
    fa.states = set(range(num_states))
    parts = lines[idx].split()
    idx += 1
    num_initial = int(parts[0])
    for i in range(1, num_initial + 1):
        fa.initial.add(int(parts[i]))
    parts = lines[idx].split()
    idx += 1
    num_final = int(parts[0])
    for i in range(1, num_final + 1):
        fa.final.add(int(parts[i]))
    num_transitions = int(lines[idx])
    idx += 1
    for i in range(num_transitions):
        t = lines[idx]
        idx += 1
        j = 0
        while j < len(t) and t[j].isdigit():
            j += 1
        src = int(t[:j])
        symbol = t[j]
        dst = int(t[j + 1:])
        fa.add_transition(src, symbol, dst)
    return fa

def format_state_label(state, initial_states, final_states):
    """Generates visual markers ('E', 'S', or 'ES') to distinguish initial and final states."""
    markers = ''
    if state in initial_states:
        markers += 'E'
    if state in final_states:
        markers += 'S'
    return markers

def display_automaton(fa, title='Finite Automaton'):
    """Prints the transition table and meta-information of the automaton."""
    sorted_states = sorted(fa.states)
    sorted_alpha = list(fa.alphabet)
    print()
    print('=' * 60)
    print(f'  {title}')
    print('=' * 60)
    print(f"  Initial state(s) : {{{', '.join((str(s) for s in sorted(fa.initial)))}}}")
    print(f"  Final state(s)   : {{{', '.join((str(s) for s in sorted(fa.final)))}}}")
    print(f"  Alphabet         : {{{', '.join(fa.alphabet)}}}")
    print(f'  Number of states : {len(fa.states)}')
    print()
    header = [''] + sorted_alpha
    rows = []
    for s in sorted_states:
        marker = format_state_label(s, fa.initial, fa.final)
        if marker:
            label = f'{marker} {s}'
        else:
            label = f'  {s}'
        row = [label]
        for a in sorted_alpha:
            targets = fa.get_targets(s, a)
            if targets:
                row.append('{' + ','.join((str(t) for t in sorted(targets))) + '}')
            else:
                row.append('--')
        rows.append(row)
    col_widths = [0] * len(header)
    for c in range(len(header)):
        col_widths[c] = max(col_widths[c], len(header[c]))
    for row in rows:
        for c in range(len(row)):
            col_widths[c] = max(col_widths[c], len(row[c]))
    for c in range(len(col_widths)):
        col_widths[c] += 2
    sep = '+' + '+'.join(('-' * w for w in col_widths)) + '+'
    print(sep)
    hdr_line = '|'
    for c, h in enumerate(header):
        hdr_line += h.center(col_widths[c]) + '|'
    print(hdr_line)
    print(sep)
    for row in rows:
        r_line = '|'
        for c, cell in enumerate(row):
            r_line += cell.center(col_widths[c]) + '|'
        print(r_line)
    print(sep)
    print()

def is_deterministic(fa, verbose=True):
    """Checks whether the automaton is deterministic and optionally prints the discrepancies."""
    reasons = []
    if len(fa.initial) > 1:
        reasons.append(f"  - It has {len(fa.initial)} initial states: {{{', '.join((str(s) for s in sorted(fa.initial)))}}} (must have exactly 1).")
    for s in sorted(fa.states):
        for a in fa.alphabet:
            targets = fa.get_targets(s, a)
            if len(targets) > 1:
                reasons.append(f"  - State {s} with symbol '{a}' leads to multiple states: {{{', '.join((str(t) for t in sorted(targets)))}}}.")
    if reasons:
        if verbose:
            print('  The automaton is NOT deterministic because:')
            for r in reasons:
                print(r)
        return False
    else:
        if verbose:
            print('  The automaton IS deterministic.')
        return True

def is_complete(fa, verbose=True):
    """Checks whether the deterministic automaton is complete."""
    reasons = []
    for s in sorted(fa.states):
        for a in fa.alphabet:
            targets = fa.get_targets(s, a)
            if len(targets) == 0:
                reasons.append(f"  - State {s} has no transition for symbol '{a}'.")
    if reasons:
        if verbose:
            print('  The automaton is NOT complete because:')
            for r in reasons:
                print(r)
        return False
    else:
        if verbose:
            print('  The automaton IS complete.')
        return True

def is_standard(fa, verbose=True):
    """Checks whether the automaton is standard (single initial state, no incoming transitions)."""
    reasons = []
    if len(fa.initial) != 1:
        reasons.append(f'  - It has {len(fa.initial)} initial states (must have exactly 1).')
    else:
        i0 = next(iter(fa.initial))
        for s in fa.states:
            for a in fa.alphabet:
                targets = fa.get_targets(s, a)
                if i0 in targets:
                    reasons.append(f"  - Transition ({s}, '{a}') -> {i0} leads back to the initial state.")
    if reasons:
        if verbose:
            print('  The automaton is NOT standard because:')
            for r in reasons:
                print(r)
        return False
    else:
        if verbose:
            print('  The automaton IS standard.')
        return True

def standardize(fa):
    """Returns a newly standardized automaton equivalent to the input automaton."""
    sfa = FiniteAutomaton()
    sfa.alphabet = list(fa.alphabet)
    new_i = max(fa.states) + 1
    sfa.states = fa.states | {new_i}
    sfa.initial = {new_i}
    sfa.final = set(fa.final)
    if fa.initial & fa.final:
        sfa.final.add(new_i)
    for (s, a), targets in fa.transitions.items():
        for t in targets:
            sfa.add_transition(s, a, t)
    for old_i in fa.initial:
        for a in fa.alphabet:
            for t in fa.get_targets(old_i, a):
                sfa.add_transition(new_i, a, t)
    return sfa

def _frozenset_label(fs, separator='.'):
    return separator.join((str(s) for s in sorted(fs)))

def determinize_and_complete(fa):
    """Applies powerset construction to build a completed deterministic equivalent of the given automaton."""
    cdfa = FiniteAutomaton()
    cdfa.alphabet = list(fa.alphabet)
    start = frozenset(fa.initial)
    unmarked = [start]
    all_macro = {start}
    macro_transitions = {}
    while unmarked:
        current = unmarked.pop(0)
        for a in fa.alphabet:
            target = set()
            for s in current:
                target |= fa.get_targets(s, a)
            target = frozenset(target)
            macro_transitions[current, a] = target
            if target not in all_macro:
                all_macro.add(target)
                unmarked.append(target)
    macro_list = sorted(all_macro, key=lambda fs: (len(fs), sorted(fs)))
    state_map = {}
    for idx, ms in enumerate(macro_list):
        state_map[idx] = ms
    inv_map = {ms: idx for idx, ms in state_map.items()}
    cdfa.states = set(range(len(macro_list)))
    cdfa.initial = {inv_map[start]}
    for idx, ms in state_map.items():
        if ms & fa.final:
            cdfa.final.add(idx)
    for (ms, a), target_ms in macro_transitions.items():
        cdfa.add_transition(inv_map[ms], a, inv_map[target_ms])
    needs_sink = False
    for s in list(cdfa.states):
        for a in cdfa.alphabet:
            if not cdfa.get_targets(s, a):
                needs_sink = True
                break
        if needs_sink:
            break
    if needs_sink:
        sink = max(cdfa.states) + 1
        cdfa.states.add(sink)
        state_map[sink] = frozenset()
        for s in cdfa.states:
            for a in cdfa.alphabet:
                if not cdfa.get_targets(s, a):
                    cdfa.add_transition(s, a, sink)
    return (cdfa, state_map)

def complete(fa):
    """Completes a deterministic automaton by routing undefined transitions to a newly created sink state."""
    cdfa = FiniteAutomaton()
    cdfa.alphabet = list(fa.alphabet)
    cdfa.states = set(fa.states)
    cdfa.initial = set(fa.initial)
    cdfa.final = set(fa.final)
    for (s, a), targets in fa.transitions.items():
        for t in targets:
            cdfa.add_transition(s, a, t)
    needs_sink = False
    for s in cdfa.states:
        for a in cdfa.alphabet:
            if not cdfa.get_targets(s, a):
                needs_sink = True
                break
        if needs_sink:
            break
    sink = None
    if needs_sink:
        sink = max(cdfa.states) + 1
        cdfa.states.add(sink)
        for s in cdfa.states:
            for a in cdfa.alphabet:
                if not cdfa.get_targets(s, a):
                    cdfa.add_transition(s, a, sink)
    return (cdfa, sink)

def minimize(cdfa):
    """Applies Moore's partition refinement algorithm to compute the minimal equivalent deterministic automaton."""
    sorted_states = sorted(cdfa.states)
    finals = frozenset((s for s in sorted_states if s in cdfa.final))
    non_finals = frozenset((s for s in sorted_states if s not in cdfa.final))
    partition = []
    if non_finals:
        partition.append(non_finals)
    if finals:
        partition.append(finals)
    step = 0
    print(f'\n  --- Minimization: step {step} (initial partition) ---')
    print(f'  Partition: {_format_partition(partition)}')

    def group_of(state):
        for i, grp in enumerate(partition):
            if state in grp:
                return i
        return -1
    while True:
        new_partition = []
        for grp in partition:
            sig_map = {}
            for s in grp:
                sig = tuple((group_of(next(iter(cdfa.get_targets(s, a)))) for a in cdfa.alphabet))
                if sig not in sig_map:
                    sig_map[sig] = set()
                sig_map[sig].add(s)
            for sub in sig_map.values():
                new_partition.append(frozenset(sub))
        step += 1
        new_partition.sort(key=lambda fs: min(fs))
        print(f'\n  --- Minimization: step {step} ---')
        print(f'  Partition: {_format_partition(new_partition)}')
        print('  Transitions by group:')
        for gi, grp in enumerate(new_partition):
            rep = min(grp)
            targets = []
            for a in cdfa.alphabet:
                t = next(iter(cdfa.get_targets(rep, a)))
                for gj, grp2 in enumerate(new_partition):
                    if t in grp2:
                        targets.append(f'G{gj}')
                        break
            print(f"    G{gi}{_format_partition_group(grp)} --({', '.join(cdfa.alphabet)})--> ({', '.join(targets)})")
        if len(new_partition) == len(partition):
            if set(new_partition) == set(partition):
                print('\n  Partition is stable. Minimization complete.')
                break
        partition = new_partition
    if len(partition) == len(cdfa.states):
        print('  The automaton was already minimal.')
    mcdfa = FiniteAutomaton()
    mcdfa.alphabet = list(cdfa.alphabet)
    partition_map = {}
    for i, grp in enumerate(partition):
        partition_map[i] = grp
    mcdfa.states = set(range(len(partition)))
    old_initial = next(iter(cdfa.initial))
    for i, grp in enumerate(partition):
        if old_initial in grp:
            mcdfa.initial = {i}
            break
    for i, grp in enumerate(partition):
        if grp & cdfa.final:
            mcdfa.final.add(i)
    for i, grp in enumerate(partition):
        rep = min(grp)
        for a in cdfa.alphabet:
            t = next(iter(cdfa.get_targets(rep, a)))
            for j, grp2 in enumerate(partition):
                if t in grp2:
                    mcdfa.add_transition(i, a, j)
                    break
    return (mcdfa, partition_map)

def _format_partition(partition):
    parts = []
    for grp in partition:
        parts.append('{' + ','.join((str(s) for s in sorted(grp))) + '}')
    return '  '.join(parts)

def _format_partition_group(grp):
    return '{' + ','.join((str(s) for s in sorted(grp))) + '}'

def recognize_word(word, fa):
    """Evaluates if a given word is recognized by the complete deterministic automaton."""
    if not word:
        current = next(iter(fa.initial))
        accepted = current in fa.final
        print(f"    Empty word : start at state {current} -> {('ACCEPTED' if accepted else 'REJECTED')}")
        return accepted
    for ch in word:
        if ch not in fa.alphabet:
            print(f"    Symbol '{ch}' is not in the alphabet {{{', '.join(fa.alphabet)}}}. Word REJECTED.")
            return False
    current = next(iter(fa.initial))
    trace = [str(current)]
    for ch in word:
        targets = fa.get_targets(current, ch)
        if not targets:
            print(f"    No transition from state {current} with '{ch}'. Word REJECTED.")
            return False
        current = next(iter(targets))
        trace.append(str(current))
    accepted = current in fa.final
    print(f"    Trace: {' -> '.join(trace)}")
    print(f"    Final state {current} {('is' if accepted else 'is NOT')} a terminal state.")
    print(f"    Result: {('ACCEPTED' if accepted else 'REJECTED')}")
    return accepted

def complementary_automaton(fa):
    """Returns an automaton that recognizes the complement language of the given determinized automaton."""
    comp = FiniteAutomaton()
    comp.alphabet = list(fa.alphabet)
    comp.states = set(fa.states)
    comp.initial = set(fa.initial)
    comp.final = fa.states - fa.final
    for (s, a), targets in fa.transitions.items():
        for t in targets:
            comp.add_transition(s, a, t)
    return comp

def display_state_composition(state_map, title='State Composition'):
    print(f'\n  {title}:')
    print(f"  {'New State':<12} {'Original States'}")
    print(f"  {'-' * 12} {'-' * 30}")
    for new_s in sorted(state_map.keys()):
        orig = state_map[new_s]
        if orig:
            orig_str = '{' + ', '.join((str(s) for s in sorted(orig))) + '}'
        else:
            orig_str = '{} (sink / trash state)'
        print(f'  {new_s:<12} {orig_str}')
    print()

def list_automaton_files():
    files = [f for f in os.listdir('.') if f.endswith('.txt')]
    files.sort()
    return files

def select_automaton():
    files = list_automaton_files()
    if not files:
        print('  No .txt automaton files found in the current directory.')
        return (None, None)
    print('\n  Available automaton files:')
    for i, fname in enumerate(files):
        print(f'    {i + 1}. {fname}')
    choice = input('\n  Enter the number of the automaton to load (or filename): ').strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(files):
            filename = files[idx]
        else:
            print('  Invalid choice.')
            return (None, None)
    except ValueError:
        if choice in files:
            filename = choice
        else:
            matches = [f for f in files if choice in f]
            if len(matches) == 1:
                filename = matches[0]
            else:
                print('  File not found.')
                return (None, None)
    fa = read_automaton_from_file(filename)
    return (fa, filename)

def main():
    print('=' * 60)
    print('  EFREI P2 INT 2025/2026')
    print('  Operations on Finite Automata')
    print('=' * 60)
    while True:
        fa, filename = select_automaton()
        if fa is None:
            again = input('\n  Try again? (y/n): ').strip().lower()
            if again != 'y':
                break
            continue
        print(f'\n  Automaton loaded from: {filename}')
        display_automaton(fa, title=f'Original Automaton ({filename})')
        print('-' * 60)
        print('  PROPERTY CHECKS')
        print('-' * 60)
        det = is_deterministic(fa)
        print()
        std = is_standard(fa)
        print()
        if det:
            comp = is_complete(fa)
        else:
            comp = False
            print('  (Completeness check skipped: automaton is not deterministic.)')
        print()
        sfa = fa
        if not std:
            print('-' * 60)
            print('  STANDARDIZATION')
            print('-' * 60)
            want = input('  The automaton is not standard. Do you want to standardize it? (y/n): ').strip().lower()
            if want == 'y':
                sfa = standardize(fa)
                display_automaton(sfa, title='Standardized Automaton')
            else:
                print('  Standardization skipped.')
        else:
            print('  The automaton is already standard. No standardization needed.')
        print('\n' + '-' * 60)
        print('  DETERMINIZATION AND COMPLETION')
        print('-' * 60)
        work_fa = sfa
        det_w = is_deterministic(work_fa, verbose=False)
        comp_w = is_complete(work_fa, verbose=False) if det_w else False
        if det_w and comp_w:
            print('  The automaton is already deterministic and complete.')
            cdfa = work_fa
            cdfa_state_map = None
        elif det_w and (not comp_w):
            print('  The automaton is deterministic but NOT complete.')
            print('  Completing the automaton...')
            cdfa, sink = complete(work_fa)
            if sink is not None:
                print(f'  Added sink (trash) state: {sink}')
            display_automaton(cdfa, title='Complete Deterministic Automaton (CDFA)')
            cdfa_state_map = None
        else:
            print('  The automaton is NOT deterministic.')
            print('  Determinizing and completing the automaton...')
            cdfa, cdfa_state_map = determinize_and_complete(work_fa)
            display_automaton(cdfa, title='Complete Deterministic Automaton (CDFA)')
            display_state_composition(cdfa_state_map, title='CDFA State Composition (new state -> original states)')
        print('-' * 60)
        print('  MINIMIZATION')
        print('-' * 60)
        mcdfa, min_partition_map = minimize(cdfa)
        display_automaton(mcdfa, title='Minimal Complete Deterministic Automaton (MCDFA)')
        display_state_composition(min_partition_map, title='MCDFA State Composition (new state -> CDFA states)')
        print('-' * 60)
        print('  WORD RECOGNITION (on MCDFA)')
        print('-' * 60)
        print('  Type words to test recognition.')
        print("  Type 'end' to stop testing.\n")
        while True:
            word = input("  Enter a word (or 'end'): ").strip()
            if word.lower() == 'end':
                break
            recognize_word(word, mcdfa)
            print()
        print('-' * 60)
        print('  COMPLEMENTARY LANGUAGE')
        print('-' * 60)
        print('  Building the complementary automaton from the MCDFA...')
        comp_fa = complementary_automaton(mcdfa)
        display_automaton(comp_fa, title='Complementary Automaton')
        print('  Word recognition on the complementary automaton:')
        print("  Type words to test. Type 'end' to stop.\n")
        while True:
            word = input("  Enter a word (or 'end'): ").strip()
            if word.lower() == 'end':
                break
            recognize_word(word, comp_fa)
            print()
        print('\n' + '=' * 60)
        again = input('  Do you want to study another automaton? (y/n): ').strip().lower()
        if again != 'y':
            break
    print('\n  Goodbye!')
if __name__ == '__main__':
    main()