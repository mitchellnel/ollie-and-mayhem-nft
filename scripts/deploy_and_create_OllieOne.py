from brownie import config, network
from brownie import SimpleOllieAndMayhemNFT
from scripts.helpful_scripts import OPENSEA_URL, get_account

token_uri = "https://raw.githubusercontent.com/mitchellnel/ollie-and-mayhem-nft/master/metadata/ollie1.json"


def deploy_and_create_ollieOne():
    account = get_account()

    nft = SimpleOllieAndMayhemNFT.deploy({"from": account})

    print("Deploying and minting NFT ...")
    create_txn = nft.createCollectible(token_uri, {"from": account})
    create_txn.wait(1)
    print(
        f"... Done! You can view your NFT at {OPENSEA_URL.format(nft.address, nft.tokenCounter() - 1)}"
    )


def main():
    deploy_and_create_ollieOne()
