import sys
import os
import glob
import traceback

sys.path.insert(0, os.path.dirname(__file__))

from automaton import (
    read_automaton_from_file, display_automaton,
    is_deterministic, is_complete, is_standard,
    standardize, determinize_and_complete, complete,
    minimize, recognize_word, complementary_automaton,
    display_state_composition
)

def process_all_automata():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    fa_files = sorted(glob.glob("FA-*.txt"))
    
    error_file = "test.txt"
    # Create or clear the test.txt file
    with open(error_file, "w", encoding="utf-8") as ef:
        ef.write("Error Log for Automata Tests\n")
        ef.write("="*70 + "\n")
        
    for fa_file in fa_files:
        base_name = os.path.splitext(fa_file)[0]
        output_file = f"output_{base_name}.txt"
        
        original_stdout = sys.stdout
        try:
            with open(output_file, "w", encoding="utf-8") as out_f:
                sys.stdout = out_f
                
                print("=" * 70)
                print(f"PROCESSING: {fa_file}")
                print("=" * 70)
                
                fa = read_automaton_from_file(fa_file)
                display_automaton(fa, title=f"Original FA ({fa_file})")
                
                print("\n--- Checking Properties ---")
                is_deterministic(fa)
                is_standard(fa)
                is_complete(fa)
                
                print("\n--- Standardizing ---")
                sfa = standardize(fa)
                display_automaton(sfa, title="Standardized FA")
                
                print("\n--- Determinizing & Completing ---")
                cdfa, sm = determinize_and_complete(sfa)
                display_automaton(cdfa, title="Complete Deterministic FA")
                display_state_composition(sm)
                
                print("\n--- Minimizing ---")
                mcdfa, mm = minimize(cdfa)
                display_automaton(mcdfa, title="Minimal CDFA")
                display_state_composition(mm)
                
        except Exception as e:
            with open(error_file, "a", encoding="utf-8") as ef:
                ef.write(f"\n[{fa_file}] ERROR:\n")
                ef.write(f"{str(e)}\n")
                ef.write(traceback.format_exc())
                ef.write("-" * 40 + "\n")
        finally:
            sys.stdout = original_stdout
            
if __name__ == "__main__":
    process_all_automata()
    print("Completed testing all FA files. Check output_FA-*.txt and test.txt for results.")
