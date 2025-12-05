# Reservations - 50 pts

> **Category:** Misc
> **Difficulty:** Easy
> **Solves:** 218 teams
> **Status:** ✅ Solved
> **Solution:** [GitHub](https://github.com/roberttk01/Null-CTF-2025/tree/main/Misc/Reservations)

---

## Challenge Description

> *I wanted to take my inexistent girlfriend to this fancy restaurant called Windows, but they keep asking me for a key PROMPT. I don't know what to do, can you help me?*

**Attachments:** [reservation.py](./files/reservation.py)
**Instance:** `nc 34.118.61.99 10276`

---

## Reconnaissance

The challenge provides source code for a simple socket server:

```python
FLAG = os.getenv("FLAG", "nullctf{...}")
PROMPT = os.getenv("PROMPT", "bananananannaanan")

# This is missing from the .env file, but it still printed something, interesting
print(os.getenv("WINDIR"))
```

The server asks for a passphrase and compares it against the `PROMPT` environment variable.

---

## Analysis

### Key Observations

1. **Challenge title wordplay:** "Windows restaurant" + "key PROMPT" = Windows environment variables
2. **Critical hint on lines 11-12:** The comment explicitly states `WINDIR` is not in `.env` but still prints a value
3. **Implication:** The server runs on Windows and inherits system environment variables

### Vulnerability / Weakness

The `PROMPT` variable uses `os.getenv()` with a fallback:

```python
PROMPT = os.getenv("PROMPT", "bananananannaanan")
```

If `PROMPT` is not set in `.env` (like `WINDIR` isn't), it falls back to the **Windows system environment variable** rather than the default string.

On Windows, `PROMPT` is a standard environment variable that controls the command prompt display. The default value is **`$P$G`** (displays current path + `>`).

---

## Solution

### Approach

1. Recognize the Windows environment variable hint from the comment
2. Know (or research) that Windows has a built-in `PROMPT` variable
3. Send the default Windows PROMPT value: `$P$G`

### Execution

```bash
$ echo '$P$G' | nc 34.118.61.99 10276
[windows_10 | cmd.exe] Welcome good sire to our fine establishment.
Unfortunately, due to increased demand,
we have had to privatize our services.
Please enter the secret passphrase received from the environment to continue.
Thank you for your patience. Here is your flag: nullctf{why_1s_it_r3srv3d_a6230356d73b9ca7}
```

---

## Flag

```
nullctf{why_1s_it_r3srv3d_a6230356d73b9ca7}
```

---

## Lessons Learned

- Windows has several "reserved" environment variables (`PROMPT`, `WINDIR`, `COMSPEC`, etc.)
- `os.getenv()` checks system environment variables, not just `.env` files
- Comments in source code can be intentional hints in CTF challenges
- The default Windows `PROMPT` value is `$P$G`

---

## Resources

- [Windows Environment Variables](https://docs.microsoft.com/en-us/windows/deployment/usmt/usmt-recognized-environment-variables)
- [PROMPT Command Reference](https://ss64.com/nt/prompt.html)

---

## Files

| File | Description |
|------|-------------|
| [reservation.py](https://github.com/roberttk01/Null-CTF-2025/blob/main/Misc/Reservations/files/reservation.py) | Challenge source code |

---

*Tags: #nullctf2025 #misc #windows #environment-variables*