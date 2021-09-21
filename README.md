# BEVM 🅑 - Lightweight EVM for Trustless Scaling

BEVM (Band-powered Ethereum Virtual Machine) is a framework for creating a virtual blockchain
without block miners or validators. All transactions on a BEVM chain are recorded and finalized
by its host chain. By using Layer-1 as the data availablity and consensus layer, BEVM archives
L1-equivalent security while keeping the cost as low as theoretically possible. Developer tools
that work with Ethereum will also work similarly on BEVM chains.

> This project is pretty much WIP. Stay tuned for more updates!

## 💰 Cost to Interact with L1

BEVM is a logical layer of top of L1 (think [Omni](https://www.omnilayer.org/)). In order to
interact with a BEVM chain, a user must send a transaction payload to the Layer-1 blockchain.
To make the process efficient, users can send over transactions to a dedicated sequencer, who
collects the transactions and submits them all as a one L1 transaction. Cost per one BEVM
transaction is roughly 2000 Gas (~$0.3 per transacton at 50 Gwei/gas and
$3000 ETH/USD), making BEVM the most cost-efficient L2 scaling solution in the market.

While originally built to target Ethreum scaling, BEVM framework it not specific to Ethereum and
can be used to scale any Layer-1 blockchain with smart contract functionality, including BSC,
Solana, Avalanche, Terra/Cosmwasm chain, Fantom, etc.

## 🏃 Transaction Prioritization & First-Class Oracle Transactions

Most blockchains use auction markets for transaction ordering. This makes oracle updates not
reliable during network congestion and prone to front-running attacks. In BEVM, the network
sequencer can prioritize oracle transactions to ensure DeFi apps can always operate properly
and have reliable data sources.

While the network sequencer has the power to re-order transactions to ensure oracle transactions
always go through, it has no permission to censor user transactions. Anyone can interact directly
with BEVM, by passing the sequencer, by broadcasting transactions directly to the Layer-1 chain.

## 🌈 Asset bridge

To bridge asset from L1 to BEVM, the user can send assets directly to the BEVM contract on L1.
As soon as the transaction is confirmed, BEVM layer execution will pick up the transfer and mint
the corresponding asset on BEVM layer. This works for both native tokens (think ETH, FTM, SOL) or
other assets on chain.

To bridge assets back to L1, the user burns BEVM tokens corresponding to the asset on L1 and
the governance will unlock equivalent value of L1 tokens to users.

In addition to briding assets from L1 to the BEVM layer, anyone can issue BEVM native tokens as
well. As an EVM compatible layer, deploying an ERC-20, ERC-721, or ERC-1155 token works similarly
to deploying it on an L1 chain, with comparable security.
