from aiohttp import request
import pytest
from brownie import network
from brownie import OllieAndMayhemNFT
from scripts.deploy_and_create import deploy_and_create
from scripts.helpful_scripts import (
    FORKED_LOCAL_ENVIRONMENTS,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)


def test_can_create_OllieAndMayhemNFT():
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() not in FORKED_LOCAL_ENVIRONMENTS
    ):
        pytest.skip("This unit test is only for local testing\n")

    account = get_account()
    # deploy the contract
    # create an NFT
    nft, create_txn = deploy_and_create()

    requestID = create_txn.events["requestedNFT"]["requestID"]

    random_number = 333
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestID, random_number, nft.address, {"from": account}
    )

    assert nft.tokenCounter() == 1
    # TODO: add one more assert statement here to match random_number to pet and colour
