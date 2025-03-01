from vyper import compile_code
from web3 import Web3

def main():
    print("Let's read in the vyper code and deploy it!")
    with open("favorites.vy") as favorites_file:
        favorites_code = favorites_file.read()
        compilation_details = compile_code(favorites_code, output_formats=["bytecode", "abi"])
        print(compilation_details)

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

    favorites_contract = w3.eth.contract(bytecode=compilation_details["bytecode"], abi=compilation_details["abi"])
    print("Building the transaction...")
    transaction = favorites_contract.constructor().build_transaction()
    # transaction = {

    # }
    print("Signing the transaction...")
    print("transaction: ", transaction)
    

if __name__ == "__main__":
    main()