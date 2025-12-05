# double_it_and_give_it_to_the_next_person - 50 pts

> **Category:** Crypto
> **Difficulty:** Medium
> **Solves:** 154 teams
> **Status:** ✅ Solved

---

## Challenge Description

> *In romanian folklore, there is a tradition called "dubleza si da mai departe" (double it and give it to the next person). This challenge is inspired by that tradition, but with a cryptographic twist.*

**Attachments:** [chal.sage](./files/chal.sage) | [output.txt](./files/output.txt)

---

## Reconnaissance

Challenge provides a SageMath script that:
1. Uses **P-256** (NIST standard elliptic curve)
2. Generates two secret keys: `key1`, `key2`
3. For 2 iterations: picks random point P, computes Q = 2*P (point doubling)
4. Obfuscates coordinates: `P.x = a*key1 + b`, `Q.x = c*key2 + d`
5. Flag = `key1 XOR key2`

```python
P.x = 101391...713 * key1 + 110183...293
Q.x = 43935...569 * key2 + 13245...655
P.x = 113113...423 * key1 + 3292...631
Q.x = 90189...921 * key2 + 93980...289
```

---

## Analysis

### Key Observations

1. **Point doubling constraint:** Q = 2P creates algebraic relationship between P.x and Q.x
2. **Linear obfuscation:** Both P.x and Q.x are linear in their respective keys
3. **Two iterations:** Gives 2 polynomial equations in 2 unknowns

### Point Doubling Formula

For P = (x, y) on curve y² = x³ + ax + b, the doubled point Q = 2P has:
```
λ = (3x² + a) / (2y)
Q.x = λ² - 2x
```

Eliminating y (since y² = x³ + ax + b):
```
(Q.x + 2·P.x) · 4·(P.x³ + a·P.x + b) = (3·P.x² + a)²
```

### Vulnerability

Substituting `P.x = a_i*key1 + b_i` and `Q.x = c_i*key2 + d_i` into the doubling formula gives a polynomial equation in key1, key2.

With 2 iterations → 2 polynomial equations → solvable via **Gröbner basis**.

---

## Solution

### Approach

1. Build polynomial constraints from point doubling formula
2. Compute Gröbner basis with lex ordering (key1 > key2)
3. Extract univariate polynomial in key2
4. Find roots in GF(p)
5. Back-substitute to find key1
6. XOR keys for flag

### Exploit / Script

```python
# SageMath - run at https://sagecell.sagemath.org/

p = 2^256 - 2^224 + 2^192 + 2^96 - 1
curve_a = -3
curve_b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b

a1 = 101391067652419278504279072061964396163420598174591672104811496061093042423713
b1 = 110183945624921546387413554986656742713737778649772602611818367446708850272293
c1 = 43935985468030112938420167350551592897480789520688041577831275174910738854569
d1 = 13245902077735905939963311540878792271896625592735457462639747889134751588655

a2 = 113113920295449343615508981422751944711310245958533784150505930220126533492423
b2 = 3292039546575820821367398987680176504505470559384412397685623175088154966631
c2 = 90189751456536603500768763858048652235807590023038279530146107092251468907921
d2 = 93980984745553841375952018332854663310402153214300203815947697055365029221289

R.<key1, key2> = PolynomialRing(GF(p), order='lex')

def constraint(ai, bi, ci, di):
    Px = ai * key1 + bi
    Qx = ci * key2 + di
    return (Qx + 2*Px) * 4 * (Px^3 + curve_a*Px + curve_b) - (3*Px^2 + curve_a)^2

I = ideal(constraint(a1,b1,c1,d1), constraint(a2,b2,c2,d2))
G = I.groebner_basis()

# Find univariate polynomial in key2
for g in G:
    if g.degree(key1) == 0:
        S.<x> = PolynomialRing(GF(p))
        uni = S(g.subs(key2=x))
        roots = uni.roots()
        for r, mult in roots:
            k2 = int(r)
            for g2 in G:
                if g2.degree(key1) == 1:
                    eq = g2.subs(key2=k2)
                    k1 = int(-eq.constant_coefficient() / eq.coefficient(key1))
                    print(f"key1 = {k1}")
                    print(f"key2 = {k2}")
                    print(f"FLAG: nullctf{{{k1 ^^ k2:064x}}}")
                    break
        break
```

### Execution

```
Computing Groebner basis...
Got 2 polynomials
Found univariate in key2, degree 7
Found 1 root(s)

key1 = ...
key2 = ...
FLAG: nullctf{25b6b8151d54b7f9e5fc3181e1d5b5a97464d019dde57aca90df349a8c951a02}
```

---

## Flag

```
nullctf{25b6b8151d54b7f9e5fc3181e1d5b5a97464d019dde57aca90df349a8c951a02}
```

---

## Lessons Learned

- **Point doubling formula** can be rearranged to eliminate y, creating polynomial in just x-coordinates
- **Gröbner basis** with lex ordering produces triangular system - last polynomial is univariate
- **SageMath** handles large prime field polynomial algebra much better than sympy
- `I.variety()` can fail on large primes; manual root finding via `.roots()` on univariate is more robust

---

## Resources

- [Elliptic Curve Point Doubling](https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication#Point_doubling)
- [Gröbner Basis](https://en.wikipedia.org/wiki/Gr%C3%B6bner_basis)
- [SageMathCell](https://sagecell.sagemath.org/) - Online Sage interpreter

---

## Files

| File | Description |
|------|-------------|
| [chal.sage](./files/chal.sage) | Challenge encryption script |
| [output.txt](./files/output.txt) | Obfuscated coordinates |
| [solve_sagecell.sage](./solve_sagecell.sage) | Solution script for SageMathCell |

---

*Tags: #nullctf2025 #crypto #elliptic-curve #p256 #grobner-basis #point-doubling*