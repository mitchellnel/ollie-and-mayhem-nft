from brownie import config, network
from brownie import OllieAndMayhemNFT
from scripts.create_nft import create_nft
from scripts.helpful_scripts import (
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

    create_nft()


def main():
    deploy_and_create()
