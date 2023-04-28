from brownie import VideoDonation, accounts, config, VideoProcessing


def main():
    account = accounts.add(config["wallets"]["from_key_2"])
    videos = VideoDonation[-1]
    video = VideoProcessing[-1]
    videos.donate(video.address, 1, 10, 50, "English", ["marvel"], ["negative"], {"from": account, "value": 15})