import pytest, time
from brownie import network
from brownie import OllieAndMayhemNFT
from scripts.deploy_and_create import deploy_and_create
from scripts.helpful_scripts import (
    FORKED_LOCAL_ENVIRONMENTS,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)


def test_integration_can_create_OllieAndMayhemNFT():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        pytest.skip("This unit test is only for integration testing\n")

    account = get_account()
    # deploy the contract
    # create an NFT
    nft, create_txn = deploy_and_create()

    # wait for randomness to come back
    time.sleep(60)

    assert nft.tokenCounter() == 1
