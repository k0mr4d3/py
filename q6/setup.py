# gonna end up on r/programmerhorror

import sys
import os
import datetime

home_path = ""
op = 0 # -il, -li = 0; -i = 1; -vl, -lv = 2; -v = 3

def is_arg2_valid():
    if sys.argv[2][0] != "-":
        return False
    else:
        known_args = ["li", "il", "i", "vl", "lv", "v"]
        try:
            known_args.index(sys.argv[2][1:])
            return True
        except ValueError:
            return False
                  
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Insufficient arguments")
    else:
        if sys.argv[1][0] != "/" or sys.argv[1][len(sys.argv[1]) - 1] != "/":
            sys.stderr.write("Invalid master directory")
        else:
            home_path = sys.argv[1]
            if len(sys.argv) == 2:
                pass
            else:
                if is_arg2_valid() == False:
                    sys.stderr.write("Invalid flag")
                else:
                    if str(sys.argv[2]).find("-il") != -1 or str(sys.argv[2]).find("-il") != -1:
                        op = 0
                    elif str(sys.argv[2]).find("-i") != -1:
                        op = 1
                    elif str(sys.argv[2]).find("-vl") != -1 or str(sys.argv[2]).find("-lv") != -1:
                        op = 2
                    elif str(sys.argv[2]).find("-v") != -1:
                        op = 3

    print(home_path)
    print(op)