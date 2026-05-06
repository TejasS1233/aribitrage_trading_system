# Arbitrage Trading — Complete Concept Encyclopedia

> A comprehensive textbook covering arbitrage trading across centralized exchanges, decentralized exchanges, prediction markets, and blockchain-native MEV strategies. Compiled from 13 open-source repositories.

---

## Table of Contents

- [Chapter 1: Blockchain & Token Fundamentals](#chapter-1-blockchain--token-fundamentals)
  - [1.1 Tokens](#11-tokens)
  - [1.2 Wrapped Tokens](#12-wrapped-tokens)
  - [1.3 Wallets and Addresses](#13-wallets-and-addresses)
  - [1.4 Program Derived Addresses (PDAs)](#14-program-derived-addresses-pdas)
  - [1.5 Associated Token Accounts (ATAs)](#15-associated-token-accounts-atas)
  - [1.6 Gas, Lamports, and Compute Units](#16-gas-lamports-and-compute-units)
  - [1.7 Transactions](#17-transactions)
  - [1.8 Atomic Transactions](#18-atomic-transactions)
  - [1.9 Versioned Transactions and Address Lookup Tables](#19-versioned-transactions-and-address-lookup-tables)
  - [1.10 Smart Contracts and On-Chain Programs](#110-smart-contracts-and-on-chain-programs)
  - [1.11 Token Decimals and Precision](#111-token-decimals-and-precision)
  - [1.12 ERC-20 Approvals](#112-erc-20-approvals)
  - [1.13 Signature Types (EOA, POLY_PROXY, Gnosis Safe)](#113-signature-types-eoa-poly_proxy-gnosis-safe)
  - [Key Takeaway](#key-takeaway)
- [Chapter 2: Exchange Architecture](#chapter-2-exchange-architecture)
  - [2.1 Centralized Exchanges (CEXs)](#21-centralized-exchanges-cexs)
  - [2.2 Decentralized Exchanges (DEXs)](#22-decentralized-exchanges-dexs)
  - [2.3 Order Books (CLOB)](#23-order-books-clob)
  - [2.4 AMMs (Automated Market Makers)](#24-amms-automated-market-makers)
  - [2.5 Liquidity Pools](#25-liquidity-pools)
  - [2.6 DEX Aggregators](#26-dex-aggregators)
  - [2.7 Factory Pattern and Pair Discovery](#27-factory-pattern-and-pair-discovery)
  - [2.8 Spread, Bid, Ask, and Mid Price](#28-spread-bid-ask-and-mid-price)
  - [2.9 Order Book Depth and Walking the Book](#29-order-book-depth-and-walking-the-book)
  - [2.10 Base and Quote Assets](#210-base-and-quote-assets)
  - [2.11 Prediction Markets (Polymarket)](#211-prediction-markets-polymarket)
  - [Key Takeaway](#key-takeaway-1)
- [Chapter 3: AMM Mathematics](#chapter-3-amm-mathematics)
  - [3.1 Constant Product Formula (x * y = k)](#31-constant-product-formula-x--y--k)
  - [3.2 getAmountOut and getAmountIn](#32-getamountout-and-getamountin)
  - [3.3 Swap Fees](#33-swap-fees)
  - [3.4 Price Impact and Slippage](#34-price-impact-and-slippage)
  - [3.5 StableSwap (Curve.fi)](#35-stableswap-curvefi)
  - [3.6 Amplification Parameter (A)](#36-amplification-parameter-a)
  - [3.7 Newton's Method for Square Roots](#37-newtons-method-for-square-roots)
  - [3.8 Virtual Reserves and Virtual Pools](#38-virtual-reserves-and-virtual-pools)
  - [3.9 Optimal Input Amount](#39-optimal-input-amount)
  - [3.10 Optimal Borrow Amount for Arbitrage](#310-optimal-borrow-amount-for-arbitrage)
  - [3.11 Fee Calculation with Fractions](#311-fee-calculation-with-fractions)
  - [3.12 Decimal Precision](#312-decimal-precision)
  - [Key Takeaway](#key-takeaway-2)
- [Chapter 4: Arbitrage Strategies](#chapter-4-arbitrage-strategies)
  - [4.1 Cross-Exchange Arbitrage](#41-cross-exchange-arbitrage)
  - [4.2 Triangular Arbitrage](#42-triangular-arbitrage)
  - [4.3 Circular Arbitrage](#43-circular-arbitrage)
  - [4.4 Inter-Exchange vs Intra-Exchange Arbitrage](#44-inter-exchange-vs-intra-exchange-arbitrage)
  - [4.5 Flash Loan Arbitrage](#45-flash-loan-arbitrage)
  - [4.6 Cross-Time Arbitrage](#46-cross-time-arbitrage)
  - [4.7 Par Relationship Arbitrage (Prediction Markets)](#47-par-relationship-arbitrage-prediction-markets)
  - [4.8 PingPong Strategy](#48-pingpong-strategy)
  - [4.9 Bundle Execution](#49-bundle-execution)
  - [4.10 Leg Sequencing (Staggered Entry)](#410-leg-sequencing-staggered-entry)
  - [4.11 Swing Detection](#411-swing-detection)
  - [4.12 Halving Strategy](#412-halving-strategy)
  - [4.13 Trade Size Strategy](#413-trade-size-strategy)
  - [4.14 Profit Thresholds](#414-profit-thresholds)
  - [Key Takeaway](#key-takeaway-3)
- [Chapter 5: Graph Theory for Arbitrage](#chapter-5-graph-theory-for-arbitrage)
  - [5.1 Directed Graphs](#51-directed-graphs)
  - [5.2 Multi-Directed Graphs](#52-multi-directed-graphs)
  - [5.3 Nodes and Edges](#53-nodes-and-edges)
  - [5.4 Edge Weights and the Negative Log Transform](#54-edge-weights-and-the-negative-log-transform)
  - [5.5 Negative Weight Cycles](#55-negative-weight-cycles)
  - [5.6 Bellman-Ford Algorithm](#56-bellman-ford-algorithm)
  - [5.7 Edge Relaxation](#57-edge-relaxation)
  - [5.8 DFS (Depth-First Search)](#58-dfs-depth-first-search)
  - [5.9 Brute Force Search with Pruning](#59-brute-force-search-with-pruning)
  - [5.10 Path Retracing](#510-path-retracing)
  - [5.11 Triangle Discovery](#511-triangle-discovery)
  - [Key Takeaway](#key-takeaway-4)
- [Chapter 6: Smart Contract Execution](#chapter-6-smart-contract-execution)
  - [6.1 Flash Loans](#61-flash-loans)
  - [6.2 Flash Swaps](#62-flash-swaps)
  - [6.3 Flash Swap Callback (uniswapV2Call)](#63-flash-swap-callback-uniswapv2call)
  - [6.4 Profit-or-Revert](#64-profit-or-revert)
  - [6.5 CPI (Cross-Program Invocation)](#65-cpi-cross-program-invocation)
  - [6.6 SwapState PDA](#66-swapstate-pda)
  - [6.7 The basic_pool_swap! Macro](#67-the-basic_pool_swap-macro)
  - [6.8 MoneyPrinter.sol](#68-moneyprintersol)
  - [6.9 Bundle Executor Contract](#69-bundle-executor-contract)
  - [6.10 Debt Repayment in Base Token](#610-debt-repayment-in-base-token)
  - [6.11 Owner-Only Functions and Access Control](#611-owner-only-functions-and-access-control)
  - [6.12 EnumerableSet for Base Tokens](#612-enumerableset-for-base-tokens)
  - [6.13 Fallback Function for Multi-DEX Support](#613-fallback-function-for-multi-dex-support)
  - [6.14 On-Chain Profit Validation](#614-on-chain-profit-validation)
  - [Key Takeaway](#key-takeaway-5)
- [Chapter 7: MEV & Priority Execution](#chapter-7-mev--priority-execution)
  - [7.1 MEV (Maximal Extractable Value)](#71-mev-maximal-extractable-value)
  - [7.2 Searchers](#72-searchers)
  - [7.3 Flashbots](#73-flashbots)
  - [7.4 Flashbots Bundles and Relay](#74-flashbots-bundles-and-relay)
  - [7.5 Jito Bundles](#75-jito-bundles)
  - [7.6 Jito Block Engine](#76-jito-block-engine)
  - [7.7 Jito Tip](#77-jito-tip)
  - [7.8 Backrunning](#78-backrunning)
  - [7.9 Sandwich Attacks](#79-sandwich-attacks)
  - [7.10 Token Sniping](#710-token-sniping)
  - [7.11 Private Mempool](#711-private-mempool)
  - [7.12 Miner Tip and Coinbase Transfer](#712-miner-tip-and-coinbase-transfer)
  - [7.13 No Cost on Failure](#713-no-cost-on-failure)
  - [7.14 Priority Fees and skip_preflight](#714-priority-fees-and-skip_preflight)
  - [7.15 Target Block and Reputation](#715-target-block-and-reputation)
  - [Key Takeaway](#key-takeaway-6)
- [Chapter 8: Risk Management](#chapter-8-risk-management)
  - [8.1 Position Limits and Max Exposure](#81-position-limits-and-max-exposure)
  - [8.2 Single Leg Recovery](#82-single-leg-recovery)
  - [8.3 Slippage Protection](#83-slippage-protection)
  - [8.4 Profit Sanity Checks](#84-profit-sanity-checks)
  - [8.5 Trade Cooldown](#85-trade-cooldown)
  - [8.6 Simulation Before Execution](#86-simulation-before-execution)
  - [8.7 Data Freshness and Expiration](#87-data-freshness-and-expiration)
  - [8.8 Blacklist](#88-blacklist)
  - [8.9 Broker Stability Tracker](#89-broker-stability-tracker)
  - [8.10 Error Count Failsafe](#810-error-count-failsafe)
  - [8.11 Exit Net Profit Ratio](#811-exit-net-profit-ratio)
  - [8.12 Execution Cap](#812-execution-cap)
  - [8.13 No Trade Periods](#813-no-trade-periods)
  - [8.14 Gas Estimation](#814-gas-estimation)
  - [Key Takeaway](#key-takeaway-7)
- [Chapter 9: Data & Infrastructure](#chapter-9-data--infrastructure)
  - [9.1 RPC (Remote Procedure Call)](#91-rpc-remote-procedure-call)
  - [9.2 WebSocket Streaming](#92-websocket-streaming)
  - [9.3 Batch RPC Queries](#93-batch-rpc-queries)
  - [9.4 Rate Limiting and Key Rotation](#94-rate-limiting-and-key-rotation)
  - [9.5 Concurrent Data Fetching](#95-concurrent-data-fetching)
  - [9.6 CCXT (Unified Exchange API)](#96-ccxt-unified-exchange-api)
  - [9.7 Sync Events (Incremental Updates)](#97-sync-events-incremental-updates)
  - [9.8 Price Merge Size and Quantization](#98-price-merge-size-and-quantization)
  - [9.9 Hardhat Network Forking and Mainnet Fork Testing](#99-hardhat-network-forking-and-mainnet-fork-testing)
  - [9.10 ChronoDB (Time-Series Storage)](#910-chronodb-time-series-storage)
  - [9.11 ZeroMQ (IPC Messaging)](#911-zeromq-ipc-messaging)
  - [9.12 Secret Enclave (Encrypted Storage)](#912-secret-enclave-encrypted-storage)
  - [9.13 Base58 Encoding](#913-base58-encoding)
  - [Key Takeaway](#key-takeaway-8)
- [Chapter 10: Trading Systems Architecture](#chapter-10-trading-systems-architecture)
  - [10.1 The Main Loop (Event Loop)](#101-the-main-loop-event-loop)
  - [10.2 Observer Pattern (Event-Driven Architecture)](#102-observer-pattern-event-driven-architecture)
  - [10.3 Template Method Pattern](#103-template-method-pattern)
  - [10.4 Strategy Pattern (Swappable Algorithms)](#104-strategy-pattern-swappable-algorithms)
  - [10.5 Factory Pattern](#105-factory-pattern)
  - [10.6 Trait-Based Polymorphism](#106-trait-based-polymorphism)
  - [10.7 Borg Pattern (Shared State)](#107-borg-pattern-shared-state)
  - [10.8 Dependency Injection](#108-dependency-injection)
  - [10.9 Supervisor Pattern](#109-supervisor-pattern)
  - [10.10 Async/Await and the Event Loop](#110-asyncawait-and-the-event-loop)
  - [10.11 Concurrent State Management](#111-concurrent-state-management)
  - [10.12 Metrics and Monitoring](#112-metrics-and-monitoring)
  - [10.13 Typed Configuration](#113-typed-configuration)
  - [10.14 Custom Error Types](#114-custom-error-types)
  - [10.15 Relayer Pattern (Gasless Transactions)](#115-relayer-pattern-gasless-transactions)
  - [10.16 Analytics Plugin](#116-analytics-plugin)
  - [10.17 Transport Layer (Logging)](#117-transport-layer-logging)
  - [Key Takeaway](#key-takeaway-9)
- [Appendix: Source Repositories](#appendix-source-repositories)

---

## Chapter 1: Blockchain & Token Fundamentals

Before you can understand arbitrage, you need to understand the building blocks: tokens, wallets, transactions, and gas. This chapter covers the foundational concepts shared across all blockchain-based arbitrage systems.

---

### 1.1 Tokens

A **token** is a digital asset on a blockchain. Think of it like a digital version of a casino chip — it represents value and can be traded, but it only exists within the blockchain's ecosystem.

**Types of tokens:**

| Token | Blockchain | Decimals | What It Is |
|-------|-----------|----------|------------|
| SOL | Solana | 9 | Native token (like cash) |
| WSOL | Solana | 9 | Wrapped SOL (like a casino chip for SOL) |
| USDC | Solana/Ethereum | 6 | Dollar-pegged stablecoin |
| ETH | Ethereum | 18 | Native token |
| WETH | Ethereum | 18 | Wrapped ETH |
| BNB | BSC | 18 | Native token |
| WBNB | BSC | 18 | Wrapped BNB |
| pUSD | Polygon | 6 | Polymarket's internal stablecoin |

> *Source: Solana-Arbitrage-Bot, amm-arbitrageur, solana-arbitrage-bot-wsol, polymarket*

---

### 1.2 Wrapped Tokens

Native blockchain tokens (SOL, ETH, BNB) can't be used directly in smart contracts. They must be **wrapped** into a token standard (SPL on Solana, ERC-20 on Ethereum).

**Analogy:** Imagine SOL is cash and WSOL is a prepaid debit card. You deposit cash to get the card, use the card for transactions, then withdraw cash when done.

```
Native SOL  →  wrap  →  WSOL (SPL token)  →  use in DEX  →  unwrap  →  Native SOL
```

**Why wrapping matters for arbitrage:** DEXs only work with standard token formats. To swap SOL for USDC, you first need WSOL.

> *Source: solana-arbitrage-bot-wsol, amm-arbitrageur*

---

### 1.3 Wallets and Addresses

A **wallet** holds your private keys (like a password) and your public address (like an account number). On Solana, wallets are identified by a public key (e.g., `7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU`).

On Solana, there are two key types:
- **EOA (Externally Owned Account):** Controlled by a private key
- **PDA (Program Derived Address):** Controlled by a program (smart contract)

> *Source: Solana-Arbitrage-Bot, polymarket*

---

### 1.4 Program Derived Addresses (PDAs)

A **PDA** is a deterministic address generated from seeds and a program ID. Same inputs always produce the same address — no one knows the private key, so only the program can control it.

```rust
fn derive_token_address(owner: &Pubkey, mint: &Pubkey) -> Pubkey {
    let (pda, _) = Pubkey::find_program_address(
        &[owner.to_bytes(), TOKEN_PROGRAM_ID.to_bytes(), mint.to_bytes()],
        &ASSOCIATED_TOKEN_PROGRAM_ID,
    );
    pda
}
```

**Why it matters:** No need to store addresses on-chain. Cryptographic math guarantees uniqueness.

> *Source: Solana-Arbitrage-Bot, solana-arb-0x19*

---

### 1.5 Associated Token Accounts (ATAs)

An **ATA** is the token account owned by a wallet for a specific mint. If you hold USDC, you have a USDC ATA. If you hold RAY, you have a RAY ATA.

**Analogy:** Think of your wallet as a bank, and each ATA as a separate sub-account for each currency (USD account, EUR account, etc.).

> *Source: solana-arb-0x19, solana-jupiter-arb*

---

### 1.6 Gas, Lamports, and Compute Units

**Gas** is the fee paid to execute transactions on a blockchain. Different chains use different units:

| Chain | Unit | Conversion |
|-------|------|------------|
| Ethereum | Gas (paid in ETH) | Varies by operation |
| Solana | Compute Units (CU) | Paid in lamports |
| Solana | Lamports | 1 SOL = 1,000,000,000 lamports |

**On Solana**, you set a compute budget to limit how much computation your transaction can use:
```typescript
const computeUnitLimitInstruction = ComputeBudgetProgram.setComputeUnitLimit({
    units: instructions.computeUnitLimit,
});
```

**Why it matters:** Every operation costs money. A failed transaction still costs gas. For arbitrage, where you might send hundreds of transactions, gas costs can eat all your profit.

> *Source: solana-arbitrage-bot-wsol, amm-arbitrageur, uniswap-arbitrage-analysis*

---

### 1.7 Transactions

A **transaction** is a set of instructions sent to the blockchain. Key properties:

- **Blockhash:** Every transaction needs a recent blockhash (expires after ~60 seconds on Solana)
- **Instructions:** What the transaction does (swap, transfer, etc.)
- **Accounts:** Which accounts the transaction reads or modifies
- **Signature:** Cryptographic proof that the sender authorized the transaction

```typescript
const { blockhash } = await connection.getLatestBlockhash();
```

> *Source: solana-arbitrage-bot-wsol, flashbots-simple-arbitrage*

---

### 1.8 Atomic Transactions

**Atomic** means all-or-nothing. Multiple operations either ALL succeed or ALL revert. If any step fails, the entire transaction is undone as if it never happened.

```
Step 1: Borrow $1,000,000       ✅
Step 2: Buy Token A             ✅
Step 3: Sell Token A for profit  ❌ (failed!)
→ ALL steps revert. No money lost (except gas).
```

**Why it matters for arbitrage:** You can attempt high-risk trades without worrying about getting stuck mid-trade. If the arb isn't profitable, everything reverts.

> *Source: Solana-Arbitrage-Bot, solana-arb-0x19, uniswap-arbitrage-analysis, flashbots-simple-arbitrage*

---

### 1.9 Versioned Transactions and Address Lookup Tables

Solana's newer transaction format (V0) supports **Address Lookup Tables (ALTs)** — pre-registered lists of addresses on-chain. Instead of including full 32-byte addresses, you reference a table index.

```typescript
const messageV0 = new TransactionMessage({
    payerKey: payer.publicKey,
    recentBlockhash: blockhash,
    instructions: ixs,
}).compileToV0Message(addressLookupTableAccounts);
const transaction = new VersionedTransaction(messageV0);
```

**Why it matters:** A single swap might need 20+ accounts. ALTs let you pack more instructions into one transaction, fitting within Solana's size limits.

> *Source: solana-arbitrage-bot-wsol*

---

### 1.10 Smart Contracts and On-Chain Programs

A **smart contract** is code that runs on the blockchain. On Solana, it's called a "program." It's immutable (can't be changed after deployment) and deterministic (same inputs always produce the same outputs).

For arbitrage, the on-chain program typically:
1. Records starting balance
2. Executes swaps
3. Checks ending balance
4. Reverts if not profitable

> *Source: Solana-Arbitrage-Bot, solana-arb-0x19, amm-arbitrageur*

---

### 1.11 Token Decimals and Precision

Each token has a different number of decimal places. Working with human-readable numbers (like "1.5 USDC") is dangerous in code — you must use raw amounts.

| Token | Decimals | Raw amount for 1 token |
|-------|----------|----------------------|
| USDC | 6 | 1,000,000 |
| SOL | 9 | 1,000,000,000 |
| ETH | 18 | 1,000,000,000,000,000,000 |

**StableSwap pools** use precision multipliers to normalize different decimals:
```rust
// A 6-decimal token gets multiplier 1
// A 9-decimal token gets multiplier 1000
```

> *Source: solana-arb-0x19, solana-jupiter-arb, amm-arbitrageur*

---

### 1.12 ERC-20 Approvals

Before a smart contract can spend your tokens, you must **approve** it on-chain. This is a one-time setup per token type.

```
"I authorize the Uniswap Router to spend up to 1000 USDC of mine."
```

**Two types (on Polymarket):**
1. **ERC-20 approval** (for pUSD collateral)
2. **ERC-1155 approval** (for conditional tokens/outcome tokens)

> *Source: polymarket, uniswap-arbitrage-analysis*

---

### 1.13 Signature Types (EOA, POLY_PROXY, Gnosis Safe)

Polymarket supports three ways to sign orders:

| Type | Name | Description |
|------|------|-------------|
| 0 | EOA | Direct signing from your wallet's private key |
| 1 | POLY_PROXY | Via a Polymarket proxy contract (allows sponsored transactions) |
| 2 | Gnosis Safe | Via a multi-sig Safe wallet (most secure) |

> *Source: polymarket*

---

### Key Takeaway

Blockchain fundamentals are the language of arbitrage. Tokens are what you trade, gas is what you pay, transactions are how you trade, and atomicity is your safety net. Understanding these concepts is prerequisite to everything else in this book.

---

## Chapter 2: Exchange Architecture

This chapter covers the different types of exchanges where arbitrage happens — from centralized order books to decentralized AMMs to prediction markets.

---

### 2.1 Centralized Exchanges (CEXs)

A **CEX** is a traditional exchange run by a company (Binance, Coinbase, Kraken). They maintain order books, match buyers and sellers, and custody your funds.

**Key characteristics:**
- Fast execution (off-chain matching)
- Requires account and KYC
- Company controls your funds
- REST/WebSocket APIs for data

> *Source: bitcoin-arbitrage, binance-triangle-arbitrage, r2-arbitrager*

---

### 2.2 Decentralized Exchanges (DEXs)

A **DEX** runs entirely on smart contracts. No company, no accounts, no custody. You trade directly from your wallet.

**Examples:**
| DEX | Blockchain | Type |
|-----|-----------|------|
| Uniswap | Ethereum | AMM |
| SushiSwap | Ethereum | AMM |
| Raydium | Solana | AMM |
| Orca | Solana | AMM |
| Serum | Solana | Order Book |
| PancakeSwap | BSC | AMM |
| Jupiter | Solana | Aggregator |

> *Source: Solana-Arbitrage-Bot, amm-arbitrageur, flashbots-simple-arbitrage*

---

### 2.3 Order Books (CLOB)

A **Central Limit Order Book** is the traditional exchange model. Buyers post limit orders ("I'll buy at $50"), sellers post limit orders ("I'll sell at $52"), and when prices match, a trade executes.

**Polymarket uses a CLOB** (not an AMM), which is unusual for DeFi:

| Feature | Order Book (Polymarket) | AMM (Uniswap) |
|---------|------------------------|---------------|
| Price discovery | Buyer/seller negotiation | Mathematical formula |
| Slippage | Linear (fixed at each level) | Exponential (curve-based) |
| Liquidity | Concentrated at best prices | Spread across entire curve |
| Speed | Very fast (off-chain matching) | Slower (on-chain) |

> *Source: polymarket, binance-triangle-arbitrage, r2-arbitrager*

---

### 2.4 AMMs (Automated Market Makers)

An **AMM** is a decentralized exchange that uses a mathematical formula instead of an order book. Users trade against a pool of tokens, not against other traders.

```
Price = Reserve_B / Reserve_A

Pool: 1000 TOKEN + 2000 USDC
Price: 1 TOKEN = 2 USDC
```

> *Source: amm-arbitrageur, uniswap-arbitrage-analysis, flashbots-simple-arbitrage*

---

### 2.5 Liquidity Pools

A **liquidity pool** is a smart contract holding two tokens that traders can swap between. Anyone can deposit tokens to become a "liquidity provider" (LP) and earn fees.

```
BNB/USDT Pool on PancakeSwap: 10,000 BNB + 3,000,000 USDT
BNB/USDT Pool on BakerySwap:   5,000 BNB + 1,400,000 USDT

Same pair, different pools, potentially different prices!
```

**Why it matters:** Different pools for the same pair create arbitrage opportunities.

> *Source: amm-arbitrageur, Solana-Arbitrage-Bot*

---

### 2.6 DEX Aggregators

A **DEX aggregator** finds the best price across ALL DEXs for a token swap. Instead of checking each DEX yourself, the aggregator does it in one API call.

**Jupiter** (Solana) is the most important aggregator for Solana arbitrage:
```
GET /quote?inputMint=WSOL&outputMint=USDC&amount=10000000
  → "Best route gives you 1.50 USDC (via Raydium + Orca split)"
```

> *Source: solana-arbitrage-bot-wsol, solana-jupiter-arb, Solana-Arbitrage-Bot*

---

### 2.7 Factory Pattern and Pair Discovery

Each DEX has a **factory** contract that can look up trading pairs. Arbitrage bots query factories to discover which token pairs exist on which DEXs.

```solidity
function getPair(address tokenA, address tokenB) external view returns (address pair);
```

**Pair discovery process:**
1. For each base token (WBNB, USDT, BUSD)
2. For each quote token (ETH, BTCB, CAKE, ...)
3. Query each DEX factory for the pair address
4. If pair exists on 2+ DEXs → potential arbitrage
5. Cache results to avoid re-querying

> *Source: amm-arbitrageur, flashbots-simple-arbitrage*

---

### 2.8 Spread, Bid, Ask, and Mid Price

- **Bid** = highest price someone will pay to buy
- **Ask** = lowest price someone wants to sell at
- **Spread** = Ask - Bid (the cost of immediate execution)
- **Mid** = (Ask + Bid) / 2 (the "fair" price estimate)

**In Polymarket:** `mid_up + mid_down` should be close to $1.00. If it deviates, there may be an arbitrage opportunity.

> *Source: polymarket, r2-arbitrager*

---

### 2.9 Order Book Depth and Walking the Book

Most naive tutorials compare best bid/ask prices. Real arbitrage bots **walk the order book** to calculate actual profit considering available volume.

```
Exchange A asks:  0.5 BTC @ $50,000  |  1.0 BTC @ $50,100
Exchange B bids:  2.0 BTC @ $50,500

Naive: "Profit $500 per BTC!"
Reality: To buy 1.5 BTC, average price = $50,066.67
Real profit: $650 (not $750)
```

> *Source: bitcoin-arbitrage, binance-triangle-arbitrage, r2-arbitrager*

---

### 2.10 Base and Quote Assets

- **Base token:** The token you want to profit in (WBNB, USDT, SOL). You keep these after arbitrage.
- **Quote token:** The token you borrow and sell. You don't hold these after arbitrage.

```
Pair: BTCB/WBNB
Base: WBNB (you profit in this)
Quote: BTCB (you borrow and sell this)
```

> *Source: amm-arbitrageur, binance-triangle-arbitrage*

---

### 2.11 Prediction Markets (Polymarket)

A **prediction market** lets you bet on future events. Polymarket uses binary outcomes (YES/NO or UP/DOWN):

- Each outcome has a token
- If the outcome happens, the token pays $1
- If not, it pays $0
- Token price = market's probability estimate

**Key math:** Since one outcome MUST happen:
```
UP_price + DOWN_price = $1.00 (par relationship)
```

If UP costs $0.60 and DOWN costs $0.35, total = $0.95. Buy both for $0.95, guarantee $1 payout, earn $0.05 profit.

> *Source: polymarket*

---

### Key Takeaway

Exchanges are where arbitrage happens. CEXs are fast but centralized. DEXs are trustless but slower. AMMs use math, order books use matching engines. Aggregators find the best price across all DEXs. Understanding each type's strengths and weaknesses is essential for finding opportunities.

---

## Chapter 3: AMM Mathematics

The math behind AMMs is the foundation of DeFi arbitrage. This chapter covers the formulas that determine prices, calculate outputs, and find optimal trade sizes.

---

### 3.1 Constant Product Formula (x * y = k)

The core pricing mechanism of Uniswap V2 AMMs. The product of reserves stays constant before and after a trade (ignoring fees).

```
Before trade: x₁ * y₁ = k
After trade:  x₂ * y₂ = k

If you add Δx tokens to the pool:
  x₂ = x₁ + Δx
  y₂ = k / x₂ = k / (x₁ + Δx)
  Δy = y₁ - y₂ = tokens you receive
```

**Example:**
```
Pool: 1000 TOKEN + 2000 USDC → k = 2,000,000
Buy 100 TOKEN:
  New x = 900, new y = 2,000,000 / 900 = 2,222.22 USDC
  You pay: 222.22 USDC for 100 TOKEN
  Effective price: 2.22 USDC per TOKEN (slippage!)
```

> *Source: amm-arbitrageur, uniswap-arbitrage-analysis, solana-arb-0x19, flashbots-simple-arbitrage*

---

### 3.2 getAmountOut and getAmountIn

**getAmountOut:** "If I put in X of token A, how much token B do I get?"
```
amountInWithFee = amountIn * 997
numerator = amountInWithFee * reserveOut
denominator = reserveIn * 1000 + amountInWithFee
amountOut = numerator / denominator
```

**getAmountIn:** "How much token A do I need to put in to get Y of token B?"
```
numerator = reserveIn * amountOut * 1000
denominator = (reserveOut - amountOut) * 997
amountIn = (numerator / denominator) + 1
```

> *Source: amm-arbitrageur, uniswap-arbitrage-analysis*

---

### 3.3 Swap Fees

Uniswap charges **0.3%** per trade. The math uses `r = 0.997` (99.7% of input passes through after fee).

```
amountInWithFee = amountIn * 997  // 0.3% fee deducted
```

The fee goes to liquidity providers, not the protocol.

**On Binance**, trading fees paid using BNB get a 25% discount.

> *Source: amm-arbitrageur, uniswap-arbitrage-analysis, binance-triangle-arbitrage*

---

### 3.4 Price Impact and Slippage

**Price impact** is how much a trade moves the price. Larger trades = more impact. Bigger pools = less impact.

**Slippage** is the difference between the expected price and the actual execution price. For arbitrage, even tiny slippage can erase profits.

```
Set slippage to 0 = you want EXACTLY the quoted price or fail
Risk: More failed transactions, but protects from losses
```

> *Source: solana-arbitrage-bot-wsol, uniswap-arbitrage-analysis, Solana-Arbitrage-Bot*

---

### 3.5 StableSwap (Curve.fi)

A different AMM formula optimized for tokens that trade near 1:1 (USDC/USDT). Uses an amplification parameter `A` to create a flatter curve around the peg.

```
Constant Product: x * y = k (curved everywhere)
StableSwap:       Flat near 1:1, curved far from peg
```

**Why it matters:** StableSwap pools have much less slippage for stablecoin pairs, making them attractive for arbitrage.

> *Source: solana-arb-0x19, Solana-Arbitrage-Bot*

---

### 3.6 Amplification Parameter (A)

Controls the shape of the StableSwap curve:
- **Higher A** = more like constant-sum (flat, low slippage)
- **Lower A** = more like constant-product (curved, higher slippage)

> *Source: solana-arb-0x19*

---

### 3.7 Newton's Method for Square Roots

An iterative algorithm to calculate square roots, used in the quadratic formula for optimal borrow amounts and in StableSwap calculations.

```
Guess: x₀ = n/2
Iterate: x_{i+1} = (x_i + n/x_i) / 2
Stop when: |x_i - x_{i+1}| < threshold
```

**Why not use built-in sqrt?** Solidity doesn't have a native sqrt for integers. The contract implements it manually.

**Optimization:** Use `n * 10^6` and divide by `10^3` at the end to handle decimal precision without floating-point math.

> *Source: amm-arbitrageur, solana-arb-0x19*

---

### 3.8 Virtual Reserves and Virtual Pools

When you chain A→B→C, it's mathematically equivalent to a single A→C pool with **virtual reserves** Ea, Eb. This simplifies multi-hop optimization.

```
Ea = 1000*Ra*Rb1 / (1000*Rb1 + 997*Rb)
Eb = 997*Rb1*Rb / (1000*Rb1 + 997*Rb)
```

> *Source: uniswap-arbitrage-analysis*

---

### 3.9 Optimal Input Amount

The exact amount of input token that maximizes profit. Too little = leaving money on the table. Too much = price impact eats profit.

```
         √(Ea × Eb × 0.997) - Ea
Δa* = ─────────────────────────────
                  0.997
```

> *Source: uniswap-arbitrage-analysis*

---

### 3.10 Optimal Borrow Amount for Arbitrage

The key question: How much should you borrow to maximize profit?

**Profit function:**
```
f(x) = (a2 * x) / (b2 + x) - (a1 * x) / (b1 - x)
```

**To find maximum, take derivative and set to 0:**
```
f'(x) = (a2 * b2) / (b2 + x)² - (a1 * b1) / (b1 - x)² = 0
```

**Solving the quadratic:**
```
a = a1*b1 - a2*b2
b = 2*b1*b2*(a1 + a2)
c = b1*b2*(a1*b2 - a2*b1)

x = (-b ± √(b² - 4ac)) / 2a
```

**Constraints:** `0 < x < b1` and `x < b2` (can't borrow more than available)

> *Source: amm-arbitrageur*

---

### 3.11 Fee Calculation with Fractions

Fees use numerator/denominator for precision (avoiding floating-point errors):

```rust
let fees = Fees {
    trade_fee_numerator: 25,        // 0.25% fee
    trade_fee_denominator: 10000,
    owner_trade_fee_numerator: 5,   // 0.05% to pool owner
    owner_trade_fee_denominator: 10000,
};

// Fee = amount * numerator / denominator
let fee = amount * 25 / 10000;  // 0.25%
```

**Why it matters:** Floating point math is imprecise. Integer fractions avoid rounding errors that could cost real money.

> *Source: Solana-Arbitrage-Bot*

---

### 3.12 Decimal Precision

The code uses Python's `Decimal` type for arbitrary precision to avoid floating point errors with large reserve values (which are in wei, often 18 decimals).

> *Source: uniswap-arbitrage-analysis*

---

### Key Takeaway

AMM math is deceptively simple. The constant product formula (x*y=k) determines everything: prices, slippage, and optimal trade sizes. Mastering these formulas — especially getAmountOut, optimal input calculation, and fee handling — is the difference between theoretical arbitrage knowledge and profitable execution.

---

## Chapter 4: Arbitrage Strategies

This chapter covers the different ways to extract profit from price differences — from simple cross-exchange arb to sophisticated multi-hop circular strategies.

---

### 4.1 Cross-Exchange Arbitrage

The simplest strategy: buy cheap on Exchange A, sell expensive on Exchange B.

```
PancakeSwap: 1 BNB = 300 USDT
BakerySwap:  1 BNB = 310 USDT

Buy 1 BNB on PancakeSwap for 300 USDT
Sell 1 BNB on BakerySwap for 310 USDT
Profit: 10 USDT
```

**Why prices differ:**
- Different liquidity depths
- Different trading volumes
- Slow bots (opportunity window)
- New information hasn't propagated yet

> *Source: amm-arbitrageur, bitcoin-arbitrage, r2-arbitrager, flashbots-simple-arbitrage*

---

### 4.2 Triangular Arbitrage

Exploiting price differences between three currencies in a loop on one exchange.

```
Start: 1 BTC
BTC → ETH: Get 30 ETH
ETH → XRP: Get 10,000 XRP
XRP → BTC: Get 1.005 BTC
Profit: 0.005 BTC (0.5%)
```

> *Source: binance-triangle-arbitrage, peregrine*

---

### 4.3 Circular Arbitrage

Instead of buying low and selling high, trade in a CIRCLE to capture tiny price inefficiencies.

```
Start: 0.01 WSOL
  → Swap WSOL → USDC (get 1.50 USDC)
  → Swap USDC → WSOL (get back 0.0102 WSOL)
  → Profit: 0.0002 WSOL
```

**Why it works:** If the WSOL/USDC price is slightly different across the routes Jupiter finds, the round-trip ends with more than you started.

> *Source: solana-arbitrage-bot-wsol, solana-jupiter-arb*

---

### 4.4 Inter-Exchange vs Intra-Exchange Arbitrage

- **Inter-exchange:** Buying a currency cheaply on one exchange and selling it at a higher price on another
- **Intra-exchange:** Finding profitable cycles within a single exchange across multiple trading pairs

> *Source: peregrine*

---

### 4.5 Flash Loan Arbitrage

The most powerful concept in DeFi: borrow unlimited money with zero collateral, execute arbitrage, repay in the same transaction.

```
1. Borrow $1,000,000 (no collateral needed!)
2. Execute arbitrage across DEXs
3. Repay $1,000,000 + small fee
4. Keep profit

If you can't repay → Transaction reverts → No loss
```

**dYdX Solo Margin** charges only 2 wei per loan (essentially free).

> *Source: Solana-Arbitrage-Bot, amm-arbitrageur, uniswap-arbitrage-analysis*

---

### 4.6 Cross-Time Arbitrage

Even if at every single moment `UP_ask + DOWN_ask > $1.00`, there might be arbitrage if you look across TIME:

```
At 10:00: UP_ask = $0.55, DOWN_ask = $0.50 → total = $1.05
At 10:02: UP_ask = $0.45, DOWN_ask = $0.48 → total = $0.93 (under par!)
```

The cheapest UP ($0.45) + cheapest DOWN ($0.48) = $0.93 — but they occurred at different moments!

**Caveat:** This is a DIAGNOSTIC — you can't execute at historical prices. But it tells you the theoretical floor.

> *Source: polymarket*

---

### 4.7 Par Relationship Arbitrage (Prediction Markets)

The fundamental arbitrage principle in binary markets:

```
If UP_ask + DOWN_ask < $1.00 → Buy both, guaranteed profit
If UP_bid + DOWN_bid > $1.00 → Sell both, guaranteed profit
```

**Why it works:** One token MUST pay out $1. Buy both for less than $1, profit the difference.

> *Source: polymarket*

---

### 4.8 PingPong Strategy

Alternate buying TokenA→TokenB and selling TokenB→TokenA, profiting from price oscillations between two tokens.

> *Source: solana-jupiter-arb*

---

### 4.9 Bundle Execution

To capture arbitrage in prediction markets, you need to buy BOTH outcome tokens simultaneously:

1. Create a FAK (Fill-and-Kill) order for UP token at the ask price
2. Create a FAK order for DOWN token at the ask price
3. Post both to the CLOB

**FAK vs FOK:**
- **FAK** (Fill-and-Kill): Fill what you can immediately, cancel the rest
- **FOK** (Fill-or-Kill): Fill the entire order or cancel everything

> *Source: polymarket*

---

### 4.10 Leg Sequencing (Staggered Entry)

Instead of buying both legs simultaneously, stagger them based on momentum:

- If UP ask is rising faster than DOWN → buy UP first (it might get more expensive)
- If DOWN ask is rising faster → buy DOWN first

**Why stagger:** If one leg's price is moving up quickly, buying it first reduces the risk of paying more later.

> *Source: polymarket*

---

### 4.11 Swing Detection

Analyze the PAIR GROSS cost (`UP_ask + DOWN_ask`) over time to detect swing patterns:

**"Rise then cheap":**
1. Pair gross rose from start of window to a peak
2. Current gross is significantly below that peak (pullback)
3. → Signal: consider buying NOW

> *Source: polymarket*

---

### 4.12 Halving Strategy

Start with the full balance, search for arbs, then halve the amount and search again (repeating 4 times). Larger swaps get worse rates due to price impact.

> *Source: solana-arb-0x19*

---

### 4.13 Trade Size Strategy

Two approaches to sizing trades:

- **Fixed** — uses initial balance every trade
- **Cumulative** — uses growing balance for compounding profits

> *Source: solana-jupiter-arb*

---

### 4.14 Profit Thresholds

Every bot has a minimum profit threshold to avoid wasting gas on tiny profits:

```typescript
const thre = 3000; // 3000 lamports ≈ $0.0005
if (diffLamports > thre) {
    // Execute arbitrage
}
```

**Why threshold:** Below this, transaction fees and tips eat all profit.

> *Source: solana-arbitrage-bot-wsol, solana-jupiter-arb, r2-arbitrager, amm-arbitrageur*

---

### Key Takeaway

Arbitrage isn't just "buy low, sell high." There are many strategies: cross-exchange, triangular, circular, flash loan, cross-time, and more. Each has different risk profiles, capital requirements, and complexity. The best bots combine multiple strategies and use graph theory to find the most profitable paths.

---

## Chapter 5: Graph Theory for Arbitrage

Finding profitable arbitrage paths is fundamentally a graph problem. This chapter covers the algorithms and data structures used to discover opportunities.

---

### 5.1 Directed Graphs

A **directed graph** (DiGraph) has edges with direction. Trading BTC→ETH is different from ETH→BTC because they have different exchange rates.

```
BTC ──→ ETH (rate: 15.5)
ETH ──→ BTC (rate: 0.064)
```

> *Source: peregrine, Solana-Arbitrage-Bot*

---

### 5.2 Multi-Directed Graphs

A **Multi-Directed Graph** allows multiple edges between the same pair of nodes. Used when multiple exchanges offer the same trading pair with different prices.

```
BTC ──→ ETH (via Binance, rate: 15.5)
BTC ──→ ETH (via Kraken, rate: 15.3)
```

> *Source: peregrine*

---

### 5.3 Nodes and Edges

- **Node (Vertex):** Represents a cryptocurrency (BTC, ETH, USD)
- **Edge:** Represents a tradeable market between two currencies
- **Edge Weight:** The cost of traversing an edge

> *Source: peregrine, Solana-Arbitrage-Bot, solana-arb-0x19*

---

### 5.4 Edge Weights and the Negative Log Transform

Peregrine uses `-log(rate)` as edge weights. This converts the multiplicative problem (chaining exchange rates) into an additive one (summing weights).

```
Without log: 0.05 × 2709 × 0.000026 = 0.00352 (>1? hard to compare)
With log: -log(0.05) + -log(2709) + -log(0.000026) = sum (easy to check if < 0)
```

**Why it matters:** Bellman-Ford works with addition, not multiplication. The log transform makes the math compatible.

> *Source: peregrine*

---

### 5.5 Negative Weight Cycles

A **negative weight cycle** is a loop where the sum of edge weights is negative. This means the product of exchange rates around the loop exceeds 1 — profit!

```
BTC → ETH → XLM → BTC
Weights: -log(0.05) + -log(2709) + -log(0.000026) = -0.003 (negative = profitable!)
```

> *Source: peregrine*

---

### 5.6 Bellman-Ford Algorithm

A shortest-path algorithm that can handle negative edge weights. Peregrine uses it to find negative cycles (which standard Dijkstra ignores).

**How it works:**
1. Initialize all distances to infinity, source to 0
2. Relax all edges V-1 times
3. If you can still relax an edge, there's a negative cycle

> *Source: peregrine*

---

### 5.7 Edge Relaxation

The core Bellman-Ford operation — checking if reaching a node through a different path yields a shorter distance:

```python
if distance_to[u] + w < distance_to[v]:
    distance_to[v] = distance_to[u] + w
    predecessor_to[v] = u
```

> *Source: peregrine*

---

### 5.8 DFS (Depth-First Search)

Graph algorithm used to explore all possible circular paths through token pairs. Controlled by `maxHops` to limit gas costs.

```
Start at TOKEN_A
  → Visit TOKEN_B (hop 1)
    → Visit TOKEN_C (hop 2)
      → Back to TOKEN_A? Profitable? EXECUTE!
      → Visit TOKEN_D (hop 3)
        → Back to TOKEN_A? Check profit!
```

> *Source: uniswap-arbitrage-analysis, solana-arb-0x19*

---

### 5.9 Brute Force Search with Pruning

Instead of fancy graph algorithms, some bots do a simple DFS exploring all paths up to a depth limit, with smart pruning:

```rust
fn brute_force_search(start_mint, current_balance, path, ...) {
    if path.len() == 4 { return; }  // Max 4 hops (Solana tx size limit)
    
    for each connected token {
        calculate output from pool
        
        if back at start AND profitable {
            EXECUTE ARBITRAGE!
        } else if token not in path {
            brute_force_search(start, new_balance, new_path, ...)
        }
    }
}
```

**What you learn:**
- Depth-limited search (don't go too deep)
- Cycle detection (don't visit same token twice, except start)
- Pruning (skip paths that can't be profitable)

> *Source: Solana-Arbitrage-Bot, solana-arb-0x19*

---

### 5.10 Path Retracing

After detecting a negative cycle, trace back through predecessor nodes to reconstruct the actual trading path.

```python
# Follow predecessors back to find the cycle
node = start
while predecessor[node] != start:
    path.append(node)
    node = predecessor[node]
```

> *Source: peregrine*

---

### 5.11 Triangle Discovery

Generating ALL possible triangles from trading pairs:

```
For each base (BTC, ETH, USDT):
  For each pair of other assets (B, C):
    If A/B, B/C, C/A markets all exist → valid triangle
```

This can generate thousands of triangles to monitor simultaneously.

> *Source: binance-triangle-arbitrage*

---

### Key Takeaway

Graph theory transforms arbitrage from "check random pairs" to "systematically find all profitable cycles." The negative log transform turns rate multiplication into weight addition, enabling Bellman-Ford to detect negative cycles (= profitable trades). DFS with pruning explores all paths efficiently. This is the mathematical backbone of every serious arbitrage bot.

---

## Chapter 6: Smart Contract Execution

This chapter covers how arbitrage is actually executed on-chain — flash loans, atomic transactions, profit validation, and the smart contract patterns that make risk-free trading possible.

---

### 6.1 Flash Loans

The most powerful concept in DeFi: borrow unlimited money with zero collateral, as long as you repay within the same transaction.

```
1. Borrow $1,000,000 (no collateral!)
2. Execute arbitrage
3. Repay $1,000,000 + small fee
4. Keep profit

Can't repay? Transaction reverts. No loss.
```

**Why it's safe for the pool:** If you can't repay, the entire transaction fails. The pool never loses money.

**Why it's powerful for you:** You need ZERO upfront capital. Just gas fees.

> *Source: Solana-Arbitrage-Bot, amm-arbitrageur, uniswap-arbitrage-analysis*

---

### 6.2 Flash Swaps

A feature of Uniswap V2 that lets you borrow tokens WITHOUT collateral, as long as you return them (plus a fee) within the SAME transaction.

```
1. Borrow 1000 TOKEN from Pool A (no collateral!)
2. Sell 1000 TOKEN on Pool B for USDT
3. Use some USDT to repay Pool A (in the other token)
4. Keep the profit
```

> *Source: amm-arbitrageur*

---

### 6.3 Flash Swap Callback (uniswapV2Call)

When you initiate a flash swap with non-empty `data`, the pool calls back to your contract. You must repay within this callback.

```
1. Your contract calls pool.swap() with data
2. Pool sends tokens to your contract
3. Pool calls your uniswapV2Call()
4. Inside callback: sell tokens on other pool, repay debt
5. Callback returns
6. Pool verifies it got paid
```

**Access control:** The contract checks `msg.sender == permissionedPairAddress` to ensure only the legitimate pool can call the callback.

> *Source: amm-arbitrageur*

---

### 6.4 Profit-or-Revert

The final instruction compares ending token balance to starting balance. If `final <= initial`, the entire transaction reverts. Risk-free (except gas).

```
1. Record starting balance: 1000 WSOL
2. Execute swaps across DEXs
3. Check ending balance: 1002 WSOL
4. Profit: 2 WSOL ✅ (keep it)
   OR
   Ending: 999 WSOL → REVERT (lose nothing)
```

> *Source: Solana-Arbitrage-Bot, solana-arb-0x19*

---

### 6.5 CPI (Cross-Program Invocation)

When the on-chain program calls another program (Orca, Serum, Jupiter). Each swap in the arb chain is a CPI call.

```
Your Program → CPI → Orca Swap Program → CPI → Token Program
```

> *Source: solana-arb-0x19*

---

### 6.6 SwapState PDA

A Program Derived Address that stores state across multiple instructions:
- `start_balance` — initial token balance
- `swap_input` — output of previous swap (becomes input for next)
- `is_valid` — flag for profit validation

> *Source: solana-arb-0x19*

---

### 6.7 The basic_pool_swap! Macro

A Rust macro that generates boilerplate for each swap instruction: read amount from SwapState → do CPI swap → write output back. Avoids code duplication.

> *Source: solana-arb-0x19*

---

### 6.8 MoneyPrinter.sol

The on-chain smart contract with two functions:
- `printMoney()` — self-funded swap (uses your own capital)
- `flashPrintMoney()` — dYdX flash loan arb (zero capital needed)

> *Source: uniswap-arbitrage-analysis*

---

### 6.9 Bundle Executor Contract

An on-chain contract that holds WETH and executes multiple swaps in sequence:

```
1. Transfer WETH to Market A
2. Swap WETH → DAI on Uniswap
3. Swap DAI → WETH on SushiSwap
4. Verify profit > miner tip
5. Pay miner tip via block.coinbase.transfer
```

> *Source: flashbots-simple-arbitrage*

---

### 6.10 Debt Repayment in Base Token

When you borrow quote tokens via flash swap, you repay in base tokens (not the borrowed token).

```
Borrow: 1000 USDT (quote token) from Pool 0
Repay: 3.33 BNB (base token) to Pool 0
```

Uniswap V2 allows repayment in either token of the pair.

> *Source: amm-arbitrageur*

---

### 6.11 Owner-Only Functions and Access Control

The contract uses OpenZeppelin's `Ownable` to restrict certain functions:

```solidity
function withdraw() external { ... }                    // Anyone can call
function addBaseToken(address token) external onlyOwner { ... }  // Owner only
function removeBaseToken(address token) external onlyOwner { ... }  // Owner only
```

> *Source: amm-arbitrageur*

---

### 6.12 EnumerableSet for Base Tokens

A data structure from OpenZeppelin that maintains a set of unique addresses with O(1) lookup.

```solidity
EnumerableSet.AddressSet baseTokens;
baseTokens.add(_WETH);           // Add WETH as base token
baseTokens.contains(token);      // Check if token is base
```

> *Source: amm-arbitrageur*

---

### 6.13 Fallback Function for Multi-DEX Support

Different DEXs use different callback function names. The contract uses a `fallback` to handle all of them:

```solidity
fallback(bytes calldata _input) external returns (bytes memory) {
    // Decode and route to uniswapV2Call()
}
```

PancakeSwap might call `pancakeCall()`, BakerySwap might call `bakeryCall()`. The fallback catches all.

> *Source: amm-arbitrageur*

---

### 6.14 On-Chain Profit Validation

The most critical piece: validate ACTUAL profit on-chain, not just quoted profit.

```
What's needed:
1. Record balance before swap
2. Execute swap ON-CHAIN
3. Check actual balance change
4. If profit > 0 → pay Jito tip
5. If profit < 0 → REVERT (no tip, no loss)
```

Without this, stale quotes can cause you to lose money even when the bot thinks it's profitable.

> *Source: solana-arbitrage-bot-wsol*

---

### Key Takeaway

Smart contracts are what make arbitrage risk-free. Flash loans give you unlimited capital. Atomic transactions ensure all-or-nothing execution. Profit-or-revert guarantees you never lose money on a bad trade. The on-chain program is your safety net — it validates actual profit before committing.

---

## Chapter 7: MEV & Priority Execution

MEV (Maximal Extractable Value) is the broader category that arbitrage operates in. This chapter covers how to get your transactions included first, and the ethical considerations of different MEV strategies.

---

### 7.1 MEV (Maximal Extractable Value)

Profit that can be extracted by reordering, inserting, or censoring transactions within a block. Arbitrage is one form of MEV.

**Other forms:**
| Strategy | How It Works | Ethical? |
|----------|-------------|----------|
| **Arbitrage** | Buy low on DEX A, sell high on DEX B | Yes |
| **Backrunning** | Place tx after a large trade | Yes |
| **Sandwich** | Frontrun + backrun large trades | No |
| **Sniping** | Buy tokens immediately when they launch | Gray area |
| **Copy Trading** | Mirror successful traders' transactions | Yes |

> *Source: Solana-Arbitrage-Bot, flashbots-simple-arbitrage, solana-arb-0x19*

---

### 7.2 Searchers

A **searcher** is a bot operator who searches for MEV opportunities and submits bundles to Flashbots or Jito. Every arbitrage bot in this book is a "searcher."

> *Source: flashbots-simple-arbitrage*

---

### 7.3 Flashbots

A system on Ethereum that lets bots submit transaction bundles directly to miners, bypassing the public mempool. This prevents front-running.

```
Normal transaction:  → Public mempool → Validator → Block
                     (anyone can see and front-run)

Flashbots bundle:    → Flashbots Relay → Miner → Block
                     (private, priority, no front-running)
```

> *Source: flashbots-simple-arbitrage*

---

### 7.4 Flashbots Bundles and Relay

A **bundle** is a group of transactions submitted atomically. The **relay** is an intermediary between searchers and miners.

**Key properties:**
- Bundles are atomic (all succeed or all fail)
- Sent to the relay, not broadcast publicly
- If not included, no cost (no gas wasted)

> *Source: flashbots-simple-arbitrage*

---

### 7.5 Jito Bundles

Jito is Solana's equivalent of Flashbots. It lets you submit transactions as "bundles" to validators for PRIORITY execution.

```
Normal transaction:  → Public mempool → Validator → Block
Jito bundle:         → Jito Block Engine → Validator → Block
                     (private, priority, no front-running)
```

> *Source: solana-arbitrage-bot-wsol*

---

### 7.6 Jito Block Engine

Jito runs block engines in different geographic locations. Frankfurt is one of them, close to European validators.

**Endpoint:** `https://frankfurt.mainnet.block-engine.jito.wtf/api/v1/bundles`

**Why location matters:** Lower latency to validators = faster inclusion.

> *Source: solana-arbitrage-bot-wsol*

---

### 7.7 Jito Tip

A payment to Jito validators for priority execution. The higher the tip, the more likely your bundle gets included.

```
jitoTip = Math.floor(diffLamports * 0.5)  // 50% of profit
```

**Trade-off:** Higher tip = faster execution but less profit. Lower tip = more profit but might not get included.

> *Source: solana-arbitrage-bot-wsol*

---

### 7.8 Backrunning

A type of MEV extraction where a bot places its transaction AFTER a large trade that creates a price discrepancy. This bot performs backruns.

```
Large trade moves price → Your arb tx captures the discrepancy
```

> *Source: flashbots-simple-arbitrage*

---

### 7.9 Sandwich Attacks

Frontrun a large trade (buy before it), then backrun it (sell after it). The victim gets worse execution, the attacker profits.

**This is unethical.** It's essentially stealing from other traders.

> *Source: Solana-Arbitrage-Bot*

---

### 7.10 Token Sniping

When a new token launches, there's a race:

```
T+0.000s  Creator adds liquidity (token now tradeable)
T+0.001s  Bot detects new pool
T+0.002s  Bot buys tokens
T+0.100s  Other bots notice
T+0.500s  Regular users find out
T+5.000s  Twitter announces
T+10.0s   Humans try to buy (price already 10x)
```

**Key insight:** The earliest buyers get the best price. Speed is everything.

> *Source: Solana-Arbitrage-Bot*

---

### 7.11 Private Mempool

Bundles sent to Flashbots/Jito never appear in the public mempool, so no one can see and front-run the arbitrage opportunity.

> *Source: flashbots-simple-arbitrage*

---

### 7.12 Miner Tip and Coinbase Transfer

Payment to the miner for including the bundle:

```solidity
block.coinbase.transfer(ethAmountToCoinbase);
```

`block.coinbase` is a special EVM variable that holds the address of the miner who produced the current block.

> *Source: flashbots-simple-arbitrage*

---

### 7.13 No Cost on Failure

If a Flashbots bundle isn't included in a block, the searcher pays nothing (no gas wasted). This is different from regular transactions, which cost gas even if they fail.

> *Source: flashbots-simple-arbitrage*

---

### 7.14 Priority Fees and skip_preflight

On Solana, you can set a priority fee in micro-lamports to get faster execution. You can also skip RPC preflight simulation to save time.

```typescript
// Skip preflight for speed
skipPreflight: true
```

> *Source: solana-jupiter-arb, solana-arb-0x19*

---

### 7.15 Target Block and Reputation

**Target block:** The block the bundle should be included in. Submit for both `blockNumber + 1` and `blockNumber + 2` to maximize inclusion chances.

**Reputation:** Flashbots tracks searcher reliability. Using a consistent signing key across runs builds reputation, improving bundle priority.

> *Source: flashbots-simple-arbitrage*

---

### Key Takeaway

MEV is the battlefield where arbitrage happens. Flashbots and Jito give you private, priority access to block space. Backrunning is ethical; sandwich attacks are not. Speed is everything — milliseconds matter. The highest tip wins, but too high eats your profit. Balancing tip size, execution speed, and profit is the art of MEV.

---

## Chapter 8: Risk Management

Even the best arbitrage strategy can lose money without proper risk management. This chapter covers the safety mechanisms that protect your capital.

---

### 8.1 Position Limits and Max Exposure

Maximum total position allowed across all exchanges (e.g., 0.1 BTC). Prevents overexposure if trades get stuck.

```rust
tx_cost <= self.max_capital_per_trade  // Don't risk too much
```

> *Source: r2-arbitrager, Solana-Arbitrage-Bot*

---

### 8.2 Single Leg Recovery

When only one side of an arbitrage order fills — a dangerous situation. You now have an unwanted position.

**Two strategies:**
- **Reverse:** Sell back the bought BTC. Takes a small loss but eliminates risk.
- **Proceed:** Retry the sell at a worse price. Accepts less profit to complete the arb.

> *Source: r2-arbitrager*

---

### 8.3 Slippage Protection

`amountOutMin` parameter ensures the trade reverts if the output is less than expected.

```typescript
slippageBps: 0  // Zero slippage for arbitrage
```

**Risk:** Zero slippage means more failed transactions, but protects you from losses.

> *Source: solana-arbitrage-bot-wsol, uniswap-arbitrage-analysis, solana-jupiter-arb*

---

### 8.4 Profit Sanity Checks

If something looks too good to be true, it probably is:

```python
if perc > 20:  # 20% profit? Suspicious.
    logging.warn("Profit=%f seems malformed" % (perc,))
    return  # Don't trade
```

**Why it matters:** A 20% arbitrage opportunity is almost certainly a data error.

> *Source: bitcoin-arbitrage*

---

### 8.5 Trade Cooldown

Don't spam trades:

```python
if current_time - self.last_trade < self.trade_wait:
    logging.warn("Last trade occurred %.2f seconds ago" % (current_time - self.last_trade))
    return
```

**Why it matters:** APIs have rate limits. Exchanges have fees. Rapid-fire trades can drain your balance.

> *Source: bitcoin-arbitrage*

---

### 8.6 Simulation Before Execution

Before risking real money, simulate:

```python
class MockMarket(object):
    def buy(self, volume, price):
        self.usd_balance -= price * volume
        self.btc_balance += volume - volume * self.fee
```

**Always paper trade first.** If your strategy loses money in simulation, it'll lose money for real.

> *Source: bitcoin-arbitrage, polymarket, solana-jupiter-arb*

---

### 8.7 Data Freshness and Expiration

Stale data is dangerous. Check if data is too old:

```python
if time.time() - self.depth_updated > config.market_expiration_time:
    self.depth = {"asks": [{"price": 0, "amount": 0}], ...}  # Expired!
```

**Trading on a 5-minute-old order book is like driving while looking in the rearview mirror.**

> *Source: bitcoin-arbitrage, binance-triangle-arbitrage*

---

### 8.8 Blacklist

Certain tokens/pairs are excluded (scams, broken tokens, low liquidity). Filter them out before checking for arbitrage.

> *Source: uniswap-arbitrage-analysis*

---

### 8.9 Broker Stability Tracker

Each exchange has a health score (1-10). Failed API calls decrement it. Below threshold = exchange disabled temporarily.

> *Source: r2-arbitrager*

---

### 8.10 Error Count Failsafe

Exits after 100 consecutive swap errors to prevent infinite failures.

> *Source: solana-jupiter-arb*

---

### 8.11 Exit Net Profit Ratio

When an open pair's profit has decreased by this percentage, close it to lock in remaining profit. Prevents holding losing positions.

> *Source: r2-arbitrager*

---

### 8.12 Execution Cap

Maximum number of trades before shutdown. Safety mechanism to prevent runaway trading.

> *Source: binance-triangle-arbitrage*

---

### 8.13 No Trade Periods

Scheduled maintenance windows where an exchange is excluded (e.g., bitFlyer 4:00-4:15 AM JST).

> *Source: r2-arbitrager*

---

### 8.14 Gas Estimation

Before submitting, estimate how much gas the bundle will use. If suspiciously high (>1.4M gas), skip (likely a bad trade).

> *Source: flashbots-simple-arbitrage*

---

### Key Takeaway

Risk management is what separates surviving bots from blowing-up bots. Position limits cap your exposure. Single-leg recovery handles stuck trades. Slippage protection prevents bad execution. Sanity checks catch data errors. Simulation validates strategies. Never trust external data blindly — always have safety nets.

---

## Chapter 9: Data & Infrastructure

The infrastructure behind an arbitrage bot — how to fetch data fast, handle rate limits, and store information efficiently.

---

### 9.1 RPC (Remote Procedure Call)

An **RPC** endpoint lets your bot interact with the blockchain. You send requests (get balance, send transaction) and receive responses.

**Private vs Public RPCs:**
| Type | Latency | Rate Limit | Reliability |
|------|---------|------------|-------------|
| Public | High | Low | Variable |
| Private | Low | High | High |

> *Source: solana-arbitrage-bot-wsol, solana-jupiter-arb*

---

### 9.2 WebSocket Streaming

Instead of repeatedly asking the server "any updates?", a WebSocket keeps a persistent connection open. The server pushes data to you the instant it changes.

**Polymarket uses WebSockets** for real-time order book updates:
- `book` — full order book snapshot
- `price_change` — individual level updates
- `best_bid_ask` — just the top-of-book prices

**Why WebSockets for trading:** HTTP polling = wasted requests + delay. WebSocket = instant updates, no polling overhead.

> *Source: polymarket, binance-triangle-arbitrage*

---

### 9.3 Batch RPC Queries

Instead of one HTTP request per pair, send a single HTTP request containing multiple `eth_call` RPCs. Dramatically speeds up reserve fetching.

```solidity
// UniswapFlashQuery.sol — read thousands of pair reserves in one call
```

> *Source: uniswap-arbitrage-analysis, flashbots-simple-arbitrage*

---

### 9.4 Rate Limiting and Key Rotation

Exchange APIs throttle requests. Handle this with:
- Retry logic and delays
- Multiple API keys rotating when one fails
- Caching responses to avoid re-fetching

> *Source: peregrine, uniswap-arbitrage-analysis*

---

### 9.5 Concurrent Data Fetching

Fetching from 10 exchanges sequentially? Slow. Fetch all at once:

```python
from concurrent.futures import ThreadPoolExecutor, wait

def update_depths(self):
    futures = []
    for market in self.markets:
        futures.append(self.threadpool.submit(self.__get_market_depth, market, depths))
    wait(futures, timeout=20)
```

Sequential = 20 seconds. Concurrent = 2 seconds.

> *Source: bitcoin-arbitrage, uniswap-arbitrage-analysis*

---

### 9.6 CCXT (Unified Exchange API)

A unified cryptocurrency exchange API library supporting 131+ exchanges. One interface for all exchanges.

> *Source: peregrine*

---

### 9.7 Sync Events (Incremental Updates)

Emitted by Uniswap pairs when reserves change. Parse block logs to incrementally update reserves instead of re-fetching everything.

> *Source: uniswap-arbitrage-analysis*

---

### 9.8 Price Merge Size and Quantization

**Price merge size:** Grouping small price levels into larger buckets (e.g., 100 JPY steps) to reduce noise.

**Quantization:** Prices rounded to the nearest cent ($0.01) before calculations. Prevents floating-point precision issues.

> *Source: r2-arbitrager, polymarket*

---

### 9.9 Hardhat Network Forking and Mainnet Fork Testing

**Hardhat** can fork a live blockchain for testing. **Solana test validator** can clone mainnet account states locally.

```bash
npx hardhat test  # Uses forked BSC mainnet
```

**Why it matters:** Test against real pool states without spending real money.

> *Source: amm-arbitrageur, solana-arb-0x19*

---

### 9.10 ChronoDB (Time-Series Storage)

A time-series key-value database used to persist active pairs, historical orders, and spread statistics.

> *Source: r2-arbitrager*

---

### 9.11 ZeroMQ (IPC Messaging)

High-performance messaging library used for IPC between main app, analytics process, and config updates.

> *Source: r2-arbitrager*

---

### 9.12 Secret Enclave (Encrypted Storage)

Instead of storing private keys in plaintext `.env` files, store them in an encrypted SQLite database.

**Why SQLite:**
- File-based (no server needed)
- WAL mode for concurrent reads
- Can be excluded from git via `.gitignore`

> *Source: polymarket*

---

### 9.13 Base58 Encoding

Solana uses base58 encoding for transaction serialization (not hex like Ethereum). More compact than hex, avoids ambiguous characters.

> *Source: solana-arbitrage-bot-wsol*

---

### Key Takeaway

Data is the lifeblood of arbitrage. WebSockets give you real-time updates. Batch queries reduce latency. Concurrent fetching maximizes speed. Private RPCs ensure reliability. Rate limiting keeps you from getting blocked. The fastest data pipeline wins the arbitrage race.

---

## Chapter 10: Trading Systems Architecture

This chapter covers the software engineering patterns that make arbitrage bots maintainable, testable, and extensible.

---

### 10.1 The Main Loop (Event Loop)

Real-time trading bots are event loops. They don't stop. They continuously scan, evaluate, execute, and repeat.

```
loop {
    1. Analyze market conditions
    2. Find opportunities (all strategies)
    3. Filter profitable ones
    4. Optimize gas costs
    5. Execute transactions
    6. Log results
    7. Sleep 500ms
}
```

> *Source: Solana-Arbitrage-Bot, solana-arbitrage-bot-wsol*

---

### 10.2 Observer Pattern (Event-Driven Architecture)

When something happens, don't hardcode what to do. Announce it and let listeners decide:

```python
for observer in self.observers:
    observer.opportunity(profit, volume, ...)

class Logger(Observer):
    def opportunity(self, ...):
        logging.info("profit: %f USD" % profit)

class TraderBotSim(Observer):
    def opportunity(self, ...):
        self.execute_trade(...)
```

**Why it matters:** Adding a new reaction (Discord alerts, database logging) doesn't require touching the detection logic.

> *Source: bitcoin-arbitrage*

---

### 10.3 Template Method Pattern

The base class defines the skeleton of an algorithm, subclasses fill in the blanks:

```python
class Market:
    def get_depth(self):
        if timediff > self.update_rate:
            self.ask_update_depth()  # Calls subclass method
        return self.depth

class Binance(Market):
    def update_depth(self):  # Fills in the blank
        # Actually fetch from Binance API
```

**Why it matters:** Write the workflow once. Each exchange only implements the unique part.

> *Source: bitcoin-arbitrage*

---

### 10.4 Strategy Pattern (Swappable Algorithms)

Different trading strategies behind a common interface:

```rust
trait Strategy {
    async fn find_opportunities(&self, market: &MarketConditions) -> Vec<MevOpportunity>;
    async fn execute_opportunities(&self, opportunities: &[MevOpportunity]);
}

let strategies: Vec<Box<dyn Strategy>> = vec![
    Box::new(ArbitrageStrategy::new(...)),
    Box::new(SnipingStrategy::new(...)),
    Box::new(CopyTradeStrategy::new(...)),
];
```

> *Source: Solana-Arbitrage-Bot*

---

### 10.5 Factory Pattern

Create objects based on configuration:

```rust
fn pool_factory(tipe: &PoolType, json_str: &String) -> Box<dyn PoolOperations> {
    match tipe {
        PoolType::OrcaPoolType => Box::new(OrcaPool::from_json(json_str)),
        PoolType::RaydiumType => Box::new(RaydiumPool::from_json(json_str)),
    }
}
```

> *Source: Solana-Arbitrage-Bot, solana-arb-0x19*

---

### 10.6 Trait-Based Polymorphism

Different DEXs have different APIs, but the bot treats them all the same:

```rust
trait PoolOperations {
    fn get_quote_with_amounts_scaled(amount_in, mint_in, mint_out) -> u128;
    fn swap_ix(program, owner, mint_in, mint_out) -> Instruction;
    fn get_mints() -> Vec<Pubkey>;
}

impl PoolOperations for OrcaPool { ... }
impl PoolOperations for RaydiumPool { ... }
```

**Want to add a new DEX?** Just implement the trait. The arbitrage logic doesn't change.

> *Source: Solana-Arbitrage-Bot, solana-arb-0x19*

---

### 10.7 Borg Pattern (Shared State)

Multiple instances of a class sharing the same state — like a singleton but more Pythonic:

```python
class FiatConverter:
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state
```

**Why it matters:** Currency conversion rates shouldn't be fetched 10 times. Fetch once, share everywhere.

> *Source: bitcoin-arbitrage*

---

### 10.8 Dependency Injection

Components receive their dependencies instead of creating them:

```rust
let rpc_client = Arc::new(RpcClient::new(...));
let dex_manager = Arc::new(Mutex::new(DexManager::new(rpc_client.clone())));

let sniping_strategy = SnipingStrategy::new(
    rpc_client.clone(),      // Injected
    dex_manager.clone(),     // Injected
    config.max_position_size,
);
```

**Why it matters:** Easy to test (inject mock dependencies), loose coupling, single responsibility.

> *Source: Solana-Arbitrage-Bot, r2-arbitrager*

---

### 10.9 Supervisor Pattern

A top-level orchestrator that manages the entire lifecycle:

```
resolve market → connect WebSocket → monitor for rollover → switch to new market → repeat
```

**Why a supervisor:** Markets are ephemeral (5-minute windows). The bot needs a resilient manager that handles transitions gracefully.

> *Source: polymarket*

---

### 10.10 Async/Await and the Event Loop

Python's `asyncio` lets you run multiple things "at once" without threads. The event loop switches between tasks when one is waiting.

**In trading bots:**
- WebSocket message handling
- Order book updates
- Rollover monitoring
- GUI updates

All run concurrently on a single thread.

> *Source: polymarket, peregrine*

---

### 10.11 Concurrent State Management

Multiple async tasks sharing state safely:

```rust
pub struct Metrics {
    pub orders: Arc<Mutex<Vec<Order>>>,
    pub profits: Arc<Mutex<HashMap<Pubkey, f64>>>,
}

pub async fn add_order(&self, order: Order) {
    self.orders.lock().await.push(order);
}
```

- **Arc** (Atomic Reference Counting) = shared ownership across threads
- **Mutex** = only one thread can modify at a time

> *Source: Solana-Arbitrage-Bot*

---

### 10.12 Metrics and Monitoring

Track performance over time:

```rust
println!("Total Orders: {}", orders.len());
println!("Total Profit: {:.2} SOL", profits.values().sum::<f64>());
println!("Total Volume: {:.2} SOL", volumes.values().sum::<f64>());
```

**You can't improve what you don't measure.** Track everything: orders, profits, volumes, success rates.

> *Source: Solana-Arbitrage-Bot, solana-jupiter-arb*

---

### 10.13 Typed Configuration

Configuration as typed structs, not magic strings:

```rust
#[derive(Debug, Deserialize, Clone)]
pub struct Config {
    pub solana: SolanaConfig,
    pub bot: BotConfig,
    pub dexes: DexesConfig,
    pub monitoring: MonitoringConfig,
}
```

**Catch config errors at startup, not runtime.**

> *Source: Solana-Arbitrage-Bot*

---

### 10.14 Custom Error Types

Domain-specific errors for better debugging:

```rust
#[error_code]
pub enum ArbitrageError {
    InsufficientProfit,
    SlippageExceeded,
    InvalidRoute,
    InsufficientLiquidity,
}
```

Generic errors like "operation failed" are useless. Domain errors tell you exactly what went wrong.

> *Source: Solana-Arbitrage-Bot*

---

### 10.15 Relayer Pattern (Gasless Transactions)

Instead of submitting transactions yourself (paying gas), a "relayer" submits them on your behalf. You sign off-chain, the relayer pays gas.

**Why relayers:** Users might not have native tokens for gas. The relayer solves this.

> *Source: polymarket*

---

### 10.16 Analytics Plugin

A JS file that receives spread statistics and can dynamically adjust config (e.g., set `minTargetProfitPercent` to μ + σ).

> *Source: r2-arbitrager*

---

### 10.17 Transport Layer (Logging)

Log pipeline that routes logs to console, files, Slack, LINE, and WebSocket clients simultaneously.

> *Source: r2-arbitrager*

---

### Key Takeaway

Software architecture determines whether your bot is maintainable or a nightmare. The Observer pattern decouples detection from reaction. Strategy pattern lets you swap algorithms. Dependency injection enables testing. The main loop is the heartbeat. Metrics tell you if it's working. Good architecture doesn't just make code cleaner — it makes your bot faster to iterate on and easier to debug when things go wrong at 3 AM.

---

## Appendix: Source Repositories

| # | Repository | What It Teaches |
|---|-----------|----------------|
| 1 | [bitcoin-arbitrage](https://github.com/maxme/bitcoin-arbitrage) | Cross-exchange CEX arbitrage, order book walking, Observer pattern, Template Method, concurrent fetching, simulation |
| 2 | [Solana-Arbitrage-Bot](https://github.com/x89/Solana-Arbitrage-Bot) | Graph-based path finding, brute force search, atomic transactions, flash loans, trait polymorphism, strategy pattern, MEV strategies, Rust |
| 3 | [polymarket-CONCEPTS](https://github.com/SupervisedAI/polymarket-analyzer) | Prediction markets, CLOB, WebSocket streaming, cross-time arbitrage, par relationship, dual-leg streaming, PyQt6 GUI, asyncio |
| 4 | [amm-arbitrageur](https://github.com/AurelianB/amm-arbitrageur) | AMM math (x*y=k), flash swaps, optimal borrow amount, Newton's method, Solidity smart contracts, BSC DeFi |
| 5 | [solana-arbitrage-bot-wsol](https://github.com/chainbuff/solana-arbitrage-bot) | Jupiter aggregator, circular arbitrage, Jito bundles, versioned transactions, WSOL wrapping, zero-slippage strategy |
| 6 | [uniswap-arbitrage-analysis](https://github.com/flashbots/simple-arbitrage) | Virtual reserves, optimal input amount, DFS path finding, batch RPC, dYdX flash loans, MoneyPrinter.sol |
| 7 | [flashbots-simple-arbitrage](https://github.com/flashbots/simple-arbitrage) | Flashbots bundles, private mempool, backrunning, BundleExecutor contract, miner tips, no-cost-on-failure |
| 8 | [peregrine](https://github.com/cryptolu/Peregrine) | Bellman-Ford algorithm, negative weight cycles, negative log transform, directed graphs, CCXT, Cython optimization |
| 9 | [binance-triangle-arbitrage](https://github.com/AurelianB/binance-triangle-arbitrage) | Triangular arbitrage, order book depth cache, WebSocket bundles, linear vs parallel execution, HUD |
| 10 | [r2-arbitrager](https://github.com/AurelianB/r2-bitcoin-arbitrager) | Inverted spread, single-leg recovery, ChronoDB, ZeroMQ, InversifyJS IoC, analytics plugins, transport layer |
| 11 | [solana-arb-0x19](https://github.com/0xNineteen/solana-arb) | DFS brute force, StableSwap, Newton's method, SwapState PDA, basic_pool_swap! macro, order book simulation, mainnet fork testing |
| 12 | [solana-jupiter-arb](https://github.com/ARBProtocol/solana-jupiter-arb) | Jupiter SDK, PingPong strategy, adaptive slippage, queue throttle, iteration tracking, React (Ink) config wizard |
| 13 | [bitcoin-arbitrage-CONCEPTS](https://github.com/maxme/bitcoin-arbitrage) | (Duplicate of #1 — same repository, same concepts) |

---

*This encyclopedia was compiled from 13 open-source arbitrage repositories. Each concept includes its source so you can dive deeper into the original implementation. The best way to learn is to read the code.*

---

**Total concepts covered: ~200+**
**Total source repositories: 13**
**Chapters: 10 + Appendix**
