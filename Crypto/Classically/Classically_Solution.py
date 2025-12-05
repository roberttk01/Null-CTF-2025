#!/usr/bin/env python3
"""
Null CTF 2025 - Classically
Category: Crypto

Cipher/Algorithm: Linear system over GF(65537)
Goal: Recover flag from result = M * flag (mod 65537)
"""

from sympy import Matrix

# Result vector from main.py output
RESULT = [29839, 662, 50523, 15906, 32667, 25159, 5172, 11685, 5618, 62174,
          54405, 34902, 12259, 59526, 12299, 37286, 6055, 16813, 42488, 40708,
          7662, 24263, 24047, 55429, 64420, 18167, 36330, 18325, 61471, 559,
          32085, 23807, 26543, 26886, 24249, 45980, 23360, 15196, 42894, 33054,
          22073, 23786, 63308, 44883, 60088, 38633, 54798, 42893, 29049, 25567,
          33563, 49913, 63714, 51666, 60112, 19656, 13133, 11756, 34277, 55622,
          14539, 54580, 48536, 1337]

MOD = 0x10001  # 65537


def load_matrix():
    """Load the 64x64 matrix from M.py."""
    namespace = {}
    with open("files/M.py", "r") as f:
        exec(f.read(), namespace)
    return namespace['M']


def solve_system(M, result, mod):
    """Solve the linear system using sympy modular inverse."""
    M_sym = Matrix(M)
    M_inv = M_sym.inv_mod(mod)
    result_vec = Matrix(result)
    flag_vec = M_inv * result_vec
    flag_vec = flag_vec.applyfunc(lambda x: x % mod)
    return bytes([int(x) for x in flag_vec])


def main():
    print("[*] Classically - Linear System Solver")
    print(f"[*] Modulus: {MOD} (0x{MOD:x})")
    print(f"[*] Result vector length: {len(RESULT)}")

    # 1. Load matrix
    print("[*] Loading matrix...")
    M = load_matrix()
    print(f"[*] Matrix size: {len(M)}x{len(M[0])}")

    # 2. Solve system
    print("[*] Computing modular inverse and solving...")
    flag = solve_system(M, RESULT, MOD)

    # 3. Print flag
    print(f"[+] Flag: {flag.decode()}")


if __name__ == "__main__":
    main()