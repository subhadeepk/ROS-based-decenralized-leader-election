#!/usr/bin/env python3
# target_script.py

def main(n):
    print(f"Variable n: {n}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(0)