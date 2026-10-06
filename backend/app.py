import os
import json
import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from web3 import Web3
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
account = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))

with open("abi.json", "r") as f:
    contract_abi = json.load(f)

contract = w3.eth.contract(
    address=os.getenv("CONTRACT_ADDRESS"),
    abi=contract_abi
)

ai_client = Groq(api_key=os.getenv("GROQ_API_KEY"))


@app.route("/generate", methods=["POST"])
def generate_invoice():
    desc = request.json.get("description", "")
    response = ai_client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": f"Create a short professional invoice for: {desc}"}]
    )
    invoice_text = response.choices[0].message.content
    invoice_hash = hashlib.sha256(invoice_text.encode()).hexdigest()
    return jsonify({"invoice_data": invoice_text, "hash": invoice_hash})


@app.route("/store", methods=["POST"])
def store_on_chain():
    invoice_hash = request.json.get("hash")
    tx = contract.functions.storeHash(invoice_hash).build_transaction({
        "from": account.address,
        "chainId": 11155111,
        "gas": 200000,
        "maxFeePerGas": w3.to_wei("2", "gwei"),
        "maxPriorityFeePerGas": w3.to_wei("1", "gwei"),
        "nonce": w3.eth.get_transaction_count(account.address),
    })
    signed = w3.eth.account.sign_transaction(tx, private_key=os.getenv("PRIVATE_KEY"))
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    return jsonify({"tx_hash": w3.to_hex(tx_hash)})


if __name__ == "__main__":
    app.run(port=5000)