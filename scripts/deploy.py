from brownie import VideoProcessing, accounts, config, VideoDonation

def deploy_contracts():
    account = accounts.add(config["wallets"]["from_key"])
    videos = VideoProcessing.deploy({"from": account})
    donations = VideoDonation.deploy({"from": account})

def main():
    deploy_contracts()