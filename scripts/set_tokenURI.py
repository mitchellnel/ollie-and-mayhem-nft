from brownie import network
from brownie import OllieAndMayhemNFT

from scripts.create_metadata import create_metadata
from scripts.helpful_scripts import OPENSEA_URL, get_account, get_colour, get_pet


def main():
    nft = OllieAndMayhemNFT[-1]

    number_of_NFTs = nft.tokenCounter()

    print(f"You have created {number_of_NFTs} NFTs.")

    # create all the new metadata
    URIs = [create_metadata()]

    for token_id in range(0, number_of_NFTs):
        if not nft.tokenURI(token_id).startswith("https://"):
            set_tokenURI(token_id, nft, URIs.pop(0))


def set_tokenURI(token_id, nft_contract, tokenURI):
    account = get_account()

    print(f"Setting token URI for OllieAndMayhem NFT with ID {token_id} ...")
    setURI_txn = nft_contract.setTokenURI(token_id, tokenURI, {"from": account})
    setURI_txn.wait(1)
    print(
        f"... Done! You can view your NFT at {OPENSEA_URL.format(nft_contract.address, token_id)}\n"
    )
