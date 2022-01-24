from brownie import account, config, network
from brownie import OllieAndMayhemNFT
from scripts.helpful_scripts import fund_with_link, get_account
from web3 import Web3

from scripts.set_tokenURI import set_tokenURI


def create_nft():
    account = get_account()
    nft_contract = OllieAndMayhemNFT[-1]

    fund_with_link(nft_contract.address, amount=Web3.toWei(0.1, "ether"))

    print("Creating an OllieAndMayhem NFT ...")
    create_txn = nft_contract.createNFT({"from": account})
    create_txn.wait(1)
    # it currently takes around 30 minutes on Rinkeby for the VRFCoordinator to come
    #   back to our nft_contract with some randomness -- just have to wait out this
    #   delay
    print(f"... Done!\n")

    set_tokenURI()


def main():
    create_nft()
