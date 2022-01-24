from brownie import config, network
from brownie import OllieAndMayhemNFT
from scripts.helpful_scripts import (
    OPENSEA_URL,
    fund_with_link,
    get_account,
    get_contract,
)


def deploy_and_create():
    account = get_account()

    print("Deploying OllieAndMayhemNFT contract ...")
    nft = OllieAndMayhemNFT.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(f"... Done! Contract deployed to {nft.address}\n")

    fund_with_link(nft.address)

    print("Creating an OllieAndMayhem NFT ...")
    create_txn = nft.createNFT({"from": account})
    create_txn.wait(1)
    print(f"... Done!\n")

    return nft, create_txn


def main():
    deploy_and_create()
