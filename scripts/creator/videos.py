# from brownie import VideoProcessing, accounts, config
from dotenv import load_dotenv
from web3 import Web3
import os
import json

def addVideo(address, player_uri, playback_uri, swear_count, topicKeys, topicValues, safety_score, languages):
    load_dotenv(".env")
    account_private = os.getenv("PRIVATE_KEY")
    account_address = "0x7394B6c17FDa8e1d39898FBA8b532B66013C5Eed"

    # Connect to theta testnet
    w3 = Web3(Web3.HTTPProvider('https://eth-rpc-api-testnet.thetatoken.org/rpc'))

    # Take advantage of brownie deployment to get latest contract address and abi
    with open("/home/domene/Documents/hacks/thetanetwork/build/deployments/map.json") as f:
        map = json.load(f)
    video_contract = map["365"]["VideoProcessing"][0]
    with open("/home/domene/Documents/hacks/thetanetwork/build/deployments/365/" + video_contract + ".json") as f:
        contract = json.load(f)
    abi = contract["abi"]

    videoProcessingContract = w3.eth.contract(address=video_contract, abi=abi)

    # address payable _owner,
    # string memory _player_uri,
    # string memory _playback_uri,
    # uint _swear_count,
    # string[] memory _topicKeys,
    # string[] memory _topicValues,
    # uint _safety_score,
    # string[] memory _languages

    tx = videoProcessingContract.functions.addVideo(
        address, # address payable _owner,
        player_uri, # string memory _player_uri,
        playback_uri, # string memory _playback_uri,
        swear_count, # uint _swear_count,
        topicKeys, # string[] memory _topicKeys,
        topicValues, # string[] memory _topicValues,
        safety_score, # uint _safety_score,
        languages, # string[] memory _languages
        ).buildTransaction(
            {
                "chainId": 365,
                "gasPrice": w3.eth.gas_price,
                "from": account_address,
                "nonce": w3.eth.getTransactionCount(account_address)
            }
        )
            
    signed_greeting_txn = w3.eth.account.sign_transaction(
        tx, private_key=account_private
    )
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    return tx_receipt
    # account = accounts.add(config["wallets"]["from_key"])
    # videos = VideoProcessing[-1]
    # videos.addVideo(address, player_uri, playback_uri, swear_count, topicKeys, topicValues, safety_score, languages, {"from": account})