#!/usr/bin/env python3
"""
Null CTF 2025 - We Go Gambling
Category: Blockchain

Contract: [TODO: Contract address or name]
Network: [TODO: Testnet/mainnet details]
Goal: [TODO: Drain funds, win game, etc.]
"""

from web3 import Web3
import requests
import re
import sys

# =============================================================================
# CONFIGURATION - Update from challenge info
# =============================================================================
INSTANCE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://public.ctf.r0devnull.team:3011"

# These get populated at runtime from instance
RPC_URL = http://public.ctf.r0devnull.team:3011/877453eb-92e8-4ce5-beb4-03249a37b7b7
PRIVATE_KEY = 7522c1d95510b248799b735cd28172920ebab5b20986f81a74da590b2df979e7
SETUP_ADDRESS = 0x0E9c8742bf0576a906f5993db38B4d16A1961E63
CASINO_ADDRESS = 0xbD39a090F511AE7682277f91bA0eC79eD9dCB3F6
TOKEN_ADDRESS = None

# =============================================================================
# CONTRACT ANALYSIS - Document findings
# =============================================================================
"""
Contract source/bytecode analysis:


State variables:


Key functions:
-

Access control:
-

Potential vulnerabilities:
- [ ] Reentrancy
- [ ] Integer overflow/underflow
- [ ] Access control issues
- [ ] Randomness manipulation
- [ ] Front-running susceptibility
- [ ] Unchecked return values
- [ ] Denial of service vectors
"""

# =============================================================================
# INSTANCE SETUP - Fetch connection details from challenge server
# =============================================================================

def fetch_instance_info(instance_url: str) -> dict:
    """
    Fetch connection details from the challenge instance.

    Returns dict with: rpc_url, private_key, setup_address, etc.
    """
    global RPC_URL, PRIVATE_KEY, SETUP_ADDRESS, CASINO_ADDRESS, TOKEN_ADDRESS

    print(f"[*] Fetching instance info from: {instance_url}")

    try:
        resp = requests.get(instance_url)
        resp.raise_for_status()
        content = resp.text

        print(f"[*] Response received ({len(content)} bytes)")
        print("-" * 60)
        print(content[:2000])  # Print first 2000 chars for inspection
        print("-" * 60)

        # Try JSON first
        try:
            data = resp.json()
            RPC_URL = data.get('rpc') or data.get('rpc_url') or data.get('RPC')
            PRIVATE_KEY = data.get('private_key') or data.get('privateKey') or data.get('key')
            SETUP_ADDRESS = data.get('setup') or data.get('setup_address') or data.get('Setup')
            return data
        except:
            pass

        # Parse text/HTML for common patterns
        # Look for Ethereum addresses (0x + 40 hex chars)
        addresses = re.findall(r'0x[a-fA-F0-9]{40}', content)
        # Look for private keys (0x + 64 hex chars)
        privkeys = re.findall(r'0x[a-fA-F0-9]{64}', content)
        # Look for RPC URLs
        rpc_urls = re.findall(r'https?://[^\s<>"\']+(?::\d+)?(?:/rpc)?', content)

        print(f"[*] Found {len(addresses)} addresses: {addresses}")
        print(f"[*] Found {len(privkeys)} private keys: {privkeys[:1]}...")  # Don't leak full key
        print(f"[*] Found {len(rpc_urls)} potential RPC URLs: {rpc_urls}")

        # You'll need to manually assign based on output:
        # RPC_URL = rpc_urls[0] if rpc_urls else None
        # PRIVATE_KEY = privkeys[0] if privkeys else None
        # SETUP_ADDRESS = addresses[0] if addresses else None

        return {
            'addresses': addresses,
            'private_keys': privkeys,
            'rpc_urls': rpc_urls,
            'raw': content
        }

    except requests.RequestException as e:
        print(f"[!] Failed to fetch instance: {e}")
        return {}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def connect_web3(rpc_url: str) -> Web3:
    """Establish Web3 connection to RPC endpoint."""
    connection = None
    try:
        connection = Web3(Web3.HTTPProvider(rpc_url))
        private_key = connection.eth.account.privateKeyToAccount(PRIVATE_KEY)
        connection.eth.account.enable_unaudited_hdwallet_features()
        connection.eth.defaultAccount = private_key.address
    except:
        pass
    return connection 
    

def get_contract(w3: Web3, address: str, abi: list):
    """Load contract instance from address and ABI."""
    # TODO: Implement contract loading
    pass

def get_account(w3: Web3, private_key: str):
    """Get account from private key for signing transactions."""
    # TODO: Implement account setup
    pass

# =============================================================================
# PHASE 1: RECONNAISSANCE
# =============================================================================

def analyze_contract_state(w3: Web3, contract) -> dict:
    """
    Read contract state variables.

    Questions to answer:
    - What is the contract balance?
    - Who is the owner?
    - What are the game parameters?
    - Any interesting state we can leverage?
    """
    # TODO: Implement state analysis
    pass

def analyze_transactions(w3: Web3, contract_address: str) -> list:
    """
    Analyze past transactions to understand contract behavior.

    Techniques:
    - Check recent transactions
    - Look for patterns in successful/failed calls
    - Identify function signatures used
    """
    # TODO: Implement transaction analysis
    pass

# =============================================================================
# PHASE 2: VULNERABILITY IDENTIFICATION
# =============================================================================

def check_reentrancy(contract_source: str) -> bool:
    """
    Check for reentrancy vulnerabilities.

    Indicators:
    - External calls before state updates
    - Missing reentrancy guards
    - Callbacks to untrusted contracts
    """
    # TODO: Implement check
    pass

def check_randomness(contract_source: str) -> bool:
    """
    Check for weak randomness.

    Common weak sources:
    - block.timestamp
    - block.number
    - blockhash
    - msg.sender as seed
    """
    # TODO: Implement check
    pass

def check_integer_issues(contract_source: str) -> bool:
    """
    Check for integer overflow/underflow.

    Look for:
    - Unchecked arithmetic (pre-Solidity 0.8)
    - Missing SafeMath usage
    - Type casting issues
    """
    # TODO: Implement check
    pass

def check_access_control(contract_source: str) -> bool:
    """
    Check for access control issues.

    Look for:
    - Missing onlyOwner modifiers
    - tx.origin vs msg.sender confusion
    - Unprotected initialization
    """
    # TODO: Implement check
    pass

# =============================================================================
# PHASE 3: EXPLOIT DEVELOPMENT
# =============================================================================

def deploy_attack_contract(w3: Web3, account) -> str:
    """
    Deploy malicious contract for attack.

    Attack contract should:
    - TODO: Define attack contract logic
    """
    # TODO: Implement attack contract deployment
    pass

def execute_exploit(w3: Web3, contract, account) -> str:
    """
    Execute the exploit.

    Steps:
    1.
    2.
    3.

    Returns: flag or result
    """
    # TODO: Implement exploit
    pass

# =============================================================================
# PHASE 4: FLAG RETRIEVAL
# =============================================================================

def get_flag(w3: Web3, contract) -> str:
    """
    Retrieve the flag after successful exploit.

    Methods:
    - Call flag() function
    - Check emitted events
    - Read storage slot
    """
    # TODO: Implement flag retrieval
    pass

# =============================================================================
# MAIN
# =============================================================================

def main():
    # Phase 0: Fetch instance info
    info = fetch_instance_info(INSTANCE_URL)

    if not RPC_URL:
        print("[!] Could not auto-detect RPC URL. Check output above and set manually.")
        print("[*] Exiting after recon phase. Update script with extracted values.")
        return

    print(f"[*] Connecting to RPC: {RPC_URL}")

    # Phase 1: Setup
    # w3 = connect_web3(RPC_URL)
    # account = get_account(w3, PRIVATE_KEY)

    # Phase 2: Recon
    # state = analyze_contract_state(w3, contract)
    # print(f"[*] Contract state: {state}")

    # Phase 3: Exploit
    # result = execute_exploit(w3, contract, account)
    # print(f"[+] Exploit result: {result}")

    # Phase 4: Flag
    # flag = get_flag(w3, contract)
    # print(f"[+] Flag: {flag}")

if __name__ == "__main__":
    main()
