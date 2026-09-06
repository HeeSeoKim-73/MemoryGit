from web3 import Web3


RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"

CONTRACT_ADDRESS = "0x3A5F47E60808e1b52BEF775f0049032E73746606"


ABI = [
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "memoryId",
                "type": "string"
            }
        ],
        "name": "getMemory",
        "outputs": [
            {
                "internalType": "string",
                "name": "memoryHash",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "approvedBy",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "memoryId",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "memoryHash",
                "type": "string"
            }
        ],
        "name": "verifyMemory",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]


w3 = Web3(
    Web3.HTTPProvider(RPC_URL)
)


contract = w3.eth.contract(
    address=Web3.to_checksum_address(CONTRACT_ADDRESS),
    abi=ABI
)


def is_connected():
    return w3.is_connected()


def get_blockchain_memory(memory_id):
    result = contract.functions.getMemory(
        memory_id
    ).call()

    return {
        "memory_hash": result[0],
        "approved_by": result[1],
        "timestamp": result[2]
    }


def verify_blockchain_memory(
    memory_id,
    memory_hash
):
    return contract.functions.verifyMemory(
        memory_id,
        memory_hash
    ).call()