from vyper import compile_code
from web3 import Web3
from guide import MY_ADDRESS, RPC_URL
import requests
from encrypt_key import KEYSTORE_PATH
import getpass
from eth_account import Account

MY_ADDRESS = MY_ADDRESS


def main():
    print("Let's read in the vyper code and deploy it!")
    with open("favorites.vy") as favorites_file:
        favorites_code = favorites_file.read()
        compilation_details = compile_code(favorites_code, output_formats=["bytecode", "abi"])
        print(compilation_details)

    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    favorites_contract = w3.eth.contract(bytecode=compilation_details["bytecode"], abi=compilation_details["abi"])
    print("Building the transaction...")

    nonce = w3.eth.get_transaction_count(MY_ADDRESS)

    transaction = favorites_contract.constructor().build_transaction(
        {
            "nonce": nonce,
            "from": MY_ADDRESS,
            "gas": 2000000,  # Sufficient gas for deployment
            "gasPrice": w3.to_wei('1', 'gwei'),  # Reasonable gas price
        }
    )
    
    print("Transaction: ", transaction)
   
    print("Signing the transaction...")
    private_key = decrpty_key()
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    print("Signed Transaction: ", signed_transaction)

    print("Sending the transaction...")
    tx_hash = w3.eth.send_raw_transaction(signed_transaction.raw_transaction)
    print(f"My TX hash is {tx_hash.hex()}")

    # Mine a block to include the transaction
    response = requests.post(RPC_URL, json={"jsonrpc": "2.0", "method": "evm_mine", "params": [], "id": 1})
    print("Mined a block:", response.json())

    # Wait for the transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
    print(f"Done! Contract deployed to {tx_receipt.contractAddress}")

def decrpty_key() -> str:
    with open (KEYSTORE_PATH, "r") as fp:
        encrypted_account = fp.read()
        password = getpass.getpass("Enter your password: ")
        key = Account.decrypt(encrypted_account,password)
        print("Decrypted Key!")
        return key
    

if __name__ == "__main__":
    main()