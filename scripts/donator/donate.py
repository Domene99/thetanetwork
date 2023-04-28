# from brownie import VideoProcessing, accounts, config, VideoDonation
from dotenv import load_dotenv
from web3 import Web3
import os
import json

def donate(swear_count, topicKeys, topicValues, safety_score, language, value):    
    load_dotenv(".env")
    account_private = os.getenv("PRIVATE_KEY_2")
    account_address = "0x8EAce4Ac550f00272e217a36C778bc66e43078a1"

    # Connect to theta testnet
    w3 = Web3(Web3.HTTPProvider('https://eth-rpc-api-testnet.thetatoken.org/rpc'))

    # Take advantage of brownie deployment to get latest videoProcessing contract address
    with open("/home/domene/Documents/hacks/thetanetwork/build/deployments/map.json") as f:
        map = json.load(f)
    video_contract = map["365"]["VideoProcessing"][0]
    # Get latest videoDonation contract address and abi
    with open("/home/domene/Documents/hacks/thetanetwork/build/deployments/map.json") as f:
        map = json.load(f)
    video_donation_contract = map["365"]["VideoDonation"][0]
    with open("/home/domene/Documents/hacks/thetanetwork/build/deployments/365/" + video_donation_contract + ".json") as f:
        contract = json.load(f)
    abi = contract["abi"]

    videoDonationContract = w3.eth.contract(address=video_donation_contract, abi=abi)

    """
        address videoProcessing, 
        uint maxTries, 
        uint maxSwearCount, 
        uint minSafetyScore, 
        string memory language,
        string[] memory topics, 
        string[] memory sentiments
    """

    tx = videoDonationContract.functions.donate(
        video_contract, # address videoProcessing, 
        1, # uint maxTries, 
        swear_count, # uint maxSwearCount, 
        safety_score, # uint minSafetyScore, 
        language, # string memory language,
        topicKeys, # string[] memory topics, 
        topicValues, # string[] memory sentiments
        ).buildTransaction(
            {
                "chainId": 365,
                "gasPrice": w3.eth.gas_price,
                "from": account_address,
                "nonce": w3.eth.getTransactionCount(account_address),
                "value": 1000000000000000000 * value
            }
        )

    # print(tx,account_private)
    signed_greeting_txn = w3.eth.account.sign_transaction(
        tx, private_key=account_private
    )
    tx_greeting_hash = w3.eth.send_raw_transaction(signed_greeting_txn.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_greeting_hash)
    return tx_receipt