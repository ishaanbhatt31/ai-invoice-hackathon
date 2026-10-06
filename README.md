# AI Invoice Generator with On-Chain Proof

An AI-powered invoice generator that drafts invoices from plain English and stores a cryptographic hash on the Sepolia blockchain as tamper-proof evidence.

## Problem

Freelancers and small businesses write invoices by hand and often face disputes about what was agreed or whether an invoice was changed. A verifiable record on-chain removes ambiguity and speeds up payment.

## Solution

1. User describes the work in plain English.
2. An LLM (Groq's `openai/gpt-oss-120b`) drafts a professional invoice.
3. The invoice is hashed (SHA-256) and the hash is stored on the Sepolia testnet.
4. Anyone can later verify the invoice wasn't changed by re-hashing the text and comparing it to the on-chain record.

## Tech Stack

- **AI**: Groq API (`openai/gpt-oss-120b`)
- **Backend**: Python, Flask, web3.py
- **Smart Contract**: Solidity (`InvoiceRegistry.sol`)
- **Frontend**: HTML + JavaScript
- **Blockchain**: Ethereum Sepolia testnet

## Deployed Contract

- **Address**: `0x95F22200f17be6B6E5Cb7309ddB22a907C6ccd40`
- **Network**: Sepolia
- **Explorer**: https://sepolia.etherscan.io/address/0x95F22200f17be6B6E5Cb7309ddB22a907C6ccd40

## Project Structure
ai-invoice-hackathon/
├── backend/
│ ├── app.py # Flask server: AI + blockchain logic
│ ├── abi.json # Contract interface
│ ├── requirements.txt # Python dependencies
│ └── .env # Secrets (NOT pushed to GitHub)
├── contract/
│ └── InvoiceRegistry.sol # Solidity smart contract
└── frontend/
└── index.html # User interface

text

## Setup Instructions

### 1. Prerequisites

- Python 3.10+
- A Sepolia wallet with test ETH (free from https://sepoliafaucet.com)
- A Groq API key (free at https://console.groq.com/keys)

### 2. Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate       # On Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
Create a .env file in backend/ with:

text
OPENAI_API_KEY=sk-proj-anything
PRIVATE_KEY=your-burner-wallet-private-key
RPC_URL=https://ethereum-sepolia-rpc.publicnode.com
CONTRACT_ADDRESS=0x95F22200f17be6B6E5Cb7309ddB22a907C6ccd40
GROQ_API_KEY=gsk_your-groq-key
Run the backend:

bash
python app.py
Server runs at http://127.0.0.1:5000

3. Frontend Setup
In a second terminal:

bash
cd frontend
python -m http.server 8000
Open http://127.0.0.1:8000 in your browser.

4. Using the App
Type a work description (e.g. "Logo design for 0.05 ETH")

Click Generate Invoice — the AI drafts a professional invoice

Paste your MetaMask wallet address

Click Store on Blockchain — the invoice hash is written to Sepolia

Click the Etherscan link to see the transaction

Smart Contract
solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InvoiceRegistry {
    mapping(string => address) public invoiceIssuers;
    event HashStored(string indexed invoiceHash, address indexed issuer);

    function storeHash(string memory _hash) public {
        require(invoiceIssuers[_hash] == address(0), "Hash already stored");
        invoiceIssuers[_hash] = msg.sender;
        emit HashStored(_hash, msg.sender);
    }
}
Why the Blockchain is Necessary
The full invoice is stored off-chain (too expensive and private for on-chain). Only the SHA-256 hash goes on-chain. This means:

Anyone can prove the invoice wasn't tampered with after being issued

The issuer's wallet address is permanently recorded

The proof is publicly verifiable without exposing the invoice contents

License
MIT

text

**Step 3: Save** (`Ctrl + S`).

**Step 4: Also create the `contract/InvoiceRegistry.sol` file** so it's included in the repo:

In VS Code, right-click the `contract` folder → New File → name it `InvoiceRegistry.sol` → paste:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InvoiceRegistry {
    mapping(string => address) public invoiceIssuers;
    event HashStored(string indexed invoiceHash, address indexed issuer);

    function storeHash(string memory _hash) public {
        require(invoiceIssuers[_hash] == address(0), "Hash already stored");
        invoiceIssuers[_hash] = msg.sender;
        emit HashStored(_hash, msg.sender);
    }
}