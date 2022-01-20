from brownie import config, network
from brownie import OllieAndMayhemNFT
from scripts.helpful_scripts import get_account


def deploy_nft():
    account = get_account()

    nft = OllieAndMayhemNFT.deploy({"from": account})


def main():
    pass
