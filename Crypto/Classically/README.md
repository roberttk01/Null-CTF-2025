# Classically - 50 pts

> **Category:** Crypto
> **Difficulty:** Easy
> **Solves:** 252 teams
> **Status:** ✅ Solved

---

## Challenge Description

> *TODO: Add official CTFd description*

**Attachments:** [classically.zip](files/classically.zip)
**Instance:** N/A (offline challenge)

---

## Reconnaissance

Challenge files:
- `main.py` - Encryption script
- `M.py` - 64x64 matrix definition

```python
# main.py key observations:
# - Flag is 64 bytes: ctf{...}
# - Matrix M is 64x64
# - result[i] = sum(M[i][j] * flag[j]) % 0x10001
# - 0x10001 = 65537 (prime!)
```

---

## Analysis

### Key Observations

1. **Linear system over finite field**: `result = M * flag (mod 65537)`
2. **65537 is prime** - so we're working in GF(65537), a field
3. **Matrix is square (64x64)** - if invertible, unique solution exists

### Vulnerability / Weakness

The system is deterministic and invertible. Given:
- `result` (64-element vector)
- `M` (64x64 matrix)
- `mod = 65537` (prime)

Solve: `flag = M^(-1) * result (mod 65537)`

---

## Solution

### Approach

1. Parse the matrix M and result vector from challenge files
2. Construct matrix over GF(65537)
3. Compute matrix inverse
4. Multiply inverse by result vector
5. Convert resulting integers to ASCII bytes

### Exploit / Script

```python
# See Classically_Solution.py
```

### Execution

```bash
$ python3 Classically_Solution.py
[*] Classically - Linear System Solver
[*] Modulus: 65537 (0x10001)
[*] Result vector length: 64
[*] Loading matrix...
[*] Matrix size: 64x64
[*] Computing modular inverse and solving...
[+] Flag: ctf{s0lve_th3_equ4t10n5_t0_f1nd_fl4g_h3r3_w4s_easy_en0ugh_NO???}
```

---

## Flag

```
ctf{s0lve_th3_equ4t10n5_t0_f1nd_fl4g_h3r3_w4s_easy_en0ugh_NO???}
```

---

## Lessons Learned

- Linear systems mod prime p can be solved with standard linear algebra in GF(p)
- `sympy.Matrix.inv_mod(p)` computes modular matrix inverse - numpy can't do this
- 65537 (0x10001) is a common prime in crypto (Fermat prime F4, RSA exponent)

---

## Resources

- [SageMath Matrix Documentation](https://doc.sagemath.org/html/en/reference/matrices/sage/matrix/constructor.html)

---

## Files

| File | Description |
|------|-------------|
| [Classically_Solution.py](Classically_Solution.py) | Solution script |
| [files/main.py](files/main.py) | Challenge encryption script |
| [files/M.py](files/M.py) | 64x64 matrix definition |

---

*Tags: #nullctf2025 #crypto #linear-algebra #matrix-inversion #finite-field*
