
from web3 import Web3


web3 = Web3(Web3.HTTPProvider('http://localhost:8552')) 


def generate_ethereum_address():
    account = web3.eth.account.create()
    return account.address, account._private_key.hex()


voter_address, voter_private_key = generate_ethereum_address()
authority_address, authority_private_key = generate_ethereum_address()


contract_abi = [{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256[]","name":"_data","type":"uint256[]"}],"name":"blindedVote","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"candidates","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"uint256","name":"voteCount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"electionAuthority","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"registerByDeadline","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"string","name":"_name","type":"string"}],"name":"registerCandidate","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_voter","type":"address"}],"name":"registerVoter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"revealVoteByDeadline","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_deadline","type":"uint256"}],"name":"setRegisterByDeadline","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_deadline","type":"uint256"}],"name":"setRevealVoteByDeadline","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_deadline","type":"uint256"}],"name":"setVoteByDeadline","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"setVotingTax","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"totalTaxCollected","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"_vote","type":"uint256[]"}],"name":"unblindVote","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"voteByDeadline","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"voters","outputs":[{"internalType":"bool","name":"registered","type":"bool"},{"internalType":"bool","name":"voted","type":"bool"},{"internalType":"bool","name":"revealed","type":"bool"},{"internalType":"uint256","name":"taxPaid","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"votingTax","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"winner","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]  # Replace [...] with the actual contract ABI
contract_address = '0xd8b934580fcE35a11B58C6D73aDeE468a2833fa8'  # Replace with actual contract address


contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def generate_certificate(voter_address, authority_address, private_key):
    certificate_message = f"I, {authority_address} assert that address {voter_address} is controlled by a voter who is eligible to vote in the election, and no other address controlled by this voter is currently registered."
    message_hash = web3.keccak(text=certificate_message)
    signature = web3.eth.account.signHash(message_hash, private_key)
    return signature.signature.hex()

certificate = generate_certificate(voter_address, authority_address, authority_private_key)
print("Certificate:", certificate)


try:
    
    tx_hash = contract.functions.blindedVote([1, 2, 3]).transact({'from': voter_address, 'gas': 300000})  # Adjust the gas limit as needed
    
    receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    print("Transaction receipt:", receipt)
except Exception as e:
    print("Error occurred:", e)

